from kivy.logger import Logger
from kivy.utils import platform

if platform != "android":
    Logger.error(
        "KivyAuth: KivyAuth currently only supports android platform.")
    exit(1)

__all__ = ("login_providers", "auto_login")


class LoginProviders:
    google = "google"
    facebook = "facebook"
    github = "github"
    twitter = "twitter"


login_providers = LoginProviders()


def auto_login(provider):
    """
    Auto login using a given provider. You may call it `on_start`.

    :param: `provider` is one of `kivyauth.login_providers`
    """
    if provider == login_providers.google:
        from kivyauth.google_auth import auto_google

        return auto_google()

    if provider == login_providers.facebook:
        from kivyauth.facebook_auth import auto_facebook

        return auto_facebook()

    if provider == login_providers.github:
        from kivyauth.firebase_auth import auto_firebase

        return auto_firebase()

    if provider == login_providers.twitter:
        from kivyauth.firebase_auth import auto_firebase

        return auto_firebase()
