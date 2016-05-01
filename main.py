import os
import logging
import soundcloud
import json
import datetime
from enum import Enum
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from src.session import ChunkedSecureCookieSessionInterface

app = Flask(__name__)
app.config.from_object(__name__)

class RequestType(Enum):
    friends = 1
    tracks = 2
    playlists = 3

def _getGenericClient():
    return soundcloud.Client(
            client_id="53e3ccfd305043eb4e01b99b9cf18a37",
            client_secret="f29c8e8b2a7ba68a2d9fd4efa62d2e21",
            redirect_url="http://brown-cloud.herokuapp.com/auth_redirect"
            )

def _getAccessToken(request):
    return request.cookies.get('browncloud_access_token')

# jsonify a list
def _toJson(list):
    return json.dumps(list, default=lambda o: o.__dict__)

# send a request to SoundCloud
def _sendQuery(request, type, limit):
    # spawn a generic client
    client = _getGenericClient()
    ret = None
    query = request.json['query']
    if (type == RequestType.friends):
        ret = client.get(
            '/users',
            q = query,
            limit = limit
        )
    elif (type == RequestType.tracks):
        ret = client.get(
            '/tracks',
            q = query,
            tags = request.json['tags'],
            filter = request.json['visibility'],
            #license = request.json['license'],
            bpmFrom= request.json['bpmFrom'],
            bpmTo = request.json['bpmTo'],
            durationFrom = request.json['durationFrom'],
            durationTo = request.json['durationTo'],
            createdAtFrom = request.json['createdAtFrom'],
            createdAtTo = request.json['createdAtTo'],
            genres = request.json['genres'],
            types = request.json['type'],
            limit = limit
        )
    elif (type == RequestType.playlists):
        ret = client.get(
            '/playlists',
            q = query,
            limit = limit
        )
    return _toJson(ret);

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

@app.route("/")
def index():
    return render_template("index.html", year=datetime.date.today().year)

@app.route("/auth_redirect")
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
def get_friends():
    return _sendQuery(request, RequestType.friends, 10)

@app.route("/tracks", methods=['POST'])
def get_tracks():
    return _sendQuery(request, RequestType.tracks, 10)

@app.route("/playlists", methods=['POST'])
def get_playlists():
    return _sendQuery(request, RequestType.playlists, 10)

if __name__ == '__main__':
    app.run(debug=True)
