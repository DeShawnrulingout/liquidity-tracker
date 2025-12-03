"""메인 스케줄러 - 데이터 수집 자동화"""
import os
import sys
import time
import schedule
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 프로젝트 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db
from collectors.fed_collector import collect_fed_data
from collectors.stablecoin_collector import collect_stablecoin_data
from collectors.etf_collector import collect_etf_data
from collectors.funding_collector import collect_funding_rates

def run_all_collectors():
    """모든 컬렉터 실행"""
    print("\n" + "="*50)
    print(f"[SCHEDULER] Running all collectors...")
    print("="*50)
    
    collect_fed_data()
    collect_stablecoin_data()
    collect_etf_data()
    collect_funding_rates()
    
    print("="*50)
    print("[SCHEDULER] Collection complete")
    print("="*50 + "\n")

def main():
    """메인 실행"""
    print("[SCHEDULER] Starting Liquidity Tracker...")
    
    # DB 초기화
    init_db()
    
    # 시작시 즉시 실행
    run_all_collectors()
    
    # 스케줄 설정
    # 매 시간 펀딩 레이트
    schedule.every(1).hours.do(collect_funding_rates)
    
    # 매 4시간 스테이블코인
    schedule.every(4).hours.do(collect_stablecoin_data)
    
    # 매일 09:00 UTC - ETF 플로우
    schedule.every().day.at("09:00").do(collect_etf_data)
    
    # 매일 12:00 UTC - Fed 데이터
    schedule.every().day.at("12:00").do(collect_fed_data)
    
    print("[SCHEDULER] Schedule configured:")
    print("  - Funding rates: every 1 hour")
    print("  - Stablecoins: every 4 hours")
    print("  - ETF flows: daily at 09:00 UTC")
    print("  - Fed data: daily at 12:00 UTC")
    print("[SCHEDULER] Waiting for scheduled jobs...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
