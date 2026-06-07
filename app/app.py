# FlaskとRender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, redirect
from . import func
from . import discord_notification

# Flaskオブジェクトの生成
app = Flask(__name__)

# SQLiteデータベースの初期化http://127.0.0.1:5000
func.init_db()

@app.route("/")
def index():
    # weekly_todoを割り当てるかを判断する
    # その日の一回目は追加、それ以降は追加しない
    assign_weekly = func.assign_weekly()
    print(f'assign_weeklyは{assign_weekly}です')
    if assign_weekly:
        func.weekly_add()

    todos = func.load_csv()
    # is_doneがfalseのものだけを抽出して残り日数を計算
    todos = [t for t in todos if not t.get("is_done")]
    todos = func.calc_days_left(todos)

    # todoをカテゴリで分けて送る
    A = [t for t in todos if t.get("category") == "個人用"]
    B = [t for t in todos if t.get("category") == "課題"]
    C = [t for t in todos if t.get("category") == "ロボコン"]

    return render_template("index.html", A=A, B=B, C=C)


@app.route('/add/<category>', methods=['POST'])
def add(category):
    title = request.form['title']
    deadline = request.form.get('deadline')
    func.save_csv({'title': title, 'category': category, 'deadline': deadline, 'is_done': False})
    print('SQLiteに保存しました')
    return redirect('/')

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    func.complete_todo(todo_id)
    return redirect('/')

@app.route('/uncomplete/<int:todo_id>', methods=['POST'])
def uncomplete(todo_id):
    func.uncomplete_todo(todo_id)
    return redirect('/archive')

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    func.delete_todo(todo_id)
    ref = request.referrer or '/'
    return redirect(ref)

@app.route("/archive")
def archive():
    todos = func.load_csv()
    # is_doneがtrueのものだけを抽出
    todos = [t for t in todos if t.get("is_done")]
    todos = func.calc_days_left(todos)

    A = [t for t in todos if t.get("category") == "個人用"]
    B = [t for t in todos if t.get("category") == "課題"]
    C = [t for t in todos if t.get("category") == "ロボコン"]

    return render_template("archive.html", A=A, B=B, C=C)

@app.route("/weekly")
def weekly():
    # SQLiteからweeklyテンプレートを取得
    weekly_todos = func.get_weekly_templates()

    # 0〜6の曜日にグループ化
    days = [[] for _ in range(7)]
    for item in weekly_todos:
        try:
            d = int(item['day_of_week'])
            if 0 <= d < 7:
                days[d].append(item)
        except (ValueError, TypeError):
            continue

    return render_template("weekly.html", days=days)

@app.route('/weekly/add', methods=['POST'])
def weekly_add_route():
    day_of_week = request.form['day_of_week']
    title = request.form['title']
    category = request.form['category']
    func.add_weekly_template(day_of_week, title, category)
    return redirect('/weekly')

@app.route('/weekly/delete', methods=['POST'])
def weekly_delete_route():
    day_of_week = request.form['day_of_week']
    title = request.form['title']
    category = request.form['category']
    func.delete_weekly_template(day_of_week, title, category)
    return redirect('/weekly')

@app.route('notify')
def discord_notification():

    discord_notification.notify_deadline()
