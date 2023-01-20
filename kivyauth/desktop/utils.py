from flask import Flask, request, redirect
import requests
import os
import threading
import socket
import random

app = Flask("Local Server: KivyAuth Login")
app.secret_key = os.urandom(26)

PATH = os.path.dirname(__file__)

port = 9004
ran_num = random.randint(1111, 9999)


def _start_server(*args):
    try:
        app.run(host="127.0.0.1", port=port, ssl_context='adhoc')
    except OSError as e:
        print(e)

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
