from kivy.logger import Logger
from jnius import autoclass, PythonJavaClass, java_method
from android.activity import bind as result_bind

FirebaseAuth = autoclass("com.google.firebase.auth.FirebaseAuth")
OAuthProvider = autoclass("com.google.firebase.auth.OAuthProvider")

PythonActivity = autoclass("org.kivy.android.PythonActivity")

context = PythonActivity.mActivity

event_success_listener = None
event_error_listener = None


class OnSuccessListener(PythonJavaClass):
    __javainterfaces__ = ["com/google/android/gms/tasks/OnSuccessListener"]
    __javacontext__ = "app"

    def __init__(self, success_listener):
        self.success_listener = success_listener

    @java_method("(Ljava/lang/Object;)V")
    def onSuccess(self, result):
        # user is signed in
        Logger.info("KivyAuth: Sign in successful using firebase.")
        user = FirebaseAuth.getInstance().getCurrentUser()

        self.success_listener(
            user.getDisplayName(),
            user.getEmail(),
            user.getPhotoUrl().toString()
        )


class OnFailureListener(PythonJavaClass):
    __javainterfaces__ = ["com/google/android/gms/tasks/OnFailureListener"]
    __javacontext__ = "app"

    def __init__(self, error_listener):
        self.error_listener = error_listener

    @java_method("(Ljava/lang/Exception;)V")
    def onFailure(self, e):
        # handle exception
        Logger.info("KivyAuth: Sign in using firebase failed")
        self.error_listener()


def initialize_firebase(success_listener, error_listener):
    FirebaseAuth.getInstance()
    Logger.info("KivyAuth: Initialized firebase auth")
    global event_success_listener
    event_success_listener = success_listener
    global event_error_listener
    event_error_listener = error_listener


def firebase_login(provider):
    pendingResultTask = FirebaseAuth.getPendingAuthResult()
    if pendingResultTask:
        # There's something already here! Finish the sign-in for your user.

        task = pendingResultTask.addOnSuccessListener(
            OnSuccessListener(event_success_listener)
        )
        task = task.addOnFailureListener(
            OnFailureListener(event_error_listener)
            )
    else:
        # There's no pending result so you need to start the sign-in flow.

        task = FirebaseAuth.startActivityForSignInWithProvider(
            context, provider.build()
        )
        task = task.addOnSuccessListener(
            OnSuccessListener(event_success_listener)
            )
        task = task.addOnFailureListener(
            OnFailureListener(event_error_listener)
            )


def firebase_logout(after_logout):
    Logger.info("KivyAuth: Initiated logout using firebase")
    FirebaseAuth.getInstance().signOut()
    after_logout()
    Logger.info("KivyAuth: Logged out from firebase auth")


def login_github():
    Logger.info("KivyAuth: Initiated github login")
    provider = OAuthProvider.newBuilder("github.com")
    firebase_login(provider)


def login_twitter():
    Logger.info("KivyAuth: Initiated twitter login")
    provider = OAuthProvider.newBuilder("twitter.com")
    firebase_login(provider)


def logout_twitter(after_logout):
    firebase_logout(after_logout)


def logout_github(after_logout):
    firebase_logout(after_logout)
