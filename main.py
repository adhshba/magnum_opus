from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


if __name__ == '__main__':
    main()
