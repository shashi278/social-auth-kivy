from kivy.utils import platform

if platform == "android":
    from kivyauth.android.twitter_auth import (
        initialize_twitter,
        login_twitter,
        logout_twitter,
    )

elif platform != "ios":
    from kivyauth.desktop.twitter_auth import (
        initialize_twitter,
        login_twitter,
        logout_twitter,
    )
