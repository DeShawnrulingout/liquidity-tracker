"""SQLite 데이터베이스 관리"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DATABASE_PATH", "/app/data/liquidity.db")

def init_db():
    """데이터베이스 및 테이블 초기화"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Fed 유동성 데이터
    c.execute('''CREATE TABLE IF NOT EXISTS fed_liquidity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        walcl REAL,
        tga REAL,
        rrp REAL,
        net_liquidity REAL,
        created_at TEXT
    )''')
    
    # 스테이블코인 데이터
    c.execute('''CREATE TABLE IF NOT EXISTS stablecoins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        symbol TEXT,
        market_cap REAL,
        created_at TEXT,
        UNIQUE(date, symbol)
    )''')
    
    # ETF 플로우 데이터
    c.execute('''CREATE TABLE IF NOT EXISTS etf_flows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        total_flow REAL,
        created_at TEXT
    )''')
    
    # 펀딩 레이트 데이터
    c.execute('''CREATE TABLE IF NOT EXISTS funding_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        exchange TEXT,
        symbol TEXT,
        rate REAL,
        created_at TEXT,
        UNIQUE(timestamp, exchange, symbol)
    )''')
    
    conn.commit()
    conn.close()
    print(f"[DB] Initialized at {DB_PATH}")

def insert_fed_data(date, walcl, tga, rrp):
    """Fed 유동성 데이터 삽입"""
    net_liquidity = walcl - tga - rrp
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO fed_liquidity 
                 (date, walcl, tga, rrp, net_liquidity, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (date, walcl, tga, rrp, net_liquidity, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def insert_stablecoin(date, symbol, market_cap):
    """스테이블코인 데이터 삽입"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO stablecoins 
                 (date, symbol, market_cap, created_at)
                 VALUES (?, ?, ?, ?)''',
              (date, symbol, market_cap, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def insert_etf_flow(date, total_flow):
    """ETF 플로우 데이터 삽입"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO etf_flows 
                 (date, total_flow, created_at)
                 VALUES (?, ?, ?)''',
              (date, total_flow, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def insert_funding_rate(timestamp, exchange, symbol, rate):
    """펀딩 레이트 데이터 삽입"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO funding_rates 
                 (timestamp, exchange, symbol, rate, created_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (timestamp, exchange, symbol, rate, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
