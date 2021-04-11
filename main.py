from flask import Flask
from waitress import serve
from flask import request, redirect


app = Flask(__name__)



@app.route('/')
def func():
    return '''<a href='https://oauth.vk.com/authorize?client_id=7820745&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=messages&response_type=token&v=5.103&state=123456'>rrr</a>'''
    # redirect('https://oauth.vk.com/authorize?client_id=7820745&display=page&redirect_uri=htts://magnumopusproject.xyz/dev/Login&scope=messages&response_type=token&v=5.103&state=123456', code=301)
    # return '''<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
#<script type="text/javascript">
#  VK.init({apiId: 7820625});
#</script>

#<!-- VK Widget -->
#<div id="vk_auth"></div>
#<script type="text/javascript">
#  VK.Widgets.Auth("vk_auth", {"authUrl":"/dev/Login"});
#</script>'''

@app.route('/ok')
def ok():
    return ok


@app.route('/dev/Login')
def logi():
    id = request.args.get('uid')
    hash = request.args.get('hash')
    access_token = request.args.get('access_token')
    return (id, hash, access_token)
   

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
