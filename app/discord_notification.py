import requests
from datetime import datetime, timedelta, date
from . func import get_conn
from pathlib import Path
import os


url = os.environ.get('DISCORD_WEBHOOK_URL')

def send_discord(message):
    data = {
        "content": message
    }
    requests.post(url, json=data)

def notify_deadline():
    conn = get_conn()
    cursor = conn.cursor()

    today = date.today()
    tomorrow = today + timedelta(days=1)
    cursor.execute("""
    SELECT id, title, deadline
    FROM todos
    WHERE is_done = 0
    AND deadline IS NOT NULL
    AND notified = 0
    """)

    rows = cursor.fetchall()

    for row in rows:
        d = datetime.strptime(row["deadline"], "%Y-%m-%d").date()

        if d == today or d == tomorrow:
            label = "今日" if d == today else "明日"
            message = f'{label}が期限のタスク\n・{row['title']}({row['deadline']})'
            send_discord(message)
            
            cursor.execute(
                "UPDATE todos SET notified = 1 WHERE id = ?",
                (row['id'],)
            )

            conn.commit()
            conn.close()