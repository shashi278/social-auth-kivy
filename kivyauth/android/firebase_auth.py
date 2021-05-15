from android.activity import bind as result_bind
from jnius import PythonJavaClass, autoclass, java_method
from kivy.logger import Logger

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

        _call_success(user)


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


def _call_success(user):
    event_success_listener(
        user.getDisplayName(),
        user.getEmail(),
        user.getPhotoUrl().toString() if user.getPhotoUrl() else ''
    )


def initialize_firebase(success_listener, error_listener):
    """
    Function to initialize firebase login.
    Must be called inside `build` method of kivy App before actual login.

    :param: `success_listener` - Function to be called on login success
    :param: `error_listener` - Function to be called on login error
    """
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
        task = task.addOnFailureListener(OnFailureListener(event_error_listener))
    else:
        # There's no pending result so you need to start the sign-in flow.

        task = FirebaseAuth.startActivityForSignInWithProvider(
            context, provider.build()
        )
        task = task.addOnSuccessListener(OnSuccessListener(event_success_listener))
        task = task.addOnFailureListener(OnFailureListener(event_error_listener))


def firebase_logout(after_logout):
    Logger.info("KivyAuth: Initiated logout using firebase")
    FirebaseAuth.getInstance().signOut()
    after_logout()
    Logger.info("KivyAuth: Logged out from firebase auth")


def auto_firebase():
    user = FirebaseAuth.getInstance().getCurrentUser()
    if user:
        _call_success(user)
        return True


def login_github():
    """
    Function to login using github
    """
    Logger.info("KivyAuth: Initiated github login")
    provider = OAuthProvider.newBuilder("github.com")
    firebase_login(provider)


def login_twitter():
    """
    Function to login using twitter
    """
    Logger.info("KivyAuth: Initiated twitter login")
    provider = OAuthProvider.newBuilder("twitter.com")
    firebase_login(provider)


def logout_twitter(after_logout):
    """
    Logout from twitter login

    :param: `after_logout` - Function to be called after logging out
    """
    firebase_logout(after_logout)


def logout_github(after_logout):
    """
    Logout from github login

    :param: `after_logout` - Function to be called after logging out
    """
    firebase_logout(after_logout)
