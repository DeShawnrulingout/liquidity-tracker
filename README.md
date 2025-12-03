# Liquidity Tracker 🔍

크립토 시장 유동성 모니터링 자동화 시스템

## 수집 데이터

| 지표 | 소스 | 주기 |
|------|------|------|
| Fed Net Liquidity (WALCL - TGA - RRP) | FRED API | 일간 |
| 스테이블코인 시총 | DefiLlama | 4시간 |
| BTC ETF 플로우 | Farside | 일간 |
| 펀딩 레이트 | Binance/Bybit | 1시간 |

## 환경변수

```
FRED_API_KEY=your_key_here
DATABASE_PATH=/app/data/liquidity.db  # Railway용
```

## 로컬 실행

```bash
pip install -r requirements.txt
python src/scheduler.py
```

## Railway 배포

1. GitHub 연결
2. 환경변수 설정 (FRED_API_KEY)
3. Volume 마운트: `data` → `/app/data`
4. Deploy!

## Phase 1 완료 ✅

- [x] Fed 유동성 수집
- [x] 스테이블코인 수집
- [x] ETF 플로우 스크래핑
- [x] 펀딩 레이트 수집
- [x] SQLite 저장
- [x] 스케줄러

## 다음 단계

- [ ] 텔레그램 알림
- [ ] Z-score 신호 생성
- [ ] 대시보드
