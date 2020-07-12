from kivy.logger import Logger
from jnius import autoclass
from android.activity import bind as result_bind

from kivyauth.callbacks import PythonFacebookCallback
from kivyauth.listeners import GoogleActivityListener

# ----For Google Login----#
Gso = autoclass("com.google.android.gms.auth.api.signin.GoogleSignInOptions")
GsoBuilder = autoclass(
    "com.google.android.gms.auth.api.signin.GoogleSignInOptions$Builder"
)
GSignIn = autoclass("com.google.android.gms.auth.api.signin.GoogleSignIn")

# ----For Facebook Login----#
CallbackManagerFactory = autoclass("com.facebook.CallbackManager$Factory")
FacebookSdk = autoclass("com.facebook.FacebookSdk")
LoginManager = autoclass("com.facebook.login.LoginManager")

FirebaseAuth = autoclass("com.google.firebase.auth.FirebaseAuth")

PythonActivity = autoclass("org.kivy.android.PythonActivity")

context = PythonActivity.mActivity


def initialize_google(success_listener, error_listener, RC_SIGN_IN):
    gso = GsoBuilder(Gso.DEFAULT_SIGN_IN).requestEmail().build()
    mGSignInClient = GSignIn.getClient(context, gso)
    gal = GoogleActivityListener(success_listener, error_listener, RC_SIGN_IN)
    result_bind(on_activity_result=gal.google_activity_listener)

    Logger.info("KivyAuth: Initialized google signin")
    return mGSignInClient


def initialize_fb(success_listener, cancel_listener, error_listener):
    FacebookSdk.sdkInitialize(context.getApplicationContext())
    mCallbackManager = CallbackManagerFactory.create()
    mFacebookCallback = PythonFacebookCallback(
        success_listener, cancel_listener, error_listener
    )
    result_bind(on_activity_result=mCallbackManager.onActivityResult)

    Logger.info("KivyAuth: Initialized facebook signin")
    return [mCallbackManager, mFacebookCallback]


def initialize_firebase():
    mAuth = FirebaseAuth.getInstance()

    Logger.info("KivyAuth: Initialized firebase auth")
    return mAuth
