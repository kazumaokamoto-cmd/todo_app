import pandas as pd
from pathlib import Path
from datetime import date, datetime
'''
save_csv
はadd_todoをcsvファイルに追記する関数
add_todoとはid, title, category, deadline, is_doneからなる辞書
 
'''
def save_csv(add_todo):
    
    db_path = Path('app/db/todo.csv')
    if db_path.is_file():
        
        print('csvファイルが見つかりました')
        #csvファイルがあってデータがないなら新しいidをつくる(id=1)
        df = pd.read_csv(db_path)
        if len(df) == 0:
            new_id = 0
        else:
            new_id = df['id'].max() + 1
        
        add_todo['id'] = new_id
        df = pd.concat([df, pd.DataFrame([add_todo])])
        df.to_csv(db_path, index=False)
    else:
        print('csvファイルが見つかりません。csvを作成します')
        
        add_todo['id'] = 0
        df = pd.DataFrame([add_todo])
        df.to_csv(db_path, index=False)


'''
load_csvはcsvファイルが存在するか確かめてからcsvのデータを辞書のリストに変換する関数
トップページをつくるために呼び出される
'''
def load_csv():
    
    db_path = Path('app/db/todo.csv')
    if db_path.is_file():
        df = pd.read_csv(db_path)
        return df.to_dict(orient='records')
    else:
        return []
        print('csvファイルが見つかりません')


'''
complete_todoはtodo_doneをfalseからtrueにする関数
todoが完了ときに呼び出される
'''

def complete_todo(todo_id):
    
    db_path = Path('app/db/todo.csv')
    df = pd.read_csv(db_path)
    df.loc[df['id'] == todo_id, 'is_done'] = True
    df.to_csv(db_path, index=False)


'''
calc_days_leftは今日とtodoの期限を比較してdays_leftを返す関数
'''

def calc_days_left(todos):
    today = date.today()

    for t in todos:
        if t.get('deadline'):
            try:
                d = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
                t['days_left'] = (d - today).days
            except:
                t['days_left'] = None
        else:
            t['days_left'] = None
    return todos