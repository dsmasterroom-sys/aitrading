"""
실시간 모니터링 & 자동매매 엔진 (안정성 개선판)
"""
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from kis_api import KISAPIClient
from strategy_parser import (
    ActionType,
    TradingCondition,
    get_buy_targets,
    get_sell_targets
)

BASE_DIR = Path('/Users/master/.openclaw/workspace/kis-trading-bot')
STATE_PATH = BASE_DIR / 'runtime-state.json'
HOLIDAY_PATH = BASE_DIR / 'market-holidays.json'
REPORT_PATH = BASE_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(BASE_DIR / 'trading.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingEngine:
    """자동매매 엔진"""

    def __init__(self, dry_run: bool = False):
        self.client = KISAPIClient()
        self.dry_run = dry_run
        self.executed_orders: List[Dict] = []
        self.daily_trade_amount = 0
        self.max_daily_amount = 5000000
        self.order_cooldown_sec = 180

        self.state = self._load_state()
        logger.info(f"{'🧪 시뮬레이션' if dry_run else '🚀 실전'} 모드로 시작")

    def _today(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')

    def _load_holidays(self) -> set:
        if not HOLIDAY_PATH.exists():
            return set()
        try:
            data = json.loads(HOLIDAY_PATH.read_text(encoding='utf-8'))
            if isinstance(data, list):
                return set(str(x) for x in data)
            if isinstance(data, dict):
                return set(str(x) for x in data.get('holidays', []))
            return set()
        except Exception:
            return set()

    def _is_trading_day(self, now: datetime) -> bool:
        # 주말 제외
        if now.weekday() >= 5:
            return False
        # 사용자 정의 휴장일 제외
        holidays = self._load_holidays()
        return now.strftime('%Y-%m-%d') not in holidays

    def _load_state(self) -> Dict:
        if self.dry_run:
            state = {
                'date': self._today(),
                'daily_trade_amount': 0,
                'symbol_locks': {},
                'last_order_ts': {}
            }
            self.daily_trade_amount = 0
            return state

        if STATE_PATH.exists():
            try:
                state = json.loads(STATE_PATH.read_text(encoding='utf-8'))
            except Exception:
                state = {}
        else:
            state = {}

        if state.get('date') != self._today():
            state = {
                'date': self._today(),
                'daily_trade_amount': 0,
                'symbol_locks': {},  # e.g. 005930: {action: 'BUY', ts: ...}
                'last_order_ts': {}
            }
        self.daily_trade_amount = int(state.get('daily_trade_amount', 0))
        return state

    def _save_state(self):
        if self.dry_run:
            return
        self.state['daily_trade_amount'] = self.daily_trade_amount
        STATE_PATH.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding='utf-8')

    def _is_symbol_locked(self, stock_code: str, action: str) -> bool:
        lock = self.state.get('symbol_locks', {}).get(stock_code)
        if not lock:
            return False
        return lock.get('action') == action

    def _set_symbol_lock(self, stock_code: str, action: str):
        self.state.setdefault('symbol_locks', {})[stock_code] = {
            'action': action,
            'ts': datetime.now().isoformat()
        }
        self._save_state()

    def _cooldown_ok(self, stock_code: str) -> bool:
        now = time.time()
        last = self.state.setdefault('last_order_ts', {}).get(stock_code, 0)
        if now - last < self.order_cooldown_sec:
            return False
        self.state['last_order_ts'][stock_code] = now
        self._save_state()
        return True

    def check_price_condition(self, current_price: int, target_min: int, target_max: int) -> bool:
        return target_min <= current_price <= target_max

    def _get_holding_qty(self, stock_code: str, balance: Dict) -> int:
        for s in balance.get('보유종목', []):
            if s.get('종목코드') == stock_code:
                return int(s.get('보유수량', 0))
        return 0

    def _confirm_position_change(self, stock_code: str, before_qty: int, expected_delta: int, timeout_sec: int = 20) -> Tuple[bool, int]:
        """주문 후 잔고 변화를 폴링하여 체결 유사 확인"""
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            bal = self.client.get_balance()
            if bal:
                after_qty = self._get_holding_qty(stock_code, bal)
                if (after_qty - before_qty) == expected_delta:
                    return True, after_qty
            time.sleep(2)
        bal = self.client.get_balance()
        after_qty = self._get_holding_qty(stock_code, bal) if bal else before_qty
        return False, after_qty

    def execute_sell(self, condition: TradingCondition, current_price: int) -> bool:
        if not (condition.sell_price_min and condition.sell_price_max):
            return False
        if not self.check_price_condition(current_price, condition.sell_price_min, condition.sell_price_max):
            return False
        if self._is_symbol_locked(condition.stock_code, 'SELL'):
            return False
        if not self._cooldown_ok(condition.stock_code):
            return False

        balance = self.client.get_balance()
        if not balance:
            logger.warning(f"⚠️ 잔고 조회 실패로 매도 보류: {condition.stock_name}")
            return False

        holding_qty = self._get_holding_qty(condition.stock_code, balance)
        sell_qty = min(int(condition.sell_qty or 0), holding_qty)
        if sell_qty <= 0:
            logger.info(f"ℹ️ 매도 가능 수량 없음: {condition.stock_name}")
            self._set_symbol_lock(condition.stock_code, 'SELL')
            return False

        trade_amount = current_price * sell_qty
        if self.daily_trade_amount + trade_amount > self.max_daily_amount:
            logger.warning(f"⚠️ 일일 거래 한도 초과: {trade_amount:,}원")
            return False

        logger.info(f"📉 매도 조건 충족: {condition.stock_name} {current_price:,}원 ({sell_qty}주)")
        before_qty = holding_qty

        if self.dry_run:
            result = True
            confirmed = True
            after_qty = before_qty - sell_qty
        else:
            result = self.client.sell_order(condition.stock_code, sell_qty, current_price, order_type="00")
            confirmed, after_qty = self._confirm_position_change(condition.stock_code, before_qty, -sell_qty)

        status = 'confirmed' if (result and confirmed) else ('submitted' if result else 'failed')

        if result:
            self._set_symbol_lock(condition.stock_code, 'SELL')
            if confirmed:
                self.daily_trade_amount += trade_amount
            self.executed_orders.append({
                'time': datetime.now().isoformat(),
                'action': '매도',
                'stock_name': condition.stock_name,
                'stock_code': condition.stock_code,
                'price': current_price,
                'quantity': sell_qty,
                'amount': trade_amount,
                'status': status,
                'before_qty': before_qty,
                'after_qty': after_qty
            })
            self._save_state()
            logger.info(f"✅ 매도 {status}: {condition.stock_name} {sell_qty}주 @ {current_price:,}원")
        return result and confirmed

    def execute_buy(self, condition: TradingCondition, current_price: int) -> bool:
        if not (condition.buy_price_min and condition.buy_price_max):
            return False
        if not self.check_price_condition(current_price, condition.buy_price_min, condition.buy_price_max):
            return False
        if self._is_symbol_locked(condition.stock_code, 'BUY'):
            return False
        if not self._cooldown_ok(condition.stock_code):
            return False

        buy_qty = int(condition.buy_qty or 0)
        if buy_qty <= 0:
            return False

        balance = self.client.get_balance()
        if not balance:
            logger.warning(f"⚠️ 잔고 조회 실패로 매수 보류: {condition.stock_name}")
            return False

        available_cash = int(balance.get('예수금', 0))
        trade_amount = current_price * buy_qty
        if trade_amount > available_cash:
            logger.warning(f"⚠️ 예수금 부족: 필요 {trade_amount:,}원 / 보유 {available_cash:,}원")
            return False

        if self.daily_trade_amount + trade_amount > self.max_daily_amount:
            logger.warning(f"⚠️ 일일 거래 한도 초과: {trade_amount:,}원")
            return False

        logger.info(f"📈 매수 조건 충족: {condition.stock_name} {current_price:,}원 ({buy_qty}주)")
        before_qty = self._get_holding_qty(condition.stock_code, balance)

        if self.dry_run:
            result = True
            confirmed = True
            after_qty = before_qty + buy_qty
        else:
            result = self.client.buy_order(condition.stock_code, buy_qty, current_price, order_type="00")
            confirmed, after_qty = self._confirm_position_change(condition.stock_code, before_qty, buy_qty)

        status = 'confirmed' if (result and confirmed) else ('submitted' if result else 'failed')

        if result:
            self._set_symbol_lock(condition.stock_code, 'BUY')
            if confirmed:
                self.daily_trade_amount += trade_amount
            self.executed_orders.append({
                'time': datetime.now().isoformat(),
                'action': '매수',
                'stock_name': condition.stock_name,
                'stock_code': condition.stock_code,
                'price': current_price,
                'quantity': buy_qty,
                'amount': trade_amount,
                'status': status,
                'before_qty': before_qty,
                'after_qty': after_qty
            })
            self._save_state()
            logger.info(f"✅ 매수 {status}: {condition.stock_name} {buy_qty}주 @ {current_price:,}원")
        return result and confirmed

    def check_stop_loss(self, condition: TradingCondition, current_price: int) -> bool:
        if not condition.stop_loss:
            return False
        if current_price <= condition.stop_loss:
            logger.warning(f"🚨 손절가 도달: {condition.stock_name} {current_price:,}원 <= {condition.stop_loss:,}원")
            if self.dry_run:
                return True
            qty = max(1, condition.holding_qty)
            return self.client.sell_order(condition.stock_code, qty, 0, order_type="01")
        return False

    def monitor_once(self) -> Dict:
        results = {'timestamp': datetime.now().isoformat(), 'actions': []}

        for condition in get_sell_targets():
            price_info = self.client.get_current_price(condition.stock_code)
            if not price_info:
                continue
            current_price = price_info['현재가']
            if self.check_stop_loss(condition, current_price):
                results['actions'].append({'type': '손절', 'stock': condition.stock_name, 'price': current_price})
                continue
            if self.execute_sell(condition, current_price):
                results['actions'].append({'type': '매도', 'stock': condition.stock_name, 'price': current_price})

        for condition in get_buy_targets():
            price_info = self.client.get_current_price(condition.stock_code)
            if not price_info:
                continue
            current_price = price_info['현재가']
            if self.check_stop_loss(condition, current_price):
                results['actions'].append({'type': '손절', 'stock': condition.stock_name, 'price': current_price})
                continue
            if self.execute_buy(condition, current_price):
                results['actions'].append({'type': '매수', 'stock': condition.stock_name, 'price': current_price})

        return results

    def run(self, interval: int = 30):
        logger.info("=" * 60)
        logger.info("🤖 자동매매 모니터링 시작")
        logger.info(f"   체크 간격: {interval}초")
        logger.info(f"   일일 한도: {self.max_daily_amount:,}원")
        logger.info("=" * 60)

        try:
            while True:
                now = datetime.now()
                hour = now.hour
                minute = now.minute

                if not self._is_trading_day(now):
                    logger.info(f"📅 휴장일/주말 대기 중... (현재 {now.strftime('%Y-%m-%d %H:%M')})")
                    time.sleep(1800)
                    continue

                if not ((hour == 9 and minute >= 30) or (10 <= hour < 15) or (hour == 15 and minute < 20)):
                    logger.info(f"⏸️  장 시간 외 대기 중... (현재 {now.strftime('%H:%M')})")
                    time.sleep(60)
                    continue

                results = self.monitor_once()
                if results['actions']:
                    logger.info(f"📊 {len(results['actions'])}건의 거래 실행")

                time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("\n⏹️  모니터링 중지")
            self.save_report()

    def save_report(self):
        report_path = REPORT_PATH / f"report-{self._today()}.json"
        report = {
            'date': self._today(),
            'total_trades': len(self.executed_orders),
            'total_amount': self.daily_trade_amount,
            'orders': self.executed_orders
        }
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        logger.info(f"📄 매매 일지 저장: {report_path}")


if __name__ == "__main__":
    import sys

    dry_run = 'real' not in sys.argv
    auto_confirm = '--auto-confirm' in sys.argv

    if not dry_run and not auto_confirm:
        confirm = input("⚠️  실전 모드로 실행하시겠습니까? (yes/no): ")
        if confirm.lower() != 'yes':
            print("취소되었습니다.")
            sys.exit(0)

    engine = TradingEngine(dry_run=dry_run)
    engine.run(interval=30)
