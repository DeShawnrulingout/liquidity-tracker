"""Farside Investors에서 BTC ETF 플로우 데이터 수집"""
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import insert_etf_flow

FARSIDE_URL = "https://farside.co.uk/btc/"

def collect_etf_data():
    """BTC ETF 플로우 데이터 스크래핑"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(FARSIDE_URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # 테이블에서 최신 데이터 추출 시도
        tables = soup.find_all("table")
        if tables:
            # Farside 페이지 구조에 따라 파싱 로직 조정 필요
            # 현재는 기본 구조만 설정
            print("[ETF] Page fetched, parsing may need adjustment")
            
            # 임시: 수동 파싱이 필요한 경우 로그
            today = datetime.utcnow().strftime("%Y-%m-%d")
            print(f"[ETF] Check {FARSIDE_URL} for {today} data")
        else:
            print("[ETF] No tables found on page")
            
    except Exception as e:
        print(f"[ETF] ERROR: {e}")

if __name__ == "__main__":
    collect_etf_data()
