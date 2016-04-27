import os
import logging
import soundcloud
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from src.session import ChunkedSecureCookieSessionInterface

app = Flask(__name__)
app.config.from_object(__name__)

client = soundcloud.Client(
        client_id="53e3ccfd305043eb4e01b99b9cf18a37",
        client_secret="f29c8e8b2a7ba68a2d9fd4efa62d2e21",
        redirect_uri="http://brown-cloud.herokuapp.com/auth_redirect"
        )

@app.route("/")
def index():
    token = request.cookies.get('access_token')
    if (token):
        #client = soundcloud.Client(access_token=token)
        #return render_template("index.html", username=client.get('/me').username)
        return render_template("index.html")
    else:
        return redirect(client.authorize_url())

@app.route("/auth_redirect")
def auth_redirect():
    code = request.args.get('code')
    obj = client.exchange_token(code)
    resp = make_response(redirect("/"))
    resp.set_cookie('access_token', '{0}'.format(obj.access_token))
    #resp.set_cookie('expires', '{0}'.format(obj.expires))
    return resp

if __name__ == '__main__':
    app.run()
