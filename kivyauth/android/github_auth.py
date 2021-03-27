from kivy.logger import Logger
from kivyauth.android.firebase_auth import (
    firebase_login,
    firebase_logout,
    initialize_firebase,
    OAuthProvider,
    auto_firebase as auto_github,
)

__all__ = ("initialize_github", "login_github", "logout_github")


def initialize_github(succes_listener, error_listener, *args, **kwargs):
    initialize_firebase(succes_listener, error_listener)


def login_github():
    """
    Function to login using github
    """
    Logger.info("KivyAuth: Initiated github login")
    provider = OAuthProvider.newBuilder("github.com")
    firebase_login(provider)


def logout_github(after_logout):
    """
    Logout from github login

    :param: `after_logout` - Function to be called after logging out
    """
    firebase_logout(after_logout)
