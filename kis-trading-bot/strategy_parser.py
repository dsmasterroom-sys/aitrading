"""
매매 전략 파서
마보스님의 전략 문서를 파싱하여 자동매매 가능한 데이터 구조로 변환
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """매매 행동 타입"""
    BUY = "매수"
    SELL = "매도"
    HOLD = "보유"


@dataclass
class TradingCondition:
    """매매 조건"""
    stock_code: str  # 종목코드
    stock_name: str  # 종목명
    action: ActionType  # 매수/매도/보유
    
    # 현재 상태
    current_price: int  # 현재가
    holding_qty: int  # 보유 수량
    
    # 매수 조건
    buy_price_min: Optional[int] = None  # 매수 최저가
    buy_price_max: Optional[int] = None  # 매수 최고가
    buy_qty: Optional[int] = None  # 매수 수량
    
    # 매도 조건
    sell_price_min: Optional[int] = None  # 매도 최저가
    sell_price_max: Optional[int] = None  # 매도 최고가
    sell_qty: Optional[int] = None  # 매도 수량
    
    # 손절/익절
    stop_loss: Optional[int] = None  # 손절가
    take_profit: Optional[int] = None  # 익절가
    
    # 메타 정보
    position_type: str = "단기"  # 장기/중기/단기
    notes: str = ""  # 메모


# 2026-02-13 매매 전략
STRATEGY_2026_02_13: List[TradingCondition] = [
    # === 매도 전략 ===
    TradingCondition(
        stock_code="454910",
        stock_name="두산로보틱스",
        action=ActionType.SELL,
        current_price=101800,
        holding_qty=7,
        sell_qty=4,  # 3-4주 매도 (절반)
        sell_price_min=100000,  # 시가 ±2%
        sell_price_max=120000,  # 반등 시 추가 정리
        stop_loss=90000,
        position_type="단기",
        notes="테마 과열, 비중 축소. 9만원 이탈 시 전량 정리"
    ),
    
    TradingCondition(
        stock_code="010140",
        stock_name="삼성중공업",
        action=ActionType.SELL,
        current_price=28000,
        holding_qty=1,
        sell_qty=1,  # 전량 매도
        sell_price_min=27000,
        sell_price_max=29000,
        position_type="단기",
        notes="비중 작음, 조선 테마 중복"
    ),
    
    TradingCondition(
        stock_code="042660",
        stock_name="한화오션",
        action=ActionType.SELL,
        current_price=131500,
        holding_qty=9,
        sell_qty=3,  # 일부 매도
        sell_price_min=135000,
        sell_price_max=140000,
        position_type="중기",
        notes="차익 실현. 잔여 6주는 165~170만원 목표"
    ),
    
    TradingCondition(
        stock_code="051910",
        stock_name="LG화학",
        action=ActionType.SELL,
        current_price=336500,
        holding_qty=4,
        sell_qty=1,  # 소폭 매도
        sell_price_min=360000,
        sell_price_max=370000,
        position_type="장기",
        notes="비중 조정. 잔여 3주는 40~42만원 목표"
    ),
    
    # === 매수 전략 ===
    TradingCondition(
        stock_code="005930",
        stock_name="삼성전자",
        action=ActionType.BUY,
        current_price=174300,
        holding_qty=36,
        buy_price_min=170000,
        buy_price_max=172000,
        buy_qty=5,  # 4-5주 추가
        stop_loss=165000,
        take_profit=185000,
        position_type="장기",
        notes="장기 코어. 눌림 시 추가 매수. 단기 목표 18.5~19.5만"
    ),
    
    TradingCondition(
        stock_code="005380",
        stock_name="현대차",
        action=ActionType.BUY,
        current_price=512000,
        holding_qty=2,
        buy_price_min=500000,
        buy_price_max=510000,
        buy_qty=2,  # 1-2주 추가
        stop_loss=480000,
        take_profit=600000,
        position_type="장기",
        notes="장기 코어. 눌림 시 추가. 장기 목표 60~65만"
    ),
    
    TradingCondition(
        stock_code="034020",
        stock_name="두산에너빌리티",
        action=ActionType.BUY,
        current_price=92800,
        holding_qty=15,
        buy_price_min=90000,
        buy_price_max=92000,
        buy_qty=5,  # 3-5주 추가
        stop_loss=85000,
        take_profit=105000,
        position_type="중기",
        notes="중기 모멘텀. 최대 20주까지. 목표 10.5~11만"
    ),
    
    TradingCondition(
        stock_code="082740",
        stock_name="한화엔진",
        action=ActionType.BUY,
        current_price=55000,
        holding_qty=1,
        buy_price_min=53000,
        buy_price_max=54000,
        buy_qty=3,  # 2-3주 추가
        stop_loss=48000,
        take_profit=65000,
        position_type="중기",
        notes="중기 모멘텀. 최대 4주까지. 목표 6.5~7만"
    ),
    
    # === 보유 유지 ===
    TradingCondition(
        stock_code="035420",
        stock_name="NAVER",
        action=ActionType.HOLD,
        current_price=255500,
        holding_qty=5,
        position_type="장기",
        notes="장기 플랫폼 포지션, 모니터링만"
    ),
    
    TradingCondition(
        stock_code="047810",
        stock_name="한국항공우주",
        action=ActionType.HOLD,
        current_price=165500,
        holding_qty=1,
        position_type="중기",
        notes="중기 방산 포지션, 모니터링만"
    ),
]


def get_strategy_by_code(stock_code: str) -> Optional[TradingCondition]:
    """종목코드로 전략 조회"""
    for condition in STRATEGY_2026_02_13:
        if condition.stock_code == stock_code:
            return condition
    return None


def get_buy_targets() -> List[TradingCondition]:
    """매수 대상 종목 리스트"""
    return [c for c in STRATEGY_2026_02_13 if c.action == ActionType.BUY]


def get_sell_targets() -> List[TradingCondition]:
    """매도 대상 종목 리스트"""
    return [c for c in STRATEGY_2026_02_13 if c.action == ActionType.SELL]


def get_hold_targets() -> List[TradingCondition]:
    """보유 유지 종목 리스트"""
    return [c for c in STRATEGY_2026_02_13 if c.action == ActionType.HOLD]


if __name__ == "__main__":
    print("="*60)
    print("📋 2026-02-13 매매 전략 요약")
    print("="*60)
    
    print("\n📉 매도 대상:")
    for c in get_sell_targets():
        print(f"  • {c.stock_name}({c.stock_code}): {c.holding_qty}주 → {c.sell_qty}주 매도")
        if c.sell_price_min and c.sell_price_max:
            print(f"    목표가: {c.sell_price_min:,}~{c.sell_price_max:,}원")
    
    print("\n📈 매수 대상:")
    for c in get_buy_targets():
        print(f"  • {c.stock_name}({c.stock_code}): {c.holding_qty}주 → +{c.buy_qty}주 매수")
        if c.buy_price_min and c.buy_price_max:
            print(f"    목표가: {c.buy_price_min:,}~{c.buy_price_max:,}원")
    
    print("\n📊 보유 유지:")
    for c in get_hold_targets():
        print(f"  • {c.stock_name}({c.stock_code}): {c.holding_qty}주")
    
    print("\n" + "="*60)
