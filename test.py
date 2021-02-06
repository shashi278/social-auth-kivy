from flask import Flask, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
import requests
from requests.exceptions import ConnectionError
import os
import json
import webbrowser
import multiprocessing
import time
import re
import urllib
import random

# google configurations
GOOGLE_CLIENT_ID = (
    "161589307268-3mk3igf1d0qh4rk03ldfm0u68g038h6t.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "mE3YsB5u4haMwq8P80xCs3g1"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# facebook configuration
FACEBOOK_CLIENT_ID = "439926446854840"
FACEBOOK_CLIENT_SECRET = "bfa21d5a50b7e51ff3eb961be6420183"
fb_authorization_endpoint = "https://www.facebook.com/v4.0/dialog/oauth?"
fb_token_endpoint = "https://graph.facebook.com/v4.0/oauth/access_token?"
fb_userinfo_endpoint = "https://graph.facebook.com/v4.0/me?"

# github configuration
GITHUB_CLIENT_ID = "33ffe92ab174c888f742"
GITHUB_CLIENT_SECRET = "5abf88cb26d599abe46996dcf576e4273c3bbd7f"
git_authorization_endpoint = "https://github.com/login/oauth/authorize"
git_token_endpoint = "https://github.com/login/oauth/access_token"
git_userinfo_endpoint = "https://api.github.com/user"

#twitter configuration
TWITTER_CLIENT_ID = "3OLfWRx7NmfS90JkhNXWvSi8a"
TWITTER_CLIENT_SECRET = "cOTkgNEbnWVrezCaD9h6RQLOOFLREnJI7rDDTfTibv6nuywSTZ"
tw_authorization_endpoint = "https://api.twitter.com/oauth/authorize"
tw_token_endpoint = "https://api.twitter.com/oauth/access_token"
tw_userinfo_endpoint = "https://api.twitter.com/user"
tw_request_token_endpoint = "https://api.twitter.com/oauth/request_token"

app = Flask(__name__)
app.secret_key = os.urandom(26)

email_verified= False
userinfo_response = json.dumps({})


client_google = WebApplicationClient(GOOGLE_CLIENT_ID)
client_facebook = WebApplicationClient(FACEBOOK_CLIENT_ID)
client_github = WebApplicationClient(GITHUB_CLIENT_ID)
client_twitter = WebApplicationClient(TWITTER_CLIENT_ID)
    
def start_server():
    thread= multiprocessing.Process(
        target= lambda : app.run(host="127.0.0.1", port=9004, ssl_context=('cert.pem', 'key.pem'))
    )
    thread.start()

def close_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def something():
    return redirect(url_for("loginGoogle"))

def get_userinfo():
    global userinfo_response
    tmp = userinfo_response
    userinfo_response = json.dumps({})
    return tmp

@app.route("/loginGoogle")
def loginGoogle():
    # takeout auth endpoint url from google login
    try:
        google_provider_cfg = get_google_provider_cfg()
        
    except ConnectionError:
        #print("Could not connect. Check internet and try again")
        close_server()
        return "Could not connect. Check connection and try again"

    
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # construct the request uri
    request_uri = client_google.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callbackGoogle",
        scope=["openid", "email", "profile"],
    )
    
    return redirect(request_uri)

@app.route("/loginFacebook")
def loginFacebook():
    try:
        r = requests.get("https://www.google.com")
    except ConnectionError:
        #print("Could not connect. Check internet and try again")
        close_server()
        return "Could not connect. Check connection and try again"

    request_uri = client_facebook.prepare_request_uri(
        fb_authorization_endpoint,
        redirect_uri=request.base_url + "/callbackFacebook",
        scope=["email"],
        state="{st=state123abc,ds=123456789}",
    )

    return redirect(request_uri)

@app.route("/loginGithub")
def loginGithub():

    # try:
    #     r = requests.get("https://www.google.com")
    # except ConnectionError:
    #     #print("Could not connect. Check internet and try again")
    #     close_server()
    #     return "Could not connect. Check connection and try again"
    
    # construct the request uri
    request_uri = client_github.prepare_request_uri(
        git_authorization_endpoint,
        redirect_uri=request.base_url + "/callbackGithub",
        scope=["read:user:email"],
        state=''.join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(20)]),
    )
    return redirect(request_uri)

@app.route("/loginTwitter")
def loginTwitter():

    # construct the request uri
    # request_uri = client_twitter.prepare_request_uri(
    #     tw_authorization_endpoint,
    #     redirect_uri=request.base_url + "/callbackTwitter",
    # )
    # return redirect(request_uri)

    resp = requests.post(tw_request_token_endpoint, {'oauth_callback': "https%3A%2F%2F127.0.0.1%3A9004%2FloginTwitter%2FcallbackTwitter"})
    return resp.json()

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

    #requests.post()

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

    # make the request and get the response
    global userinfo_response
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    # parse the information
    if userinfo_response.get("email_verified"):
        #tmp = userinfo_response
        #print(tmp)
        # uri = request.base_url + "/hello"
        # r = requests.get(uri)
        # print(r.json())
        """ return update_database(
            tmp["sub"], tmp["email"], tmp["picture"], tmp["given_name"]
        ) """
        close_server()
        print(get_userinfo())
        print(get_userinfo())
        return "Success using google. Return to the application"
    
    return "User Email not available or not verified"


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

    token_url = (
        fb_token_endpoint
        + "client_id={}"
        + "&client_secret={}"
        + "&grant_type=client_credentials"
    ).format(FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET)

    # send the request and get the response
    #app_token_response = requests.get(token_url, headers=headers, data=body)

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
    global userinfo_response
    userinfo_response = requests.get(request_uri, headers=headers, data=None).json()

    # parse the information
    if userinfo_response.get("id"):
        close_server()
        print(get_userinfo())
        print(get_userinfo())
        # return update_database(
        #     tmp["id"], tmp["email"], tmp["picture"]["data"]["url"], tmp["name"]
        # )
        return "Success using facebook. Return to the app"
    return "User Email not available or not verified", 400

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
        state=''.join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(20)]),
    )

    # send the request and get the response
    token_response = requests.post(token_url, headers=headers, data=body)

    # for some reason, token_response.json() is raising an error. So gotta do it manually
    token_info = re.search(
        "^access_token=(.*)&scope=.*&token_type=(.*)$", token_response.text
    )
    uri = git_userinfo_endpoint
    headers = {"Authorization": token_info.group(2) + " " + token_info.group(1)}
    body = None

    global userinfo_response
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    # parse the information
    if userinfo_response.get("id"):
        close_server()
        print(get_userinfo())
        print(get_userinfo())
        # return update_database(
        #     tmp["id"], tmp["email"], tmp["picture"]["data"]["url"], tmp["name"]
        # )
        return "Success using github. Return to the app"
    return "User Email not available or not verified", 400


@app.route("/loginTwitter/callbackTwitter")
def callbackTwitter():
    code = request.args.get("code")

    token_url, headers, body = client_twitter.prepare_token_request(
        tw_token_endpoint,
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        code=code,
        redirect_url=request.base_url
    )

    # send the request and get the response
    token_response = requests.post(token_url, headers=headers, data=body)

    # for some reason, token_response.json() is raising an error. So gotta do it manually
    token_info = re.search(
        "^access_token=(.*)&scope=.*&token_type=(.*)$", token_response.text
    )
    uri = tw_userinfo_endpoint
    headers = {"Authorization": token_info.group(2) + " " + token_info.group(1)}
    body = None

    global userinfo_response
    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    # parse the information
    if userinfo_response.get("id"):
        close_server()
        print(get_userinfo())
        print(get_userinfo())
        # return update_database(
        #     tmp["id"], tmp["email"], tmp["picture"]["data"]["url"], tmp["name"]
        # )
        return "Success using twitter. Return to the app"
    return "User Email not available or not verified", 400

if __name__ == "__main__":

    start_server()
    
    webbrowser.open("https://127.0.0.1:9004/", 1, False)
