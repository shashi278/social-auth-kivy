from kivy.logger import Logger

from jnius import autoclass, PythonJavaClass, java_method

GSignIn = autoclass("com.google.android.gms.auth.api.signin.GoogleSignIn")
ApiException = autoclass("com.google.android.gms.common.api.ApiException")
FirebaseAuth = autoclass("com.google.firebase.auth.FirebaseAuth")


class GoogleActivityListener:
    def __init__(self, success_listener, error_listener, RC_SIGN_IN):
        self.success_listener = success_listener
        self.error_listener = error_listener
        self.RC_SIGN_IN = RC_SIGN_IN

    def google_activity_listener(self, request_code, result_code, data):
        Logger.info("KivyAuth: google_activity_listener called.")
        if request_code == self.RC_SIGN_IN:
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
                Logger.info("KivyAuth: Error signing in using Google.")
                self.error_listener()


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
