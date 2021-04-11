from flask import Flask
from waitress import serve
from flask import request, redirect

app = Flask(__name__)


@app.route('/')
def func():
    return '''<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
    <!-- VK Widget -->
    <div id="vk_allow_messages_from_community"></div>
    <script type="text/javascript">
    VK.Widgets.AllowMessagesFromCommunity("vk_allow_messages_from_community", {}, 203859351);
    </script>'''


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
