import requests
from oauthlib.oauth2 import WebApplicationClient
import json
import webbrowser

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

# google configurations
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client_google = None

event_success_listener = None
event_error_listener = None

__all__ = ("initialize_google", "login_google", "logout_google")


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def initialize_google(
    success_listener, error_listener, client_id=None, client_secret=None
):
    a = App.get_running_app()
    a.bind(on_stop=lambda *args: _close_server_pls(port))

    global event_success_listener
    event_success_listener = success_listener

    global event_error_listener
    event_error_listener = error_listener

    global GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_ID = client_id

    global GOOGLE_CLIENT_SECRET
    GOOGLE_CLIENT_SECRET = client_secret

    global client_google
    client_google = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route("/loginGoogle")
def loginGoogle():
    # takeout auth endpoint url from google login
    google_provider_cfg = get_google_provider_cfg()

    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # construct the request uri
    request_uri = client_google.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callbackGoogle",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)

@app.route("/loginGoogle/callbackGoogle")
def callbackGoogle():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # Extract the URL to hit to get tokens
    # that allows to ask things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # prepare a request to get tokens
    token_url, headers, body = client_google.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    # send the request and get the response
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # parse the token response
    client_google.parse_request_body_response(json.dumps(token_response.json()))

    # Now we already have necessary tokens
    # lets ask Google for required informations
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client_google.add_token(userinfo_endpoint)

    userinfo_response = requests.get(uri, headers=headers, data=body).json()
    stop_login()

    # parse the information
    if userinfo_response.get("email_verified"):
        Clock.schedule_once(lambda *args: event_success_listener(
            userinfo_response["name"],
            userinfo_response["email"],
            userinfo_response["picture"],
        ), 0)

        return "<h2>Logged in using Google. Return back to the Kivy application</h2>"

    event_error_listener()
    return "User Email not available or not verified"

def login_google():
    if is_connected():
        start_server(port)
        webbrowser.open("https://127.0.0.1:{}/loginGoogle".format(port), 1, False)

    else:
        event_error_listener()

def logout_google(after_logout):
    """
    Logout from google login

    :param: `after_logout` - Function to be called after logging out
    """
    after_logout()
