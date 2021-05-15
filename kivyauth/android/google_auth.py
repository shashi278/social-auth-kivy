from android.activity import bind as result_bind
from jnius import autoclass
from kivy.clock import mainthread
from kivy.logger import Logger

Gso = autoclass("com.google.android.gms.auth.api.signin.GoogleSignInOptions")
GsoBuilder = autoclass(
    "com.google.android.gms.auth.api.signin.GoogleSignInOptions$Builder"
)
GSignIn = autoclass("com.google.android.gms.auth.api.signin.GoogleSignIn")
ApiException = autoclass("com.google.android.gms.common.api.ApiException")
PythonActivity = autoclass("org.kivy.android.PythonActivity")
context = PythonActivity.mActivity

RC_SIGN_IN = 10122
mGSignInClient = None
event_success_listener = None

__all__ = ("initialize_google", "login_google", "logout_google")


class GoogleActivityListener:
    def __init__(self, success_listener, error_listener):
        self.success_listener = success_listener
        self.error_listener = error_listener

    def google_activity_listener(self, request_code, result_code, data):
        if request_code == RC_SIGN_IN:
            Logger.info("KivyAuth: google_activity_listener called.")
            task = GSignIn.getSignedInAccountFromIntent(data)
            try:
                account = task.getResult(ApiException)
                _call_success(account)

            except Exception as e:
                Logger.info("KivyAuth: Error signing in using Google. {}".format(e))
                self.error_listener()


def _call_success(account):
    if account:
        Logger.info("KivyAuth: Google Login success. Calling success listener.")
        event_success_listener(
            account.getDisplayName(),
            account.getEmail(),
            account.getPhotoUrl().toString() if account.getPhotoUrl() else '',
        )
        return True


def initialize_google(success_listener, error_listener, *args, **kwargs):
    """
    Function to initialize google login.
    Must be called inside `build` method of kivy App before actual login.

    :param: `success_listener` - Function to be called on login success
    :param: `error_listener` - Function to be called on login error
    """
    global event_success_listener
    event_success_listener = success_listener
    gso = GsoBuilder(Gso.DEFAULT_SIGN_IN).requestEmail().build()
    global mGSignInClient
    mGSignInClient = GSignIn.getClient(context, gso)
    gal = GoogleActivityListener(success_listener, error_listener)
    result_bind(on_activity_result=gal.google_activity_listener)

    Logger.info("KivyAuth: Initialized google signin")


# @mainthread
def login_google():
    """
    Function to login using google
    """
    Logger.info("KivyAuth: Initiated google login")
    signInIntent = mGSignInClient.getSignInIntent()
    context.startActivityForResult(signInIntent, RC_SIGN_IN)


def auto_google():
    """
    Auto login using Google. You may call it `on_start`.
    """
    account = GSignIn.getLastSignedInAccount(context)
    return _call_success(account)


def logout_google(after_logout):
    """
    Logout from google login

    :param: `after_logout` - Function to be called after logging out
    """
    mGSignInClient.signOut()
    after_logout()
    Logger.info("KivyAuth: Logged out from google login")
