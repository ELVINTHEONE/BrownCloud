import os
import logging
import soundcloud
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, jsonify
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

# before each request, make sure we have a validation token, unless requesting the index or redirect
#@app.before_request
#def before_request():
    #token = _getAccessToken()
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
    # spawn a client
    client = soundcloud.Client(access_token="{0}".format(_getAccessToken()))
    # get the query string
    #query = request.json['query']
    # query the tracks
    # tracks = client.get('/tracks', q="{0}".format("helo"), limit=10)
    # jsonify the tracks
    # return jsonify({'tracks': tracks})
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)
