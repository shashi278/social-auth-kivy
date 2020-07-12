from kivy.logger import Logger
from kivy.clock import mainthread
from jnius import autoclass, cast

from kivyauth.listeners import OnSuccessListener, OnFailureListener

LoginManager = autoclass("com.facebook.login.LoginManager")
FirebaseAuth = autoclass("com.google.firebase.auth.FirebaseAuth")
OAuthProvider = autoclass("com.google.firebase.auth.OAuthProvider")

Arrays = autoclass("java.util.Arrays")

PythonActivity = autoclass("org.kivy.android.PythonActivity")
context = PythonActivity.mActivity

mMgr = None
mClient = None


@mainthread
def login_google(mGSignInClient, RC_SIGN_IN, *args):
    Logger.info("KivyAuth: Initiated google login")
    global mClient
    mClient = mGSignInClient
    signInIntent = mGSignInClient.getSignInIntent()
    context.startActivityForResult(signInIntent, RC_SIGN_IN)


@mainthread
def login_facebook(mList, *args):
    Logger.info("KivyAuth: Initiated facebook login")
    mLoginMgr = LoginManager.getInstance()
    mLoginMgr.registerCallback(*mList)
    mLoginMgr.logInWithReadPermissions(
        cast(autoclass("android.app.Activity"), context),
        Arrays.asList("email", "public_profile"),
    )

    global mMgr
    mMgr = mLoginMgr


@mainthread
def login_github(success_listener, error_listener):
    Logger.info("KivyAuth: Initiated github login")
    provider = OAuthProvider.newBuilder("github.com")
    firebase_auth(provider, success_listener, error_listener)


@mainthread
def login_twitter(success_listener, error_listener):
    Logger.info("KivyAuth: Initiated twitter login")
    provider = OAuthProvider.newBuilder("twitter.com")
    firebase_auth(provider, success_listener, error_listener)


def firebase_auth(provider, success_listener, error_listener):
    pendingResultTask = FirebaseAuth.getPendingAuthResult()
    if pendingResultTask:
        # There's something already here! Finish the sign-in for your user.

        task = pendingResultTask.addOnSuccessListener(
            OnSuccessListener(success_listener)
        )
        task = task.addOnFailureListener(OnFailureListener(error_listener))
    else:
        # There's no pending result so you need to start the sign-in flow.

        task = FirebaseAuth.startActivityForSignInWithProvider(
            context, provider.build()
        )
        task = task.addOnSuccessListener(OnSuccessListener(success_listener))
        task = task.addOnFailureListener(OnFailureListener(error_listener))


def logout(current_provider, after_logout):
    Logger.info("KivyAuth: Initiated logout")
    if current_provider == "facebook":
        mMgr.logOut()
        after_logout()
        Logger.info("KivyAuth: Logged out from google login")

    elif current_provider == "google":
        mClient.signOut()
        after_logout()
        Logger.info("KivyAuth: Logged out from facebook login")

    elif current_provider in ("github", "twitter"):
        FirebaseAuth.getInstance().signOut()
        after_logout()
        Logger.info("KivyAuth: Logged out from firebase auth")


class LoginProviders:
    google = "google"
    facebook = "facebook"
    github = "github"
    twitter = "twitter"


login_providers = LoginProviders()
