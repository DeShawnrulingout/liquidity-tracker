"""DefiLlama API를 통한 스테이블코인 데이터 수집"""
import os
import requests
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import insert_stablecoin

DEFILLAMA_URL = "https://stablecoins.llama.fi/stablecoins?includePrices=true"

# 추적할 주요 스테이블코인
TARGET_STABLES = ["USDT", "USDC", "DAI", "BUSD", "TUSD", "FRAX"]

def collect_stablecoin_data():
    """스테이블코인 시총 데이터 수집"""
    try:
        response = requests.get(DEFILLAMA_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        total_mcap = 0
        
        for coin in data.get("peggedAssets", []):
            symbol = coin.get("symbol", "")
            if symbol in TARGET_STABLES:
                mcap = coin.get("circulating", {}).get("peggedUSD", 0)
                if mcap:
                    insert_stablecoin(today, symbol, mcap)
                    total_mcap += mcap
                    print(f"[STABLE] {symbol}: ${mcap/1e9:.2f}B")
        
        print(f"[STABLE] Total tracked: ${total_mcap/1e9:.2f}B")
        
    except Exception as e:
        print(f"[STABLE] ERROR: {e}")

if __name__ == "__main__":
    collect_stablecoin_data()
