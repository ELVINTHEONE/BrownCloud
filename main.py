import os
import logging
import soundcloud
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from src.session import ChunkedSecureCookieSessionInterface

app = Flask(__name__)
app.config.from_object(__name__)

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
    return render_template("index.html")

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
@app.route("/tracks", methods=['POST'])
def get_tracks():
    # spawn a generic client
    client = _getGenericClient()
    # get the query string
    query = request.json['query']
    print("got query " + query)
    # query the tracks
    tracks = client.get('/tracks', q=query, limit=10)
    # jsonify the tracks
    print("sending response")
    return _toJson(tracks)

@app.route("/playlists", methods=['POST'])
def get_playlists():
    # spawn a generic client
    client = _getGenericClient()
    # get the query string
    query = request.json['query']
    print("got query " + query)
    # query the tracks
    tracks = client.get('/tracks', q=query, limit=10)
    # jsonify the tracks
    print("sending response")
    return _toJson(tracks)

if __name__ == '__main__':
    app.run(debug=True)
