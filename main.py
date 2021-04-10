from flask import Flask
from waitress import serve

app = Flask(__name__)



@app.route('/')
def func():
    return 'NICE'


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)