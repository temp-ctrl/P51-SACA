import sqlite3
from datetime import datetime

DB_PATH = "saca.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_text TEXT NOT NULL,
            symptoms_detected TEXT NOT NULL,
            severity TEXT NOT NULL,
            severity_sw TEXT NOT NULL,
            reason TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_session(symptom_text: str, symptoms: list, severity: str, severity_sw: str, reason: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (symptom_text, symptoms_detected, severity, severity_sw, reason, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        symptom_text,
        ", ".join(symptoms),
        severity,
        severity_sw,
        reason,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows