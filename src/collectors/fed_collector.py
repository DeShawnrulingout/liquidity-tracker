"""FRED API를 통한 Fed 유동성 데이터 수집"""
import os
from datetime import datetime, timedelta
from fredapi import Fred
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import insert_fed_data

FRED_API_KEY = os.getenv("FRED_API_KEY")

# FRED 시리즈 ID
SERIES = {
    "WALCL": "WALCL",      # Fed Balance Sheet (주간)
    "TGA": "WTREGEN",      # Treasury General Account (주간)
    "RRP": "RRPONTSYD"     # Reverse Repo (일간)
}

def collect_fed_data():
    """최근 Fed 유동성 데이터 수집"""
    if not FRED_API_KEY:
        print("[FED] ERROR: FRED_API_KEY not set")
        return
    
    fred = Fred(api_key=FRED_API_KEY)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        walcl = fred.get_series(SERIES["WALCL"], start_date, end_date)
        tga = fred.get_series(SERIES["TGA"], start_date, end_date)
        rrp = fred.get_series(SERIES["RRP"], start_date, end_date)
        
        # 가장 최근 공통 날짜 찾기
        latest_walcl = walcl.dropna().iloc[-1] if len(walcl.dropna()) > 0 else None
        latest_tga = tga.dropna().iloc[-1] if len(tga.dropna()) > 0 else None
        latest_rrp = rrp.dropna().iloc[-1] if len(rrp.dropna()) > 0 else None
        
        if all([latest_walcl, latest_tga, latest_rrp]):
            date = walcl.dropna().index[-1].strftime("%Y-%m-%d")
            insert_fed_data(date, float(latest_walcl), float(latest_tga), float(latest_rrp))
            net_liq = latest_walcl - latest_tga - latest_rrp
            print(f"[FED] {date}: Net Liquidity = ${net_liq/1e6:.2f}T")
        else:
            print("[FED] Incomplete data")
            
    except Exception as e:
        print(f"[FED] ERROR: {e}")

if __name__ == "__main__":
    collect_fed_data()
