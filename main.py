from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def func():
    return 'NICE'


def main():
    app.run('127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
