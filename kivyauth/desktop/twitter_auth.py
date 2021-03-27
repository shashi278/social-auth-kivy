__all__ = ("initialize_twitter", "login_twitter", "logout_twitter")


def initialize_twitter(
    success_listener, error_listener, client_id=None, client_secret=None
):
    raise NotImplementedError


def login_twitter():
    raise NotImplementedError


def logout_twitter():
    raise NotImplementedError
