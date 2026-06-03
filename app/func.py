import pandas as pd
from pathlib import Path
from datetime import date, datetime, timedelta

day_of_week = ['月', '火', '水', '木', '金', '土', '日']
normal_db_path = Path('app/db/todo.csv')
weekly_db_path = Path('app/db/weekly_todo.csv')
today = date.today()
tomorrow = today + timedelta(days=1)
'''
save_csv
はadd_todoをcsvファイルに追記する関数
add_todoとはid, title, category, deadline, is_doneからなる辞書
 
'''
def save_csv(add_todo, normal_db_path):
    
    if normal_db_path.is_file():
        
        print('csvファイルが見つかりました')
        #csvファイルがあってデータがないなら新しいidをつくる(id=1)
        df = pd.read_csv(normal_db_path)
        if len(df) == 0:
            new_id = 0
        else:
            new_id = df['id'].max() + 1
        
        add_todo['id'] = new_id
        add_todo['added_date'] = today
        df = pd.concat([df, pd.DataFrame([add_todo])])
        df.to_csv(normal_db_path, index=False)
    else:
        print('csvファイルが見つかりません。csvを作成します')
        
        add_todo['id'] = 0
        add_todo['added_date'] = today
        df = pd.DataFrame([add_todo])
        df.to_csv(normal_db_path, index=False)


'''
load_csvはcsvファイルが存在するか確かめてからcsvのデータを辞書のリストに変換する関数
トップページをつくるために呼び出される
'''
def load_csv(normal_db_path):
    
    if normal_db_path.is_file():
        df = pd.read_csv(normal_db_path)
        return df.to_dict(orient='records')
    else:
        return []
        print('csvファイルが見つかりません')


'''
complete_todoはtodo_doneをfalseからtrueにする関数
todoが完了ときに呼び出される
'''

def complete_todo(todo_id, normal_db_path):
    
    df = pd.read_csv(normal_db_path)
    df.loc[df['id'] == todo_id, 'is_done'] = True
    df.to_csv(normal_db_path, index=False)


'''
calc_days_leftは今日とtodoの期限を比較してdays_leftを返す関数
'''

def calc_days_left(todos):
    

    for t in todos:
        if t.get('deadline'):
            try:
                d = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
                t['days_left'] = (d - today).days

                if d == today:
                    t["deadline_display"] = '今日'
                    
                elif d == tomorrow:
                    t['deadline_display'] = '明日'
                   
                else:
                    t['deadline_display'] = t['deadline']
                    

            except:
                t['days_left'] = None
        else:
            t['days_left'] = None
    return todos


'''
weekly_addは今日の曜日と同じ曜日のタスクをすべて追加する関数
deadlineは一週間後になる
'''

def weekly_add():
    deadline = today + timedelta(7)
    #曜日の番号=today.weekday()
    weekly_todo = [#曜日のリスト
        [#月曜日のリスト
            {
                'title':'現代文化論',
                'category':'課題',
                'deadline':None,
                'is_done':False,
            }
        ],
        [#火曜日のリスト
            {
                'title':'現代文化論',
                'category':'課題',
                'deadline':None,
                'is_done':False,
            },
            {
                'title':'情報学入門',
                'category':'課題',
                'deadline':None,
                'is_done':False,
            }
        ],
        [#水曜日のリスト
            {
                'title':'制御班',
                'category':'ロボコン',
                'deadline':None,
                'is_done':False,
            }
        ]
    
        ]
    print(f'今日は{day_of_week[today.weekday()]}曜日です')    
        
    #deadlineの設定したあとに保存する。この流れをforで回す
    
    for i in weekly_todo[today.weekday()]:
        i['deadline'] = deadline
        save_csv(i, normal_db_path)       
        print('１つ保存した')

def assign_weekly():
    assign_weekly = True
    if normal_db_path.is_file():
        df = pd.read_csv(normal_db_path)
        last_row = df.iloc[-1]
        added_date = pd.to_datetime(last_row['added_date'])
        print(today)
        print(added_date)
        inttoday = today.year * 10000 + today.month * 100 + today.day
        print(inttoday)
        intadded_date = added_date.year * 10000 + added_date.month * 100 + added_date.day
        print(intadded_date)
        
        
        
        if inttoday == intadded_date:
            assign_weekly = False 
            return assign_weekly
    else:
        print('csvファイルが見つかりません')
        assign_weekly = False
        return assign_weekly
    