import os
import logging
import soundcloud
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

logger = logging.getLogger(__file__)

app = Flask(__name__)
app.config.from_object(__name__)

client = soundcloud.Client(
        client_id="53e3ccfd305043eb4e01b99b9cf18a37",
        client_secret="f29c8e8b2a7ba68a2d9fd4efa62d2e21",
        redirect_uri="http://brown-cloud.herokuapp.com/auth_redirect"
        )

user = None

class User:
    def __init__(self, access_token, expires, scope, refresh_token, me):
        this.access_token = access_token
        this.expires = expires
        this.scope = scope
        this.refresh_token = refresh_token
        this.me = me

@app.route("/")
def index():
    logger.info('user is ' + user)
    if user is None:
        return redirect(client.authorize_url())
    else:
        return render_template("index.html")


@app.route("/auth_redirect")
def auth_redirect():
    code = request.args.get('code')
    try:
        access_token = client.exchange_token(code)
        user = "hello"
        logging.info('access token is ' + access_token)
        #user = User( "", "", "", "", "")
        #return "hello!" + client.get('/me').username
    except:
        print("unexpected error:")
    user = "wtf"
    return redirect(url_for('index'))
    return "hello " + url_for('/')
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
