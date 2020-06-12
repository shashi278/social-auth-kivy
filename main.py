from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.button import RectangularElevationBehavior, MDRectangleFlatIconButton
from kivymd.uix.toolbar import MDToolbar

from jnius import autoclass, cast, PythonJavaClass, java_method, JavaClass, MetaJavaClass
from android.activity import bind as result_bind
from android.runnable import run_on_ui_thread

#----For Google Login----#
Gso= autoclass('com.google.android.gms.auth.api.signin.GoogleSignInOptions')
GsoBuilder= autoclass('com.google.android.gms.auth.api.signin.GoogleSignInOptions$Builder')
GSignIn= autoclass('com.google.android.gms.auth.api.signin.GoogleSignIn')
ApiException= autoclass('com.google.android.gms.common.api.ApiException')

#----For Facebook Login----#
AccessToken= autoclass('com.facebook.AccessToken')
CallbackManagerFactory= autoclass('com.facebook.CallbackManager$Factory')
FacebookCallback= autoclass('com.facebook.FacebookCallback')
FacebookException= autoclass('com.facebook.FacebookException')
FacebookSdk= autoclass('com.facebook.FacebookSdk')
LoginManager= autoclass('com.facebook.login.LoginManager')
GraphRequest= autoclass('com.facebook.GraphRequest')
ImageRequest= autoclass('com.facebook.internal.ImageRequest')

#----Firebase classes for Github and Twitter Login----#
FirebaseAuth= autoclass('com.google.firebase.auth.FirebaseAuth')
FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
OAuthProvider = autoclass('com.google.firebase.auth.OAuthProvider')
FirebaseUser = autoclass('com.google.firebase.auth.FirebaseUser')

Arrays= autoclass('java.util.Arrays')
Toast= autoclass('android.widget.Toast')
String = autoclass('java.lang.String')
CharSequence= autoclass('java.lang.CharSequence')
Bundle= autoclass('android.os.Bundle')

PythonActivity= autoclass('org.kivy.android.PythonActivity')

context= PythonActivity.mActivity
RC_SIGN_IN= 999
current_provider= ""

@run_on_ui_thread
def show_toast(text):
    t= Toast.makeText(context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT)
    t.show()

def activity_listener_google(request_code, result_code, data):
    if request_code== RC_SIGN_IN:
        task= GSignIn.getSignedInAccountFromIntent(data)
        try:
            account= task.getResult(ApiException)
            if account:
                show_toast("Logged in using Google")

                global current_provider
                current_provider='google'
                
                app= App.get_running_app()
                app.after_login(
                    account.getDisplayName(),
                    account.getEmail(),
                    account.getPhotoUrl().toString()
                    )
            
            else:
                show_toast("Could not get account")

        except Exception as e:
            show_toast("Error signing in using Google")


kv="""
#:import Clock kivy.clock.Clock
ScreenManager:
    
    LoginScreen:
        id: login_screen
    
    HomeScreen:
        id: home_screen

<LoginScreen>:
    name:"loginscreen"
    BoxLayout:
        orientation:"vertical"

        MDToolbar:
            title: "Social Auth Kivy Demo"
            elevation:9
            opposite_colos: True
            left_action_items: [['menu', lambda x: None]]
            right_action_items: [['information-outline', lambda x: None]]

        BoxLayout:
            orientation:"vertical"

            Widget:
                size_hint_y: None
                height: dp(100)

            LoginButton
                text: "Sign In with Google"
                icon: "google"
                text_color: 1,1,1,1
                can_color: 66/255, 133/255, 244/255, 1
                release_action: app.gl_login
            
            LoginButton
                text: "Sign In with Facebook"
                icon: "facebook-box"
                text_color: 1,1,1,1
                can_color: 59/255, 89/255, 152/255, 1
                release_action: app.fb_login
            
            LoginButton
                text: "Sign In with Github"
                icon: "github-circle"
                text_color: 1,1,1,1
                can_color: 33/255, 31/255, 31/255, 1
                release_action: app.git_login
            
            LoginButton
                text: "Sign In with Twitter"
                icon: "twitter"
                text_color: 1,1,1,1
                can_color: 8/255, 160/255, 233/255, 1
                release_action: app.twitter_login
            
            Widget:
                size_hint_y: None
                height: dp(100)

<LoginButton@AnchorLayout>:
    text:""
    icon: ""
    text_color: [0,0,0,1]
    can_color: 1,1,1,1
    release_action: print
    RectangleRaisedIconButton:
        elevation:8
        width: dp(270)
        height: dp(50)
        canvas.before:
            Color:
                rgba: root.can_color
            Rectangle:
                pos: self.pos
                size: self.size
        
        icon: root.icon
        text: root.text
        font_size: dp(8)
        text_color: root.text_color
        on_release:
            if root.release_action: Clock.schedule_once(root.release_action, 0)
        

<HomeScreen@Screen>:
    name:"homescreen"

    BoxLayout:
        id: main_box
        orientation:"vertical"

        MDToolbar:
            id: user_name
            title: ""
            elevation:9
            opposite_colos: True
            left_action_items: [['menu', lambda x: None]]
            right_action_items: [['information-outline', lambda x: None]]
        
        AnchorLayout:
            id: user_photo

        BoxLayout:
            size_hint_y:None
            height: dp(20)
            padding: dp(5)
            
            MDLabel:
                id: user_email
                halign: "center"
                font_style: "Body1"
                text: ""

        AnchorLayout:
            MDRaisedButton:
                text: "LOGOUT"
                md_bg_color: .9,.9,.9,1
                theme_text_color: "Custom"
                font_color: 0,0,0,1
                text_color: 0,0,0,1
                on_release:
                    app.logout()




"""

class LoginScreen(Screen):
    pass

class RectangleRaisedIconButton(MDRectangleFlatIconButton, RectangularElevationBehavior):
    elevation_normal=16

class PythonGraphJSONObjectCallback(PythonJavaClass):
    __javainterfaces__= ['com/facebook/GraphRequest$GraphJSONObjectCallback']
    __javacontext__= 'app'

    @java_method('(Lorg/json/JSONObject;Lcom/facebook/GraphResponse;)V')
    def onCompleted(self, me, response):
        if response.getError():
            #handle error
            show_toast('Error retrieving profile info')
            
        else:
            
            #Logger.info('Hahaha: json_obj= {}'.format(me.toString()))
            #Logger.info('Hahaha: graph_resp= {}'.format(response.toString()))

            if AccessToken.isCurrentAccessTokenActive():
                access_token= AccessToken.getCurrentAccessToken().getToken()
            else:
                access_token= ""
            
            uri= ImageRequest.getProfilePictureUri(
                me.optString("id"),
                100,
                100,
                access_token
            )
            
            global current_provider
            current_provider= "facebook"

            app= App.get_running_app()
            app.after_login(
                me.optString("first_name")+" "+me.optString("last_name"),
                me.optString("email"),
                uri.toString()
                )

class PythonFacebookCallback(PythonJavaClass):
    __javainterfaces__= ['com/facebook/FacebookCallback']
    __javacontext__= 'app'

    @java_method('(Ljava/lang/Object;)V')
    def onSuccess(self, result):
        
        request= GraphRequest.newMeRequest(
            result.getAccessToken(),
            PythonGraphJSONObjectCallback()
        )

        params= Bundle()
        params.putString("fields", "last_name,first_name,email")
        request.setParameters(params)
        request.executeAsync()

        show_toast("Logged in using Facebook")


    @java_method('()V')
    def onCancel(self):
        show_toast("Login Canceled")

    @java_method('(Lcom/facebook/FacebookException;)V')
    def onError(self, error):
        show_toast("Login Error")

class OnSuccessListener(PythonJavaClass):
    __javainterfaces__=['com/google/android/gms/tasks/OnSuccessListener']
    __javacontext__= 'app'

    def __init__(self, provider):
        self.provider= provider

    @java_method('(Ljava/lang/Object;)V')
    def onSuccess(self, result):
        #user is signed in
        Logger.info('hahaha: OnSuccess={}'.format(result))
        user = FirebaseAuth.getInstance().getCurrentUser()
        #Logger.info('hahaha: userInfo-DisplayName= {}'.format(user.getDisplayName()))
        #Logger.info('hahaha: userInfo-Email= {}'.format(user.getEmail()))
        #Logger.info('hahaha: userInfo-photo= {}'.format(user.getPhotoUrl().toString()))

        show_toast("Logged in using {}".format(self.provider))

        global current_provider
        current_provider=self.provider
        
        app= App.get_running_app()
        app.after_login(
            user.getDisplayName(),
            user.getEmail(),
            user.getPhotoUrl().toString()
            )

class OnFailureListener(PythonJavaClass):
    __javainterfaces__=['com/google/android/gms/tasks/OnFailureListener']
    __javacontext__= 'app'

    @java_method('(Ljava/lang/Exception;)V')
    def onFailure(self, e):
        #handle exception
        Logger.info('hahaha: OnFailure={}'.format(e))
        show_toast("Error Logging in using Github or twitter")
        

class LoginDemo(MDApp):
    def build(self):
        self.mAuth= FirebaseAuth.getInstance()
        
        gso= GsoBuilder(Gso.DEFAULT_SIGN_IN).requestEmail().build()
        self.mGSignInClient= GSignIn.getClient(context, gso)
        result_bind(on_activity_result=activity_listener_google)

        FacebookSdk.sdkInitialize(context.getApplicationContext())
        mCallbackManager = CallbackManagerFactory.create()
        mFacebookCallback= PythonFacebookCallback()
        self.mLoginMgr = LoginManager.getInstance()
        self.mLoginMgr.registerCallback(mCallbackManager, mFacebookCallback)
        result_bind(on_activity_result=mCallbackManager.onActivityResult)

        return Builder.load_string(kv)
    
    def on_resume(self):
        return True
    
    def on_start(self):
        # If a user is logged in, send them to login page on start
        # Since we've different providers here, you need to check them all &
        # login using your priority if logged in with more than one provider
        # Below is an example of fb login. Refer to other providers' doc for their
        # implementations

        #accessToken = AccessToken.getCurrentAccessToken()
        #if accessToken and not accessToken.isExpired():
        #    self.fb_login()
        pass
    
    def fb_login(self, *args):
        self.mLoginMgr.logInWithReadPermissions(
                cast(autoclass('android.app.Activity'),
                context), Arrays.asList("email", "public_profile")
                )
    
    def gl_login(self, *args):
        signInIntent= self.mGSignInClient.getSignInIntent()
        context.startActivityForResult(signInIntent, RC_SIGN_IN)
    
    def git_login(self, *args):
        provider = OAuthProvider.newBuilder("github.com")
        pendingResultTask = FirebaseAuth.getPendingAuthResult()
        if pendingResultTask:
            #There's something already here! Finish the sign-in for your user.

            task= pendingResultTask.addOnSuccessListener(OnSuccessListener("github"))
            task= task.addOnFailureListener(OnFailureListener())
        else:
            #There's no pending result so you need to start the sign-in flow.

            task= FirebaseAuth.startActivityForSignInWithProvider(context, provider.build())
            task= task.addOnSuccessListener(OnSuccessListener("github"))
            task= task.addOnFailureListener(OnFailureListener())
        

    def twitter_login(self, *args):
        provider = OAuthProvider.newBuilder("twitter.com")
        pendingResultTask = FirebaseAuth.getPendingAuthResult()
        if pendingResultTask:
            #There's something already here! Finish the sign-in for your user.

            task= pendingResultTask.addOnSuccessListener(OnSuccessListener("twitter"))
            task= task.addOnFailureListener(OnFailureListener())
        else:
            #There'
            


            task= FirebaseAuth.startActivityForSignInWithProvider(context, provider.build())
            task= task.addOnSuccessListener(OnSuccessListener("twitter"))
            task= task.addOnFailureListener(OnFailureListener())


    def logout(self):
        Logger.info("hahaha: provider= {}".format(current_provider))
        if current_provider=="facebook":
            self.mLoginMgr.logOut()
            show_toast('Logged out from facebook')
        elif current_provider=="google":
            self.mGSignInClient.signOut()
            show_toast('Logged out from google')
        elif current_provider=="github":
            FirebaseAuth.getInstance().signOut()
            show_toast('Logged out from github')
        elif current_provider=="twitter":
            FirebaseAuth.getInstance().signOut()
            show_toast('Logged out from twitter')

        self.after_logout()

    def after_login(self, name, email, photo_uri):
        self.update_ui(name, email, photo_uri)

    def after_logout(self):
        self.root.current= 'loginscreen'
    
    def update_ui(self, name, email, photo_uri):
        self.root.current= 'homescreen'
        self.root.ids.home_screen.ids.user_photo.add_widget(AsyncImage(source=photo_uri, size_hint=(None, None), height=dp(60), width=dp(60)))
        self.root.ids.home_screen.ids.user_name.title= "Welcome, {}".format(name)
        self.root.ids.home_screen.ids.user_email.text= "Your Email: {}".format(email) if email else "Your Email: Could not fetch email"

if __name__ == "__main__":
    LoginDemo().run()