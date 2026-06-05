import sqlite3
import csv
from pathlib import Path
from datetime import date, datetime, timedelta

day_of_week = ['月', '火', '水', '木', '金', '土', '日']

DB_PATH = Path('app/db/todo.db')
last_run_path = Path('app/db/last_weekly_run.txt')
WEEKLY_CSV_PATH = Path('app/db/weekly_todo.csv')


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """データベースとテーブルを初期化する"""
    conn = get_conn()
    c = conn.cursor()

    # todos テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            deadline TEXT,
            is_done INTEGER NOT NULL DEFAULT 0,
            added_date TEXT
        )
    ''')

    # weekly_templates テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS weekly_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_of_week INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT
        )
    ''')

    # weekly_todo.csv が存在すれば移行してCSVを削除する
    if WEEKLY_CSV_PATH.is_file():
        print('weekly_todo.csvをSQLiteに移行します...')
        migrated = []
        try:
            with open(WEEKLY_CSV_PATH, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        migrated.append((int(float(row['day_of_week'])), row['title'], row['category']))
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            print(f'weekly_todo.csv の読み込みに失敗しました: {e}')

        if migrated:
            c.executemany(
                'INSERT INTO weekly_templates (day_of_week, title, category) VALUES (?, ?, ?)',
                migrated
            )
            print(f'{len(migrated)}件のweeklyテンプレートを移行しました')

        WEEKLY_CSV_PATH.unlink()
        print('weekly_todo.csvを削除しました')

    # weekly_templates が空かつCSVも存在しない場合はデフォルト値を挿入
    else:
        c.execute('SELECT COUNT(*) FROM weekly_templates')
        if c.fetchone()[0] == 0:
            default_weekly = [
                (0, '現代文化論', '課題'),
                (1, '現代文化論', '課題'),
                (1, '情報学入門', '課題'),
                (2, '制御班', 'ロボコン'),
            ]
            c.executemany(
                'INSERT INTO weekly_templates (day_of_week, title, category) VALUES (?, ?, ?)',
                default_weekly
            )

    conn.commit()
    conn.close()
    add_notified_column()
    print('SQLiteデータベースを初期化しました')


'''
save_todo はtodoをSQLiteに追加する関数
add_todoとはtitle, category, deadline, is_doneからなる辞書
'''
def save_csv(add_todo):
    today = date.today().isoformat()
    conn = get_conn()
    conn.execute(
        'INSERT INTO todos (title, category, deadline, is_done, added_date) VALUES (?, ?, ?, ?, ?)',
        (
            add_todo.get('title'),
            add_todo.get('category'),
            add_todo.get('deadline') or None,
            1 if add_todo.get('is_done') else 0,
            today,
        )
    )
    conn.commit()
    conn.close()


'''
load_todos はSQLiteからすべてのtodoを辞書のリストで返す関数
'''
def load_csv():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d['is_done'] = bool(d['is_done'])
        result.append(d)
    return result


'''
complete_todo は is_done を True にする関数
'''
def complete_todo(todo_id):
    conn = get_conn()
    conn.execute('UPDATE todos SET is_done = 1 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()


'''
uncomplete_todo は is_done を False に戻す関数
'''
def uncomplete_todo(todo_id):
    conn = get_conn()
    conn.execute('UPDATE todos SET is_done = 0 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()


'''
delete_todo は指定IDのtodoを削除する関数
'''
def delete_todo(todo_id):
    conn = get_conn()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()


'''
calc_days_left は今日とtodoの期限を比較してdays_leftを返す関数
'''
def calc_days_left(todos):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    for t in todos:
        if t.get('deadline'):
            try:
                d = datetime.strptime(t['deadline'], '%Y-%m-%d').date()
                t['days_left'] = (d - today).days

                if d == today:
                    t['deadline_display'] = '今日'
                elif d == tomorrow:
                    t['deadline_display'] = '明日'
                else:
                    t['deadline_display'] = f'{d.month}月{d.day}日'
            except Exception:
                t['days_left'] = None
        else:
            t['days_left'] = None
    return todos


'''
get_weekly_templates はweekly_templatesテーブルの全行を返す関数
'''
def get_weekly_templates():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM weekly_templates ORDER BY day_of_week').fetchall()
    conn.close()
    return [dict(row) for row in rows]


'''
weekly_add は今日の曜日のテンプレートをtodosに追加する関数
deadlineは一週間後になる
'''
def weekly_add():
    today = date.today()
    current_weekday = today.weekday()
    print(f'今日は{day_of_week[current_weekday]}曜日です')

    deadline = (today + timedelta(days=7)).strftime('%Y-%m-%d')

    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM weekly_templates WHERE day_of_week = ?', (current_weekday,)
    ).fetchall()
    conn.close()

    for row in rows:
        new_todo = {
            'title': row['title'],
            'category': row['category'],
            'deadline': deadline,
            'is_done': False,
        }
        save_csv(new_todo)
        print(f"定期タスクを追加しました: {row['title']}")

    # 実行日を記録
    try:
        last_run_path.parent.mkdir(parents=True, exist_ok=True)
        last_run_path.write_text(today.isoformat(), encoding='utf-8')
    except Exception as e:
        print(f'実行ログファイルの更新に失敗しました: {e}')


def assign_weekly():
    today = date.today()
    if not last_run_path.is_file():
        return True
    try:
        last_run_str = last_run_path.read_text(encoding='utf-8').strip()
        last_run_date = datetime.strptime(last_run_str, '%Y-%m-%d').date()
        if last_run_date == today:
            return False
    except Exception as e:
        print(f'実行ログファイルの読み込みに失敗しました: {e}')
        return True
    return True


def add_weekly_template(day_of_week, title, category):
    conn = get_conn()
    conn.execute(
        'INSERT INTO weekly_templates (day_of_week, title, category) VALUES (?, ?, ?)',
        (int(day_of_week), title, category)
    )
    conn.commit()
    conn.close()

    # 追加した曜日が今日と一致する場合は即座にtodosにも追加する
    today = date.today()
    if int(day_of_week) == today.weekday():
        deadline = (today + timedelta(days=7)).strftime('%Y-%m-%d')
        save_csv({
            'title': title,
            'category': category,
            'deadline': deadline,
            'is_done': False,
        })
        print(f'今日の曜日と一致するため、todoにも即座に追加しました: {title}')


def delete_weekly_template(day_of_week, title, category):
    conn = get_conn()
    conn.execute(
        'DELETE FROM weekly_templates WHERE day_of_week = ? AND title = ? AND category = ?',
        (int(day_of_week), title.strip(), category.strip())
    )
    conn.commit()
    conn.close()

def add_notified_column():
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute("ALTER TABLE todos ADD COLUMN notified INTEGER DEFAULT 0")
        print('notifiedカラムを追加しました')
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()