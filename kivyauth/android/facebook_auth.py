from android.activity import bind as result_bind
from jnius import PythonJavaClass, autoclass, cast, java_method
from kivy.logger import Logger

CallbackManagerFactory = autoclass("com.facebook.CallbackManager$Factory")
FacebookSdk = autoclass("com.facebook.FacebookSdk")
LoginManager = autoclass("com.facebook.login.LoginManager")
AccessToken = autoclass("com.facebook.AccessToken")
GraphRequest = autoclass("com.facebook.GraphRequest")
ImageRequest = autoclass("com.facebook.internal.ImageRequest")

Bundle = autoclass("android.os.Bundle")
Arrays = autoclass("java.util.Arrays")

PythonActivity = autoclass("org.kivy.android.PythonActivity")

context = PythonActivity.mActivity
mLoginMgr = None
mList = None


__all__ = ("initialize_fb", "login_facebook", "logout_facebook")


class PythonGraphJSONObjectCallback(PythonJavaClass):
    __javainterfaces__ = ["com/facebook/GraphRequest$GraphJSONObjectCallback"]
    __javacontext__ = "app"

    def __init__(self, complete_listener):
        self.complete_listener = complete_listener
        super().__init__()

    @java_method("(Lorg/json/JSONObject;Lcom/facebook/GraphResponse;)V")
    def onCompleted(self, me, response):
        if response.getError():
            # handle error
            Logger.error("KivyAuth: Unable to retrieve profile info")

        else:

            if AccessToken.isCurrentAccessTokenActive():
                access_token = AccessToken.getCurrentAccessToken().getToken()
            else:
                access_token = ""

            uri = ImageRequest.getProfilePictureUri(
                me.optString("id"), 200, 200, access_token
            )

            Logger.info(
                "KivyAuth: Profile info retrieved successfully."
                " Calling success listener."
            )

            self.complete_listener(
                me.optString("first_name") + " " + me.optString("last_name"),
                me.optString("email"),
                uri.toString() if uri else '',
            )


class PythonFacebookCallback(PythonJavaClass):
    __javainterfaces__ = ["com/facebook/FacebookCallback"]
    __javacontext__ = "app"

    def __init__(self, success_listener, cancel_listener, error_listener):
        self.success_listener = success_listener
        self.cancel_listener = cancel_listener
        self.error_listener = error_listener

    @java_method("(Ljava/lang/Object;)V")
    def onSuccess(self, result):
        Logger.info("KivyAuth: Login success. Requesting profile info.")

        request = GraphRequest.newMeRequest(
            result.getAccessToken(),
            PythonGraphJSONObjectCallback(self.success_listener),
        )

        params = Bundle()
        params.putString("fields", "last_name,first_name,email")
        request.setParameters(params)
        request.executeAsync()

    @java_method("()V")
    def onCancel(self):
        Logger.info("KivyAuth: Login Cancelled.")
        self.cancel_listener()

    @java_method("(Lcom/facebook/FacebookException;)V")
    def onError(self, error):
        Logger.error("KivyAuth: Error logging in.")
        self.error_listener()


def initialize_fb(success_listener, error_listener, *args, **kwargs):
    """
    Function to initialize facebook login.
    Must be called inside `build` method of kivy App before actual login.

    :param: `success_listener` - Function to be called on login success
    :param: `error_listener` - Function to be called on login error
    """
    FacebookSdk.sdkInitialize(context.getApplicationContext())
    mCallbackManager = CallbackManagerFactory.create()
    mFacebookCallback = PythonFacebookCallback(
        success_listener, error_listener, error_listener
    )
    result_bind(on_activity_result=mCallbackManager.onActivityResult)

    Logger.info("KivyAuth: Initialized facebook signin")
    global mList
    mList = [mCallbackManager, mFacebookCallback]


def login_facebook():
    """
    Function to login using facebook
    """
    Logger.info("KivyAuth: Initiated facebook login")
    global mLoginMgr
    mLoginMgr = LoginManager.getInstance()
    mLoginMgr.registerCallback(*mList)
    mLoginMgr.logInWithReadPermissions(
        cast(autoclass("android.app.Activity"), context),
        Arrays.asList("email", "public_profile"),
    )


def auto_facebook():
    """
    Auto login using Facebook. You may call it `on_start`.
    """
    accessToken = AccessToken.getCurrentAccessToken()
    if accessToken and not accessToken.isExpired():
        login_facebook()
        return True


def logout_facebook(after_logout):
    """
    Logout from facebook login

    :param: `after_logout` - Function to be called after logging out
    """
    mLoginMgr.logOut()
    after_logout()
    Logger.info("KivyAuth: Logged out from facebook login")
