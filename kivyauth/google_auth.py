from kivy.utils import platform

if platform == "android":
    from kivyauth.android.google_auth import (
        initialize_google,
        login_google,
        logout_google,
    )

elif platform != "ios":
    from kivyauth.desktop.google_auth import (
        initialize_google,
        login_google,
        logout_google,
    )
