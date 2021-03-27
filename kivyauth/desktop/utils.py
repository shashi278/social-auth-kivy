from flask import Flask, request, redirect
import requests
import os
import threading
import socket
from kivy.clock import Clock
import random

# # twitter configuration
# TWITTER_CLIENT_ID = ""
# TWITTER_CLIENT_SECRET = ""
# tw_authorization_endpoint = "https://api.twitter.com/oauth/authorize"
# tw_token_endpoint = "https://api.twitter.com/oauth/access_token"
# tw_userinfo_endpoint = "https://api.twitter.com/user"
# tw_request_token_endpoint = "https://api.twitter.com/oauth/request_token"

app = Flask(__name__)
app.secret_key = os.urandom(26)

PATH = os.path.dirname(__file__)
cert_path = os.path.join(PATH, "cert.pem")
key_path = os.path.join(PATH, "key.pem")

port = 9004
ran_num = random.randint(1111, 9999)


def _start_server(*args):
    try:
        app.run(host="127.0.0.1", port=port, ssl_context=(cert_path, key_path))
    except OSError:
        pass


def start_server(port):
    thread = threading.Thread(target=_start_server)

    thread.start()


@app.route("/kill{}".format(ran_num))
def close_server(*args, **kwargs):
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()

    return ""


def stop_login(*args):
    _close_server_pls(port)


def _close_server_pls(port, *args):
    try:
        requests.get("https://127.0.0.1:{}/kill{}".format(port, ran_num), verify=False)
    except requests.exceptions.ConnectionError:
        pass


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


# @app.route("/loginTwitter")
# def loginTwitter():

#     # construct the request uri
#     # request_uri = client_twitter.prepare_request_uri(
#     #     tw_authorization_endpoint,
#     #     redirect_uri=request.base_url + "/callbackTwitter",
#     # )
#     # return redirect(request_uri)

#     resp = requests.post(
#         tw_request_token_endpoint,
#         {
#             "oauth_callback": "https%3A%2F%2F127.0.0.1%3A9004%2FloginTwitter%2FcallbackTwitter"
#         },
#     )
#     return resp.json()


# @app.route("/loginTwitter/callbackTwitter")
# def callbackTwitter():
#     code = request.args.get("code")

#     token_url, headers, body = client_twitter.prepare_token_request(
#         tw_token_endpoint,
#         client_id=TWITTER_CLIENT_ID,
#         client_secret=TWITTER_CLIENT_SECRET,
#         code=code,
#         redirect_url=request.base_url,
#     )

#     # send the request and get the response
#     token_response = requests.post(token_url, headers=headers, data=body)

#     # for some reason, token_response.json() is raising an error. So gotta do it manually
#     token_info = re.search(
#         "^access_token=(.*)&scope=.*&token_type=(.*)$", token_response.text
#     )
#     uri = tw_userinfo_endpoint
#     headers = {"Authorization": token_info.group(2) + " " + token_info.group(1)}
#     body = None

#     global userinfo_response
#     userinfo_response = requests.get(uri, headers=headers, data=body).json()

#     # parse the information
#     if userinfo_response.get("id"):
#         close_server()
#         print(get_userinfo())
#         print(get_userinfo())
#         # return update_database(
#         #     tmp["id"], tmp["email"], tmp["picture"]["data"]["url"], tmp["name"]
#         # )
#         return "Success using twitter. Return to the app"
#     return "User Email not available or not verified", 400


# if __name__ == "__main__":

#     if is_connected():
#         port = 9004
#         start_server(port)

#         webbrowser.open("https://127.0.0.1:{}/loginGoogle".format(port), 1, False)

#     else:
#         print("Could not connect. Check connection and try again")
