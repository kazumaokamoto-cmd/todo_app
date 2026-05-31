import pandas as pd
from pathlib import Path

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

# add_todo = {'title':'洗濯', 'category':'個人用'}
# save_csv(add_todo)

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
# def complete_todo(id):
#     df = pd.read_csv(db_path)
    
    
#     # is_doneが何番目か調べる。なぜならilocで番号指定しての書き換えをするから
#     # カラムを変更しなければ絶対4なんだけどね
#     # ごみみたいなコードができた。データフレームを辞書にして、その辞書のリストの0番目を取り出すと辞書だから
#     # その辞書をリストにしてインデックスがis_doneになっているインデックスが何なのかを列として指定してる
#     df.iloc[id, list(df.to_dict(orient='records')[0]).index('is_done')] = True

def complete_todo(todo_id):
    
    db_path = Path('app/db/todo.csv')
    df = pd.read_csv(db_path)
    df.loc[df['id'] == todo_id, 'is_done'] = True
    df.to_csv(db_path, index=False)