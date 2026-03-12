#!/usr/bin/env python3
"""
장 시작 전 체크리스트 & 알림
"""
import sys
import json
from datetime import datetime
sys.path.append('/Users/master/.openclaw/workspace/kis-trading-bot')

from kis_api import KISAPIClient
from strategy_parser import get_buy_targets, get_sell_targets, get_hold_targets


def format_telegram_message(balance: dict, strategy_summary: str) -> str:
    """텔레그램 메시지 포맷"""
    today = datetime.now().strftime('%Y-%m-%d')
    msg = f"🌅 **장 시작 전 체크** ({today})\n\n"
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    
    msg += "💼 **계좌 현황**\n"
    msg += f"• 예수금: {balance['예수금']:,}원\n"
    msg += f"• 총평가: {balance['총평가금액']:,}원\n"
    msg += f"• 총손익: {balance['총손익']:+,}원\n"
    msg += f"• 보유종목: {len(balance['보유종목'])}개\n\n"
    
    msg += "━━━━━━━━━━━━━━━━━━\n\n"
    msg += strategy_summary
    msg += "\n━━━━━━━━━━━━━━━━━━\n\n"
    
    msg += "⏰ **일정**\n"
    msg += "• 08:30 ✅ 사전 체크 완료\n"
    msg += "• 09:00 장 시작\n"
    msg += "• 09:30 자동매매 시작\n"
    msg += "• 15:20 장 마감\n\n"
    
    msg += "🤖 자동매매 시스템 대기 중...\n"
    msg += "`/start` - 모니터링 시작\n"
    msg += "`/stop` - 모니터링 중지\n"
    msg += "`/status` - 현재 상태 확인"
    
    return msg


def main():
    print("="*60)
    print("🌅 장 시작 전 체크리스트")
    print("="*60)
    
    # 1. API 연결 확인
    print("\n1️⃣  API 연결 확인...")
    try:
        client = KISAPIClient()
        print("   ✅ 연결 성공")
    except Exception as e:
        print(f"   ❌ 연결 실패: {e}")
        return
    
    # 2. 계좌 잔고 조회
    print("\n2️⃣  계좌 잔고 조회...")
    balance = client.get_balance()
    if balance:
        print(f"   ✅ 예수금: {balance['예수금']:,}원")
        print(f"   ✅ 총평가: {balance['총평가금액']:,}원")
        print(f"   ✅ 보유: {len(balance['보유종목'])}종목")
    else:
        print("   ❌ 조회 실패")
        return
    
    # 3. 전략 확인
    print("\n3️⃣  오늘의 전략 확인...")
    buy_targets = get_buy_targets()
    sell_targets = get_sell_targets()
    hold_targets = get_hold_targets()
    
    print(f"   📈 매수 대상: {len(buy_targets)}종목")
    for t in buy_targets:
        print(f"      • {t.stock_name}: {t.buy_price_min:,}~{t.buy_price_max:,}원에서 {t.buy_qty}주")
    
    print(f"   📉 매도 대상: {len(sell_targets)}종목")
    for t in sell_targets:
        print(f"      • {t.stock_name}: {t.sell_price_min:,}~{t.sell_price_max:,}원에서 {t.sell_qty}주")
    
    print(f"   📊 보유 유지: {len(hold_targets)}종목")
    
    # 4. 전략 요약 생성
    strategy_summary = "📋 **오늘의 전략**\n\n"
    strategy_summary += f"📈 매수: {len(buy_targets)}종목\n"
    for t in buy_targets:
        strategy_summary += f"• {t.stock_name}: {t.buy_price_min:,}~{t.buy_price_max:,}원\n"
    strategy_summary += f"\n📉 매도: {len(sell_targets)}종목\n"
    for t in sell_targets:
        strategy_summary += f"• {t.stock_name}: {t.sell_price_min:,}~{t.sell_price_max:,}원"
        if t == sell_targets[-1]:
            strategy_summary += ""
        else:
            strategy_summary += "\n"
    
    # 5. 텔레그램 메시지 생성
    print("\n4️⃣  텔레그램 알림 준비...")
    telegram_msg = format_telegram_message(balance, strategy_summary)
    
    # 메시지 저장
    msg_path = "/Users/master/.openclaw/workspace/kis-trading-bot/morning-report.txt"
    with open(msg_path, 'w', encoding='utf-8') as f:
        f.write(telegram_msg)
    print(f"   ✅ 메시지 저장: {msg_path}")
    
    # 6. 완료
    print("\n" + "="*60)
    print("✅ 사전 체크 완료!")
    print("="*60)
    print("\n📱 텔레그램 메시지:")
    print("-"*60)
    print(telegram_msg)
    print("-"*60)


if __name__ == "__main__":
    main()
