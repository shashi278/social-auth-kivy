import requests
from oauthlib.oauth2 import WebApplicationClient
import json
import webbrowser
import random

from kivyauth.desktop.utils import (
    request,
    redirect,
    is_connected,
    start_server,
    app,
    _close_server_pls,
    port,
    stop_login,
)
from kivy.app import App
from kivy.clock import Clock

# facebook configuration
FACEBOOK_CLIENT_ID = ""
FACEBOOK_CLIENT_SECRET = ""
fb_authorization_endpoint = "https://www.facebook.com/v15.0/dialog/oauth?"
fb_token_endpoint = "https://graph.facebook.com/v15.0/oauth/access_token?"
fb_userinfo_endpoint = "https://graph.facebook.com/v15.0/me?"

client_facebook = None

event_success_listener = None
event_error_listener = None

__all__ = ("initialize_fb", "login_facebook", "logout_facebook")


def initialize_fb(success_listener, error_listener, client_id=None, client_secret=None):
    a = App.get_running_app()
    a.bind(on_stop=lambda *args: _close_server_pls(port))

    global event_success_listener
    event_success_listener = success_listener

    global event_error_listener
    event_error_listener = error_listener

    global FACEBOOK_CLIENT_ID
    FACEBOOK_CLIENT_ID = client_id

    global FACEBOOK_CLIENT_SECRET
    FACEBOOK_CLIENT_SECRET = client_secret

    global client_facebook
    client_facebook = WebApplicationClient(FACEBOOK_CLIENT_ID)


@app.route("/loginFacebook")
def loginFacebook():

    st = "".join([random.choice("abcdefgh1234567") for _ in range(10)])
    ds = "".join([random.choice("1234567890") for _ in range(10)])

    request_uri = client_facebook.prepare_request_uri(
        fb_authorization_endpoint,
        redirect_uri=request.base_url + "/callbackFacebook",
        scope=["email"],
        state="{st=" + st + ",ds=" + ds + "}",
    )

    return redirect(request_uri)


@app.route("/loginFacebook/callbackFacebook")
def callbackFacebook():
    code = request.args.get("code")

    # prepare a request to get tokens
    token_url, headers, body = client_facebook.prepare_token_request(
        fb_token_endpoint,
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        code=code,
        redirect_url=request.base_url,
    )

    # send the request and get the response
    token_response = requests.post(token_url, headers=headers, data=body)

    # send the request and get the response
    # app_token_response = requests.get(token_url, headers=headers, data=body)

    headers = {
        "Authorization": token_response.json()["access_token"]
        + " "
        + token_response.json()["token_type"]
    }

    request_uri = client_facebook.prepare_request_uri(
        fb_userinfo_endpoint,
        fields=["id", "name", "email", "picture"],
        access_token=token_response.json()["access_token"],
    )

    # make the request and get the response
    userinfo_response = requests.get(request_uri, headers=headers, data=None).json()
    stop_login()

    # parse the information
    if userinfo_response.get("id"):
        Clock.schedule_once(lambda *args: event_success_listener(
            userinfo_response["name"],
            userinfo_response["email"],
            userinfo_response["picture"]["data"]["url"],
        ), 0)

        return "<h2>Logged in using Facebook. Return back to the Kivy application</h2>"

    event_error_listener()
    return "User Email not available or not verified"


def login_facebook():
    if is_connected():
        start_server(port)
        webbrowser.open("https://127.0.0.1:{}/loginFacebook".format(port), 1, False)
    else:
        event_error_listener()


def logout_facebook(after_logout):
    """
    Logout from facebook login

    :param: `after_logout` - Function to be called after logging out
    """
    after_logout()
