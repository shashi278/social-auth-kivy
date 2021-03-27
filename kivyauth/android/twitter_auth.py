from kivy.logger import Logger
from kivyauth.android.firebase_auth import (
    firebase_login,
    firebase_logout,
    initialize_firebase,
    OAuthProvider,
    auto_firebase as auto_twitter,
)

__all__ = ("initialize_twitter", "login_twitter", "logout_twitter")


def initialize_twitter(succes_listener, error_listener, *args, **kwargs):
    initialize_firebase(succes_listener, error_listener)


def login_twitter():
    """
    Function to login using twitter
    """
    Logger.info("KivyAuth: Initiated twitter login")
    provider = OAuthProvider.newBuilder("twitter.com")
    firebase_login(provider)


def logout_twitter(after_logout):
    """
    Logout from twitter login

    :param: `after_logout` - Function to be called after logging out
    """
    firebase_logout(after_logout)
