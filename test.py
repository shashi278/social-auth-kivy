from flask import Flask, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
import webbrowser
import multiprocessing
import time

# google configurations
GOOGLE_CLIENT_ID = (
    "161589307268-8nn5amnk5ba79tj4tbkht5dobiff5nsb.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "CwEd_BZrrwjprk8ZS5L9Soaa"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

app = Flask(__name__)
app.secret_key = os.urandom(26)

email_verified= False

client_id="161589307268-8nn5amnk5ba79tj4tbkht5dobiff5nsb.apps.googleusercontent.com"

url= (
    "https://accounts.google.com/o/oauth2/v2/auth?scope=email%20profile&response_type=code&"
    #"state=security_token%3D138r5719ru3e1%26url%3Dhttps%3A%2F%2Foauth2.example.com%2Ftoken&"
    "redirect_uri=http%3A//127.0.0.1%3A9004&"
    "client_id={}"
).format(client_id)



client_google = WebApplicationClient(GOOGLE_CLIENT_ID)

class Some():
    def __init__(self): 
        self._running = True
        
    def terminate(self): 
        self._running = False

    def close_thread(self):
        #if not self._running:
        self.thread.terminate()
    
    def start_thread(self):
        self.thread= multiprocessing.Process(
            target= lambda : app.run(host="127.0.0.1", port=9004, debug=False, ssl_context="adhoc")
        )
        self.thread.start()

some= Some()

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/")
def something():
    return redirect(url_for("loginGoogle"))

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

    # make the request and get the response
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # parse the information
    if userinfo_response.json().get("email_verified"):
        tmp = userinfo_response.json()
        print(tmp)
        """ return update_database(
            tmp["sub"], tmp["email"], tmp["picture"], tmp["given_name"]
        ) """
        close_server()
        return "Success. Return to the application"
    
    return "User Email not available or not verified"

def close_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def check_close():
    
    while not email_verified:
        print("Email verified: {}".format(email_verified))
        time.sleep(.5)
    
    print("Email verified: {}".format(email_verified))
    Some().close_thread()

thread1= multiprocessing.Process(
        target= check_close
    )
    

if __name__ == "__main__":
    #import threading
    
    #from kivy.clock import Clock
    
    
    #global thread
    #thread.start()
    #thread1.start()
    #check_close()
    some.start_thread()
    #time.sleep(2)
    #print(email_verified)
    #print("After 2 sec")
    #some.close_thread()
    #email_verified= True
    #print(email_verified)
    #thread1 = thread
    #thread1.terminate()
    #Some().close_thread()

    webbrowser.open("https://127.0.0.1:9004/")

    #webbrowser.open(url)

