#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template, request, redirect
from . import func
from pathlib import Path


#Flaskオブジェクトの生成
app = Flask(__name__)
normal_db_path = Path('app/db/todo.csv')

@app.route("/")
def index():
    #weekly_todoを割り当てるかを判断する
    #その日の一回目は追加、それ以降は追加しない
    #一番最新のadded_dateとtodayを比較して違うならば追加する

    assign_weekly = func.assign_weekly()    
    print(f'assign_weeklyは{assign_weekly}です')
    if assign_weekly:

        func.weekly_add()
    
    #weekly_todoの追加
   
    todos = func.load_csv(normal_db_path)
    #todosは辞書のリスト 

# todos = [こんなかんじ
#     {
#         "title": "英語勉強",
#         "category": "勉強",
#         "deadline": "2026-06-01",
#         "is_done": False
#     },
#     {
#         "title": "買い物",
#         "category": "生活",
#         "deadline": None,
#         "is_done": False
#     }
# ]

#is_doneがfalseのものだけを抽出して残り日数を計算
    todos = [t for t in todos if not t.get("is_done")]
    todos = func.calc_days_left(todos)

#todoをカテゴリで分けて送る    
    A = [t for t in todos if t.get("category") == "個人用"]
    B = [t for t in todos if t.get("category") == "課題"]
    C = [t for t in todos if t.get("category") == "ロボコン"]


    return render_template("index.html", A=A, B=B, C=C)


@app.route('/add/<category>', methods=['POST'])    
def add(category):
    #htmlから情報をとってきた
    title = request.form['title']
    deadline = request.form.get('deadline')
    #csvに追加
    func.save_csv({'title':title, 'category':category, 'deadline':deadline, 'is_done':False}, normal_db_path)
    print('csvを保存しました')


    return redirect('/')

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    func.complete_todo(todo_id, normal_db_path)
    return redirect('/')

