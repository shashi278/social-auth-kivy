from kivy.utils import platform

if platform == "android":

    def stop_login(*args):
        pass


elif platform != "ios":
    from kivyauth.desktop.utils import stop_login


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
    if platform == "android":
        if provider == login_providers.google:
            from kivyauth.android.google_auth import auto_google

            return auto_google()

        if provider == login_providers.facebook:
            from kivyauth.android.facebook_auth import auto_facebook

            return auto_facebook()

        if provider == login_providers.github:
            from kivyauth.android.github_auth import auto_github

            return auto_github()

        if provider == login_providers.twitter:
            from kivyauth.android.twitter_auth import auto_twitter

            return auto_twitter()

    else:
        raise NotImplementedError("Not yet availabe for desktop")
