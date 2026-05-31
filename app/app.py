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
    # print('todosの要素数は')
    # print(len(todos))
    # del_id_list = []    
    # for i in range(len(todos) - 1):
    #     print(f'{i}番目の判定を開始')
    #     if todos[i]['is_done'] == True:
    #         print(f'{i}番目はis_done')
    #         del_id_list.append(i)

    #     else:
    #         print(f'{i}番目はis_doneでない')
    # print(todos)
    # print(del_id_list) 
    
    # for i in range(len(del_id_list) - 1): 
    #     del todos[i]

    # print(todos)


    todos = [i for i in todos if not i.get('is_done')]
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

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    func.complete_todo(todo_id)
    return redirect('/')