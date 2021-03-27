from kivy.utils import platform

if platform == "android":
    from kivyauth.android.facebook_auth import (
        initialize_fb,
        login_facebook,
        logout_facebook,
    )

elif platform != "ios":
    from kivyauth.desktop.facebook_auth import (
        initialize_fb,
        login_facebook,
        logout_facebook,
    )
