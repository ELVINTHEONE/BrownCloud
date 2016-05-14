import os
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from werkzeug.debug import get_current_traceback

from lib.sc_lib import getGenericClient, toJson, sendQuery, RequestType
from lib.session import ChunkedSecureCookieSessionInterface

app = Flask(__name__)

try:
    # if running from localhost, enable cross origin
    if os.environ['env'] == local:
        from flask.ext.cors import CORS, cross_origin
        cors = CORS(app)
        app.config.from_object(__name__)
        app.config['CORS_HEADERS'] = 'Content-Type'
except:
    pass

BASE_URI = os.environ['BASE_URI']
SOUNDCLOUD_MAX_REQUEST_LIMIT = 200

# return the BrownCloud access token from the client's cookie, if they have one
def _getAccessToken(request):
    return request.cookies.get('browncloud_access_token')

# before each request, make sure we have a validation token, unless requesting the index or redirect
#@app.before_request
#def before_request():
    print("before request getting a token")
    token = _getAccessToken(request)
    if (token):
        print("before request got a token " + token)
    #if (not token and
        #request.endpoint != '/' and
        #request.endpoint != 'auth_redirect' and
        #request.endpoint != 'static'):
        #client = getGenericClient()
        #return redirect(client.authorize_url())
    #pass

@app.errorhandler(500)
def print_err(ex):
    print(ex)
    track = get_current_traceback(skip=1, show_hidden_frames=True, ignore_system_exceptions=False)
    track.log()

@app.route("/", methods=['GET'])
def index():
    return render_template(
        "index.html",
        year=datetime.date.today().year,
        base_uri=BASE_URI
    )

@app.route("/find_user", methods=['GET'])
def find_user():
    return render_template("find_user.html", base_uri=BASE_URI)

@app.route("/auth_redirect", methods=['GET'])
def auth_redirect():
    print("in redirect")
    code = request.args.get('code')
    client = getGenericClient()
    print("exchanging token")
    obj = client.exchange_token(code)
    print("making the response and setting the cookie")
    resp = make_response(redirect("/"))
    resp.set_cookie('access_token', '{0}'.format(obj.access_token))
    print("returning")
    #resp.set_cookie('expires', '{0}'.format(obj.expires))
    return resp

@app.route("/login", methods=['GET'])
def login():
    client = getGenericClient()
    return redirect(client.authorize_url())

@app.route("/logout", methods=['GET'])
def logout():
    return "not implemented"
    #client = getGenericClient()
    #return redirect(client.authorize_url())

# api functions
@app.route("/friends", methods=['POST'])
@cross_origin()
def get_friends():
    return sendQuery(request, RequestType.friends, SOUNDCLOUD_MAX_REQUEST_LIMIT)

@app.route("/tracks", methods=['POST'])
def get_tracks():
    return sendQuery(request, RequestType.tracks, 10)

@app.route("/playlists", methods=['POST'])
def get_playlists():
    return sendQuery(request, RequestType.playlists, 10)

@app.route("/user_favorites", methods=['POST'])
def get_user_favorites():
    return sendQuery(request, RequestType.user_favorites, 10)

@app.route("/user_playlists", methods=['POST'])
def get_user_playlists():
    return sendQuery(request, RequestType.user_playlists, 10)

if __name__ == '__main__':
    app.run(debug=True)
