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

    for i in range(len(todos)):
        if todos[i]['is_done'] == True:
            del todos[i]
        else:
            pass
    
    return render_template('index.html', todos=todos)
    

@app.route('/add', methods=['POST'])    
def add():
    #htmlから情報をとってきた
    new_title = request.form['new_title']
    new_category = request.form['new_category']
    new_deadline = request.form.get('new_deadline')
    #csvに追加
    func.save_csv({'title':new_title, 'category':new_category, 'deadline':new_deadline, 'is_done':False})
    print('csvを保存しました')


    return redirect('/')

@app.route('/complete/<int:index>', methods=['POST'])
def complete(id):
    func.complete_todo(id)
    return redirect('/')