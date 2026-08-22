import sqlite3
from typing import Dict, Any, List
from app.config import settings

def init_db():
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escalations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            reason TEXT NOT NULL,
            urgency TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'ESCALATED'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            action TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def record_escalation(ticket_id: str, reason: str, urgency: str, created_by: str) -> Dict[str, Any]:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO escalations (ticket_id, reason, urgency, created_by) VALUES (?, ?, ?, ?)",
        (ticket_id, reason, urgency, created_by)
    )
    esc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "escalation_id": esc_id,
        "ticket_id": ticket_id,
        "reason": reason,
        "urgency": urgency,
        "status": "ESCALATED"
    }

def get_escalations() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM escalations ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]