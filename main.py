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
        return render_template("index.html")
    else:
        resp = make_response(redirect(client.authorize_url()))
        resp.set_cookie('test', 'abc')
        return resp

@app.route("/auth_redirect")
def auth_redirect():
    code = request.args.get('code')
    access_token = client.exchange_token(code)
    resp = make_response(redirect("/"))
    resp.set_cookie('access_token', access_token)
    return resp
    #user = User("", "", "", "", "")
    #return "hello!" + client.get('/me').username
    #return redirect(url_for('index'))
    #return render_template("index.html")


if __name__ == '__main__':
    app.run()
