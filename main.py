import os
import logging
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from flask.ext.cors import CORS, cross_origin
from src.session import ChunkedSecureCookieSessionInterface
from werkzeug.debug import get_current_traceback

from lib.sc_lib import _getGenericClient, _toJson, _sendQuery, RequestType

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

BASE_URI = os.environ['BASE_URI']

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
        #client = _getGenericClient()
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
    code = request.args.get('code')
    client = _getGenericClient()
    obj = client.exchange_token(code)
    resp = make_response(redirect("/"))
    resp.set_cookie('access_token', '{0}'.format(obj.access_token))
    #resp.set_cookie('expires', '{0}'.format(obj.expires))
    return resp

# api functions
@app.route("/friends", methods=['POST'])
@cross_origin()
def get_friends():
    print("finding " + request.json['query']);
    return _sendQuery(request, RequestType.friends, 10)

@app.route("/tracks", methods=['POST'])
def get_tracks():
    return _sendQuery(request, RequestType.tracks, 10)

@app.route("/playlists", methods=['POST'])
def get_playlists():
    return _sendQuery(request, RequestType.playlists, 10)

@app.route("/user_favorites", methods=['POST'])
def get_user_favorites():
    return _sendQuery(request, RequestType.user_favorites, 10)

@app.route("/user_playlists", methods=['POST'])
def get_user_playlists():
    return _sendQuery(request, RequestType.user_playlists, 10)

if __name__ == '__main__':
    app.run(debug=True)
