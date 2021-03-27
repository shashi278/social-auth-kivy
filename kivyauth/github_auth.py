from kivy.utils import platform

if platform == "android":
    from kivyauth.android.github_auth import (
        initialize_github,
        login_github,
        logout_github,
    )

elif platform != "ios":
    from kivyauth.desktop.github_auth import (
        initialize_github,
        login_github,
        logout_github,
    )
