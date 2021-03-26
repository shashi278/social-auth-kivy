from kivy import platform
from kivy.logger import Logger
from kivyauth.desktop.utils import _close_server_pls, port

def stop_login(*args):
    _close_server_pls(port)

if platform == "android":
    Logger.error("KivyAuth: Seems like you tried from kivyauth.android while being on a non-android device. Import from kivyauth.desktop")