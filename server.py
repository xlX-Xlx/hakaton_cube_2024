import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from generate import alg

app = Flask(__name__)
app.secret_key = 'your_secret_key'

admin_username = 'admin'
admin_password = 'qwerty'

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
    return render_template('login.html')


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
        if username == admin_username and password == admin_password:
            session['username'] = username
            flash(f"Добро пожаловать, {username}!", 'success')
            return redirect(url_for('admin_panel'))
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

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
            return redirect(url_for('person_panel'))

    return render_template('register.html')


@app.route('/admin_panel')
def admin_panel():
    if 'username' in session and session['username'] == admin_username:
        return render_template('admin_panel.html')
    else:
        flash("Доступ к админ панели запрещен.", 'error')
        return redirect(url_for('index'))


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
            return render_template('profile.html', username=username, email=email)
        else:
            flash("Не удалось загрузить данные профиля.", 'error')
            return redirect(url_for('index'))
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к профилю.", 'error')
        return redirect(url_for('index'))


@app.route('/person_panel')
def person_panel():
    if 'username' in session:
        return render_template('person_panel.html')
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к пользователю", 'error')
        return redirect(url_for('index'))


@app.route('/test_easy')
def test_easy():
    if 'username' in session:
        if 'attempts' not in session:
            session['attempts'] = 3  # Устанавливаем количество попыток
        example = alg.Generate.simple_examples(self=None)
        session['example'] = example
        return render_template('test_easy.html', example=example, attempts=session['attempts'])
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        example = session.get('example')
        answer = request.form['answer']
        correct_answer = example[1]
        if int(answer) == int(correct_answer):
            print("Получен правильный ответ:", answer)
            # Получаем имя пользователя из сессии
            username = session.get('username')
            # Увеличиваем рейтинг пользователя на 1
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET rating = rating + 1 WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            print("Рейтинг пользователя увеличен.")
            return "Ответ верный!"
        else:
            session['attempts'] -= 1
            print("Получен неправильный ответ:", answer)
            print("Осталось попыток:", session['attempts'])
            return redirect(url_for('test_easy'))
    return "Что-то пошло не так!"


@app.route('/test_normal')
def test_normal():
    if 'username' in session:
        return render_template('test_normal.html')
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/test_hard')
def test_hard():
    if 'username' in session:
        return render_template('test_hard.html')
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


@app.route('/test_very_hard')
def test_very_hard():
    if 'username' in session:
        return render_template('test_very_hard.html')
    else:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к тесту", 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
