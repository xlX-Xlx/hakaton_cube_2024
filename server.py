from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from algGenerate import Simple, Normal
from oge_ege_tasks.ege_oge_tasks import GIATasks
import os
import sqlite3
import random
import json
import requests
import secrets
import string
import html

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_ID = '623a52b24eba4a6888d3b87d0b2904e2'
CLIENT_SECRET = '453cfc6b79fe4b2084d803061731ab12'
TOKEN_URL = 'https://oauth.yandex.ru/token'
AUTH_URL = 'https://oauth.yandex.ru/authorize'
REDIRECT_URI = 'http://127.0.0.1:8000/index'


conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  rating INTEGER DEFAULT 0)
                  ''')

conn.commit()
conn.close()


@app.route('/')
def index():
    return render_template('main.html')



@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'username' in session:
        username = session['username']
        if 'avatar' in request.files:
            avatar = request.files['avatar']
            if avatar.filename != '':
                avatar.save(os.path.join(app.root_path, 'static', 'avatars', username + '.jpg'))
                flash('Аватарка успешно загружена.', 'success')
            else:
                flash('Не выбран файл.', 'error')
        else:
            flash('Файл не найден.', 'error')
        return redirect(url_for('profile'))
    else:
        flash('Пожалуйста, войдите в систему, чтобы загрузить аватарку.', 'error')
        return redirect(url_for('index'))



@app.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        print(user)

        if user and user[1] == password:
            session['username'] = username
            flash(f"Добро пожаловать, {username}!", 'success')
            return redirect(url_for('person_panel'))

        flash("Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.", 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash("Пароли не совпадают. Пожалуйста, попробуйте снова.", 'error')
        else:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))

            conn.commit()
            conn.close()

            flash(f"Регистрация успешна для пользователя: {username}", 'success')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/YanRedir')
def YanRedir():
    auth_url = f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
    return redirect(auth_url)


@app.route('/index')
def callback():
    auth_code = request.args.get('code')

    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, data=token_data)

    access_token = response.json().get('access_token')

    headers = {
        'Authorization': f'OAuth {access_token}'
    }

    data = requests.get("https://login.yandex.ru/info", headers=headers).json()

    email = data["default_email"]
    name = data["first_name"]
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, password FROM users WHERE email = ?", (email,))
    email_user = cursor.fetchone()

    if email_user is None:
        cursor.execute("INSERT INTO users (email, password, username) VALUES (?, ?, ?)", (email, password, name))
        conn.commit()
        session['username'] = name
        flash(f"Добро пожаловать, {name}!", 'success')
        return redirect(url_for('person_panel'))
    else:
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        username = cursor.fetchone()[0]
        session['username'] = username  # Set session to username
        flash(f"Добро пожаловать, {username}!", 'success')
        return redirect(url_for('person_panel'))

    conn.close()


def get_user_rating(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rating FROM users WHERE username = ?", (username,))
    rating = cursor.fetchone()[0]
    conn.close()
    return rating


@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, email FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            username = user[0]
            email = user[1]
            user_rating = get_user_rating(username)

            if user_rating >= 100:
                achievement_image = 'ach4.png'
            elif user_rating >= 50:
                achievement_image = 'ach3.png'
            elif user_rating >= 35:
                achievement_image = 'ach2.png'
            else:
                achievement_image = 'ach1.png'

            achievement_path = os.path.join('static', 'img', achievement_image)

            return render_template('profile.html', username=username, email=email, achievement_path=achievement_path)
        else:
            flash("Не удалось загрузить данные профиля.", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к профилю.", 'error')
        return redirect(url_for('index'))


@app.route('/person_panel')
def person_panel():
    if 'username' in session:
        session['attempts'] = 3
        return render_template('person_panel.html')
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к пользователю", 'error')
        return redirect(url_for('index'))


@app.route('/test_easy')
def test_easy():
    if 'username' in session:
        if 'attempts' not in session:
            session['attempts'] = 3
        else:
            attempts = session.get('attempts')
            if attempts == 0:
                return redirect(url_for('person_panel'))

        example = Simple()
        example_functions = [example.simple_examples(), example.branch_examples(), example.multNdivide()]
        example = random.choice(example_functions)

        if example:
            session['example'] = example
            return render_template('test_easy.html', example=example, attempts=session['attempts'])
        else:
            flash("Ошибка: Не удалось получить пример", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        example = session.get('example')

        if 'answer' in request.form:
            answer = request.form['answer']
        else:
            flash("Ошибка: Нет ответа в запросе", 'error')
            return redirect(url_for('test_easy'))

        correct_answer = example[1]
        attempts = session.get('attempts', 3)

        if int(answer) == int(correct_answer):
            print("Получен правильный ответ:", answer)
            username = session.get('username')

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT rating FROM users WHERE username = ?", (username,))
            user_rating = cursor.fetchone()[0]

            updated_rating = user_rating + 1
            cursor.execute("UPDATE users SET rating = ? WHERE username = ?", (updated_rating, username))
            conn.commit()
            conn.close()
            print("Рейтинг пользователя увеличен.")
            return render_template('check.html', rating=updated_rating)
        else:
            attempts -= 1
            session['attempts'] = attempts
            print("Получен неправильный ответ:", answer)
            print("Осталось попыток:", attempts)
            flash("Неверный ответ. Осталось попыток: {}".format(attempts), 'error')
            return redirect(url_for('test_easy'))

    return "Что-то пошло не так!"


@app.route('/test_normal')
def test_normal():
    if 'username' in session:
        if 'attempts' not in session:
            session['attempts'] = 3
        else:
            attempts = session.get('attempts')
            if attempts == 0:
                return redirect(url_for('person_panel'))

        example = Normal()
        example_functions = [example.simple_equantion()]
        example = random.choice(example_functions)

        if example:
            session['example'] = example
            return render_template('test_normal.html', example=example, attempts=session['attempts'])
        else:
            flash("Ошибка: Не удалось получить пример", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/submit_normal', methods=['POST'])
def submit_normal():
    if request.method == 'POST':
        example = session.get('example')

        if 'answer' in request.form:
            answer = request.form['answer']
        else:
            flash("Ошибка: Нет ответа в запросе", 'error')
            return redirect(url_for('test_normal'))

        correct_answer = example[1]
        attempts = session.get('attempts', 3)

        if int(answer) == int(correct_answer):
            print("Получен правильный ответ:", answer)
            username = session.get('username')

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT rating FROM users WHERE username = ?", (username,))
            user_rating = cursor.fetchone()[0]

            updated_rating = user_rating + 3
            cursor.execute("UPDATE users SET rating = ? WHERE username = ?", (updated_rating, username))
            conn.commit()
            conn.close()
            print("Рейтинг пользователя увеличен.")
            return render_template('check.html', rating=updated_rating)
        else:
            attempts -= 1
            session['attempts'] = attempts
            print("Получен неправильный ответ:", answer)
            print("Осталось попыток:", attempts)
            flash("Неверный ответ. Осталось попыток: {}".format(attempts), 'error')
            return redirect(url_for('test_normal'))

    return "Что-то пошло не так!"


@app.route('/test_hard')
def test_hard():
    if 'username' in session:
        if 'attempts' not in session:
            session['attempts'] = 3
        else:
            attempts = session.get('attempts')
            if attempts == 0:
                return redirect(url_for('person_panel'))

        tasks = GIATasks()
        oge_task = tasks.get_random_oge_task()
        example = [oge_task['condition'], oge_task['answer']]  
        print(example)
        if example:
            session['example'] = example
            return render_template('test_hard.html', example=example, attempts=session['attempts'])
        else:
            flash("Ошибка: Не удалось получить пример", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/submit_hard', methods=['POST'])
def submit_hard():
    if request.method == 'POST':
        example = session.get('example')

        if 'answer' in request.form:
            answer = request.form['answer']
        else:
            flash("Ошибка: Нет ответа в запросе", 'error')
            return redirect(url_for('test_normal'))

        correct_answer = example[1]
        attempts = session.get('attempts', 3)

        if int(answer) == int(correct_answer):
            print("Получен правильный ответ:", answer)
            username = session.get('username')

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT rating FROM users WHERE username = ?", (username,))
            user_rating = cursor.fetchone()[0]

            updated_rating = user_rating + 15
            cursor.execute("UPDATE users SET rating = ? WHERE username = ?", (updated_rating, username))
            conn.commit()
            conn.close()
            print("Рейтинг пользователя увеличен.")
            return render_template('check.html', rating=updated_rating)
        else:
            attempts -= 1
            session['attempts'] = attempts
            print("Получен неправильный ответ:", answer)
            print("Осталось попыток:", attempts)
            flash("Неверный ответ. Осталось попыток: {}".format(attempts), 'error')
            return redirect(url_for('test_normal'))

    return "Что-то пошло не так!"

@app.route('/test_very_hard')
def test_very_hard():
    if 'username' in session:
        if 'attempts' not in session:
            session['attempts'] = 3
        else:
            attempts = session.get('attempts')
            if attempts == 0:
                return redirect(url_for('person_panel'))

        tasks = GIATasks()
        oge_task = tasks.get_random_ege_task()
        example = [oge_task['condition'], oge_task['answer']]  
        print(example)
        if example:
            session['example'] = example
            return render_template('test_very_hard.html', example=example, attempts=session['attempts'])
        else:
            flash("Ошибка: Не удалось получить пример", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/submit_very_hard', methods=['POST'])
def submit_very_hard():
    if request.method == 'POST':
        example = session.get('example')

        if 'answer' in request.form:
            answer = request.form['answer']
        else:
            flash("Ошибка: Нет ответа в запросе", 'error')
            return redirect(url_for('test_normal'))

        correct_answer = example[1]
        attempts = session.get('attempts', 3)

        if int(answer) == int(correct_answer):
            print("Получен правильный ответ:", answer)
            username = session.get('username')

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT rating FROM users WHERE username = ?", (username,))
            user_rating = cursor.fetchone()[0]

            updated_rating = user_rating + 20
            cursor.execute("UPDATE users SET rating = ? WHERE username = ?", (updated_rating, username))
            conn.commit()
            conn.close()
            print("Рейтинг пользователя увеличен.")
            return render_template('check.html', rating=updated_rating)
        else:
            attempts -= 1
            session['attempts'] = attempts
            print("Получен неправильный ответ:", answer)
            print("Осталось попыток:", attempts)
            flash("Неверный ответ. Осталось попыток: {}".format(attempts), 'error')
            return redirect(url_for('test_normal'))

    return "Что-то пошло не так!"



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
