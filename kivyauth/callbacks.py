from kivy.logger import Logger
from jnius import autoclass, PythonJavaClass, java_method

AccessToken = autoclass("com.facebook.AccessToken")
GraphRequest = autoclass("com.facebook.GraphRequest")
ImageRequest = autoclass("com.facebook.internal.ImageRequest")

Bundle = autoclass("android.os.Bundle")


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
                me.optString("id"), 100, 100, access_token
            )

            Logger.info(
                "KivyAuth: Profile info retrieved successfully."
                " Calling success listener."
            )

            self.complete_listener(
                me.optString("first_name") + " " + me.optString("last_name"),
                me.optString("email"),
                uri.toString(),
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
