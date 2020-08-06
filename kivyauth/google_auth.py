from kivy.logger import Logger
from kivy.clock import mainthread
from jnius import autoclass
from android.activity import bind as result_bind

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
                if account:
                    Logger.info(
                        "KivyAuth: Google Login success.\
                         Calling success listener."
                    )
                    self.success_listener(
                        account.getDisplayName(),
                        account.getEmail(),
                        account.getPhotoUrl().toString(),
                    )

            except Exception as e:
                Logger.info(
                    "KivyAuth: Error signing in using Google. {}".format(e)
                    )
                self.error_listener()


def initialize_google(success_listener, error_listener):
    gso = GsoBuilder(Gso.DEFAULT_SIGN_IN).requestEmail().build()
    global mGSignInClient
    mGSignInClient = GSignIn.getClient(context, gso)
    gal = GoogleActivityListener(success_listener, error_listener)
    result_bind(on_activity_result=gal.google_activity_listener)

    Logger.info("KivyAuth: Initialized google signin")


# @mainthread
def login_google():
    Logger.info("KivyAuth: Initiated google login")
    signInIntent = mGSignInClient.getSignInIntent()
    context.startActivityForResult(signInIntent, RC_SIGN_IN)


def logout_google(after_logout):
    mGSignInClient.signOut()
    after_logout()
    Logger.info("KivyAuth: Logged out from google login")
