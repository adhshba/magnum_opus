from flask import Flask
from waitress import serve

app = Flask(__name__)



@app.route('/')
def func():
    return '''<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
<script type="text/javascript">
  VK.init({apiId: 7820625});
</script>

<!-- VK Widget -->
<div id="vk_auth"></div>
<script type="text/javascript">
  VK.Widgets.Auth("vk_auth", {"authUrl":"/dev/Login"});
</script>'''


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
