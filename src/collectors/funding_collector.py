"""ccxt를 통한 펀딩 레이트 데이터 수집"""
import os
import ccxt
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import insert_funding_rate

# 추적할 거래소 및 심볼
EXCHANGES = {
    "binance": ["BTC/USDT:USDT", "ETH/USDT:USDT"],
    "bybit": ["BTC/USDT:USDT", "ETH/USDT:USDT"]
}

def collect_funding_rates():
    """거래소 펀딩 레이트 수집"""
    for exchange_id, symbols in EXCHANGES.items():
        try:
            exchange_class = getattr(ccxt, exchange_id)
            exchange = exchange_class({"enableRateLimit": True})
            
            for symbol in symbols:
                try:
                    # 펀딩 레이트 조회
                    funding = exchange.fetch_funding_rate(symbol)
                    rate = funding.get("fundingRate", 0)
                    timestamp = datetime.utcnow().isoformat()
                    
                    insert_funding_rate(timestamp, exchange_id, symbol, rate)
                    print(f"[FUNDING] {exchange_id} {symbol}: {rate*100:.4f}%")
                    
                except Exception as e:
                    print(f"[FUNDING] {exchange_id} {symbol} ERROR: {e}")
                    
        except Exception as e:
            print(f"[FUNDING] {exchange_id} ERROR: {e}")

if __name__ == "__main__":
    collect_funding_rates()
