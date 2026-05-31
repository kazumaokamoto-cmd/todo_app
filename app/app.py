#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template, request, redirect
from . import func



#Flaskオブジェクトの生成
app = Flask(__name__)


@app.route("/")
def index():
    todos = func.load_csv()
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

    
    todos = [t for t in todos if not t.get("is_done")]
    todos = func.calc_days_left(todos)

    A = [t for t in todos if t.get("category") == "A"]
    B = [t for t in todos if t.get("category") == "B"]
    C = [t for t in todos if t.get("category") == "C"]

    
    return render_template("index.html", A=A, B=B, C=C)


@app.route('/add/<category>', methods=['POST'])    
def add(category):
    #htmlから情報をとってきた
    title = request.form['title']
    deadline = request.form.get('deadline')
    #csvに追加
    func.save_csv({'title':title, 'category':category, 'deadline':deadline, 'is_done':False})
    print('csvを保存しました')


    return redirect('/')

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    func.complete_todo(todo_id)
    return redirect('/')