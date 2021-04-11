from flask import Flask
from waitress import serve
from flask import request, redirect

app = Flask(__name__)


@app.route('/')
def func():
    return '''<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
# <script type="text/javascript">
#  VK.init({apiId: 7820625});
# </script>

# <!-- VK Widget -->
# <div id="vk_auth"></div>
# <script type="text/javascript">
#  VK.Widgets.Auth("vk_auth", {"authUrl":"/dev/Login"});
# </script>'''


@app.route('/ok')
def ok():
    return ok


@app.route('/dev/Login')
def logi():
    id = request.args.get('uid')
    hash = request.args.get('hash')
    return '''<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
<!-- VK Widget -->
<div id="vk_allow_messages_from_community"></div>
<script type="text/javascript">
VK.Widgets.AllowMessagesFromCommunity("vk_allow_messages_from_community", {}, 203859351);
</script>'''


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
