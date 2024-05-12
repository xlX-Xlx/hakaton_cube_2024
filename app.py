from flask import Flask, redirect, request
import requests
import secrets
import string

app = Flask(__name__)

CLIENT_ID = '623a52b24eba4a6888d3b87d0b2904e2' # 5 ВАЖНЫХ переменных 
CLIENT_SECRET = '453cfc6b79fe4b2084d803061731ab12'
TOKEN_URL = 'https://oauth.yandex.ru/token'
AUTH_URL = 'https://oauth.yandex.ru/authorize'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'

@app.route('/') # здесь нужна ссылка ведущая с кнопки "Авторизоваться через Яндекс"
def index():
    auth_url = f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
    return redirect(auth_url)

@app.route('/callback') # здесь нужна ссылка для редиректа на нужную страницу, эту ссылку нужно скинуть мне
def callback():
    auth_code = request.args.get('code')
    print(request)

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

    email = data["default_email"] # здесь мы получаем нужные данные и автоматом генерируем пароль для записи в БД
    name = data["first_name"]
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))

    return None

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)