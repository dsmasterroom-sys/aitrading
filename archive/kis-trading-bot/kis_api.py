"""
한국투자증권 API 클라이언트
모의투자 전용
"""
import requests
import json
import logging
import time
from typing import Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KISAPIClient:
    """한국투자증권 API 클라이언트"""
    
    # 모의투자 URL
    BASE_URL = "https://openapivts.koreainvestment.com:29443"
    
    def __init__(self, config_path: str = "/Users/master/.openclaw/workspace/kis-demo-config.json"):
        """초기화"""
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.app_key = config.get('KIS_KEY')
        self.app_secret = config.get('KIS_SECRET')
        raw_account = str(config.get('계좌번호', '')).strip()
        if '-' in raw_account:
            self.account_no = raw_account.split('-')[0]
            self.account_code = raw_account.split('-')[1]
        else:
            self.account_no = raw_account
            self.account_code = '01'
        
        logger.info(f"✅ 설정 로드 완료")
        logger.info(f"   계좌: {self.account_no}-{self.account_code}")
        
        self.access_token = None
        self.request_retries = 3
        self.request_timeout = 8
        self._get_access_token()
    
    def _get_access_token(self) -> bool:
        """접근 토큰 발급"""
        url = f"{self.BASE_URL}/oauth2/tokenP"
        
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            res = self._request("POST", url, headers=headers, json_body=body)
            if res.status_code == 200:
                data = res.json()
                self.access_token = data.get('access_token')
                logger.info("✅ 토큰 발급 성공")
                return True
            else:
                logger.error(f"❌ 토큰 발급 실패: {res.status_code} - {res.text}")
                return False
        except Exception as e:
            logger.error(f"❌ 토큰 발급 오류: {e}")
            return False
    
    def _get_headers(self, tr_id: str, tr_cont: str = "") -> Dict:
        """공통 헤더 생성"""
        return {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
            "custtype": "P",
            "tr_cont": tr_cont
        }

    def _request(self, method: str, url: str, *, headers: Dict = None, params: Dict = None, json_body: Dict = None):
        """공통 요청 래퍼: 5xx/타임아웃 재시도 + 401 토큰 재발급 1회"""
        refreshed = False
        for attempt in range(1, self.request_retries + 1):
            try:
                res = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_body,
                    timeout=self.request_timeout,
                )

                if res.status_code == 401 and not refreshed and headers and 'authorization' in headers:
                    logger.warning("⚠️ 401 응답 - 토큰 재발급 후 재시도")
                    if self._get_access_token():
                        refreshed = True
                        if headers and 'authorization' in headers:
                            headers = dict(headers)
                            headers['authorization'] = f"Bearer {self.access_token}"
                        continue

                if res.status_code >= 500 and attempt < self.request_retries:
                    wait = 0.7 * attempt
                    logger.warning(f"⚠️ HTTP {res.status_code} 재시도({attempt}/{self.request_retries}) {wait:.1f}s")
                    time.sleep(wait)
                    continue

                return res
            except requests.RequestException as e:
                if attempt >= self.request_retries:
                    raise
                wait = 0.7 * attempt
                logger.warning(f"⚠️ 요청 오류 재시도({attempt}/{self.request_retries}): {e}")
                time.sleep(wait)

        return None
    
    def get_current_price(self, stock_code: str) -> Optional[Dict]:
        """현재가 조회"""
        url = f"{self.BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"

        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code
        }

        try:
            res = self._request("GET", url, headers=self._get_headers(tr_id), params=params)
            if res.status_code == 200:
                data = res.json()
                if data.get('rt_cd') == '0':
                    output = data.get('output', {})
                    result = {
                        '종목명': output.get('hts_kor_isnm'),
                        '현재가': int(output.get('stck_prpr', 0)),
                        '전일대비': int(output.get('prdy_vrss', 0)),
                        '등락률': float(output.get('prdy_ctrt', 0)),
                        '거래량': int(output.get('acml_vol', 0)),
                        '시가': int(output.get('stck_oprc', 0)),
                        '고가': int(output.get('stck_hgpr', 0)),
                        '저가': int(output.get('stck_lwpr', 0))
                    }
                    logger.info(f"✅ {result['종목명']} 현재가: {result['현재가']:,}원")
                    return result
                else:
                    logger.error(f"❌ API 오류: {data.get('msg1')}")
                    return None
            else:
                logger.error(f"❌ HTTP 오류: {res.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ 현재가 조회 실패: {e}")
            return None
    
    def buy_order(self, stock_code: str, quantity: int, price: int = 0, order_type: str = "00") -> bool:
        """매수 주문
        
        Args:
            stock_code: 종목코드
            quantity: 수량
            price: 가격 (0이면 시장가)
            order_type: "00"=지정가, "01"=시장가
            
        Returns:
            성공 여부
        """
        url = f"{self.BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"
        tr_id = "VTTC0802U"  # 모의투자 매수

        # 시장가 자동 전환
        if price == 0:
            order_type = "01"

        body = {
            "CANO": self.account_no,
            "ACNT_PRDT_CD": self.account_code,
            "PDNO": stock_code,
            "ORD_DVSN": order_type,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price) if price > 0 else "0"
        }

        try:
            res = self._request("POST", url, headers=self._get_headers(tr_id), json_body=body)
            if res.status_code == 200:
                data = res.json()
                if data.get('rt_cd') == '0':
                    logger.info(f"✅ 매수 주문 성공: {stock_code} {quantity}주")
                    logger.info(f"   주문번호: {data.get('output', {}).get('ODNO')}")
                    return True
                else:
                    logger.error(f"❌ 매수 실패: {data.get('msg1')}")
                    return False
            else:
                logger.error(f"❌ HTTP 오류: {res.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ 매수 주문 오류: {e}")
            return False
    
    def sell_order(self, stock_code: str, quantity: int, price: int = 0, order_type: str = "00") -> bool:
        """매도 주문
        
        Args:
            stock_code: 종목코드
            quantity: 수량
            price: 가격 (0이면 시장가)
            order_type: "00"=지정가, "01"=시장가
            
        Returns:
            성공 여부
        """
        url = f"{self.BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"
        tr_id = "VTTC0801U"  # 모의투자 매도

        # 시장가 자동 전환
        if price == 0:
            order_type = "01"

        body = {
            "CANO": self.account_no,
            "ACNT_PRDT_CD": self.account_code,
            "PDNO": stock_code,
            "ORD_DVSN": order_type,
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price) if price > 0 else "0"
        }

        try:
            res = self._request("POST", url, headers=self._get_headers(tr_id), json_body=body)
            if res.status_code == 200:
                data = res.json()
                if data.get('rt_cd') == '0':
                    logger.info(f"✅ 매도 주문 성공: {stock_code} {quantity}주")
                    logger.info(f"   주문번호: {data.get('output', {}).get('ODNO')}")
                    return True
                else:
                    logger.error(f"❌ 매도 실패: {data.get('msg1')}")
                    return False
            else:
                logger.error(f"❌ HTTP 오류: {res.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ 매도 주문 오류: {e}")
            return False
    
    def get_balance(self) -> Optional[Dict]:
        """계좌 잔고 조회
        
        Returns:
            잔고 정보 딕셔너리 또는 None
        """
        url = f"{self.BASE_URL}/uapi/domestic-stock/v1/trading/inquire-balance"
        tr_id = "VTTC8434R"  # 모의투자 잔고조회
        
        params = {
            "CANO": self.account_no,
            "ACNT_PRDT_CD": self.account_code,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "00",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        
        try:
            res = self._request("GET", url, headers=self._get_headers(tr_id), params=params)
            if res.status_code == 200:
                data = res.json()
                if data.get('rt_cd') == '0':
                    output1 = data.get('output1', [])
                    output2 = data.get('output2', [])
                    
                    result = {
                        '보유종목': [],
                        '총평가금액': int(float(output2[0].get('tot_evlu_amt', 0))) if output2 else 0,
                        '예수금': int(float(output2[0].get('dnca_tot_amt', 0))) if output2 else 0,
                        '총손익': int(float(output2[0].get('evlu_pfls_smtl_amt', 0))) if output2 else 0
                    }
                    
                    for stock in output1:
                        if int(float(stock.get('hldg_qty', 0))) > 0:
                            result['보유종목'].append({
                                '종목명': stock.get('prdt_name'),
                                '종목코드': stock.get('pdno'),
                                '보유수량': int(float(stock.get('hldg_qty', 0))),
                                '평균매입가': int(float(stock.get('pchs_avg_pric', 0))),
                                '현재가': int(float(stock.get('prpr', 0))),
                                '평가금액': int(float(stock.get('evlu_amt', 0))),
                                '손익': int(float(stock.get('evlu_pfls_amt', 0))),
                                '수익률': float(stock.get('evlu_pfls_rt', 0))
                            })
                    
                    logger.info(f"✅ 잔고 조회 성공: 보유 {len(result['보유종목'])}종목")
                    return result
                else:
                    logger.error(f"❌ API 오류: {data.get('msg1')}")
                    return None
            else:
                logger.error(f"❌ HTTP 오류: {res.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ 잔고 조회 실패: {e}")
            return None


if __name__ == "__main__":
    # 테스트 코드
    client = KISAPIClient()
    
    print("\n" + "="*60)
    print("🧪 한국투자증권 API 테스트")
    print("="*60)
    
    # 1. 현재가 조회
    print("\n1️⃣ 삼성전자 현재가 조회")
    price_info = client.get_current_price("005930")
    if price_info:
        print(f"   {price_info['종목명']}: {price_info['현재가']:,}원 ({price_info['등락률']:+.2f}%)")
    
    # 2. 잔고 조회
    print("\n2️⃣ 계좌 잔고 조회")
    balance = client.get_balance()
    if balance:
        print(f"   예수금: {balance['예수금']:,}원")
        print(f"   총평가: {balance['총평가금액']:,}원")
        print(f"   총손익: {balance['총손익']:+,}원")
        if balance['보유종목']:
            print(f"   보유종목: {len(balance['보유종목'])}개")
            for stock in balance['보유종목']:
                print(f"     - {stock['종목명']}: {stock['보유수량']}주 ({stock['수익률']:+.2f}%)")
    
    print("\n" + "="*60)
    print("✅ 테스트 완료!")
    print("="*60)
