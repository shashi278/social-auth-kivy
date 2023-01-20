import requests
from oauthlib.oauth2 import WebApplicationClient
import json
import webbrowser
import random
import re

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

# github configuration
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
git_authorization_endpoint = "https://github.com/login/oauth/authorize"
git_token_endpoint = "https://github.com/login/oauth/access_token"
git_userinfo_endpoint = "https://api.github.com/user"

client_github = None

event_success_listener = None
event_error_listener = None

__all__ = ("initialize_github", "login_github", "logout_github")


def initialize_github(
    success_listener, error_listener, client_id=None, client_secret=None
):
    a = App.get_running_app()
    a.bind(on_stop=lambda *args: _close_server_pls(port))

    global event_success_listener
    event_success_listener = success_listener

    global event_error_listener
    event_error_listener = error_listener

    global GITHUB_CLIENT_ID
    GITHUB_CLIENT_ID = client_id

    global GITHUB_CLIENT_SECRET
    GITHUB_CLIENT_SECRET = client_secret

    global client_github
    client_github = WebApplicationClient(GITHUB_CLIENT_ID)

@app.route("/loginGithub")
def loginGithub():
    request_uri = client_github.prepare_request_uri(
        git_authorization_endpoint,
        redirect_uri=request.base_url + "/callbackGithub",
        scope=["read:user:email"],
        state="".join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(20)]),
    )
    return redirect(request_uri)

@app.route("/loginGithub/callbackGithub")
def callbackGithub():
    # Get authorization code Github sent back
    code = request.args.get("code")

    # prepare a request to get tokens
    token_url, headers, body = client_github.prepare_token_request(
        git_token_endpoint,
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        code=code,
        redirect_url=request.base_url,
        state="".join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(20)]),
    )

    # send the request and get the response
    token_response = requests.post(token_url, headers=headers, data=body)

    # for some reason, token_response.json() is raising an error. So gotta do it manually
    token_info = re.search(
        "^access_token=(.*)&scope=.*&token_type=(.*)$", token_response.text
    )

    headers = {"Authorization": token_info.group(2) + " " + token_info.group(1)}
    body = None

    userinfo_response = requests.get(
        git_userinfo_endpoint, headers=headers, data=body
    ).json()
    stop_login()

    # parse the information
    if userinfo_response.get("id"):
        Clock.schedule_once(lambda *args: event_success_listener(
            userinfo_response["name"],
            userinfo_response["email"],
            userinfo_response["avatar_url"],
        ), 0)
        return "<h2>Logged in using Github. Return back to the Kivy application</h2>"

    event_error_listener()
    return "User Email not available or not verified"

def login_github():
    if is_connected():
        start_server(port)
        webbrowser.open("https://127.0.0.1:{}/loginGithub".format(port), 1, False)
    else:
        event_error_listener()

def logout_github(after_logout):
    """
    Logout from github login

    :param: `after_logout` - Function to be called after logging out
    """
    after_logout()
