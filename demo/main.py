from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
from kivy.metrics import dp

import os

from kivyauth.initialize import initialize_google, initialize_fb, initialize_firebase
from kivyauth.logins import login_google, login_facebook, login_github, login_twitter, logout, login_providers

from kivymd.app import MDApp
from kivymd.uix.button import RectangularElevationBehavior, MDRectangleFlatIconButton
from kivymd.uix.toolbar import MDToolbar

from jnius import autoclass, cast
from android.runnable import run_on_ui_thread

import certifi

os.environ['SSL_CERT_FILE']= certifi.where()

Toast= autoclass('android.widget.Toast')
String = autoclass('java.lang.String')
CharSequence= autoclass('java.lang.CharSequence')

PythonActivity= autoclass('org.kivy.android.PythonActivity')

context= PythonActivity.mActivity
RC_SIGN_IN= 999
current_provider= ""

@run_on_ui_thread
def show_toast(text):
    t= Toast.makeText(context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT)
    t.show()

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
                    app.logout_()


"""

class LoginScreen(Screen):
    pass

class RectangleRaisedIconButton(MDRectangleFlatIconButton, RectangularElevationBehavior):
    elevation_normal=16
        
class LoginDemo(MDApp):
    def build(self):

        self.mGSignInClient= initialize_google(self.after_login, self.error_listener, RC_SIGN_IN)
        self.mList= initialize_fb(self.after_login, self.cancel_listener, self.error_listener)
        initialize_firebase()

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
        login_facebook(self.mList)
        global current_provider
        current_provider= login_providers.facebook
        
    def gl_login(self, *args):
        login_google(self.mGSignInClient, RC_SIGN_IN)
        global current_provider
        current_provider= login_providers.google
    
    def git_login(self, *args):
        login_github(self.after_login, self.error_listener)
        global current_provider
        current_provider= login_providers.github

    def twitter_login(self, *args):
        login_twitter(self.after_login, self.error_listener)
        global current_provider
        current_provider= login_providers.twitter

    def logout_(self):
        logout(current_provider, self.after_logout)

    def after_login(self, name, email, photo_uri):
        show_toast('Logged in using {}'.format(current_provider))
        self.root.current= 'homescreen'
        self.update_ui(name, email, photo_uri)

    def after_logout(self):
        self.update_ui('','','')
        self.root.current= 'loginscreen'
        show_toast('Logged out from {} login'.format(current_provider))
    
    def update_ui(self, name, email, photo_uri):
        self.root.ids.home_screen.ids.user_photo.add_widget(AsyncImage(source=photo_uri, size_hint=(None, None), height=dp(60), width=dp(60)))
        self.root.ids.home_screen.ids.user_name.title= "Welcome, {}".format(name)
        self.root.ids.home_screen.ids.user_email.text= "Your Email: {}".format(email) if email else "Your Email: Could not fetch email"

    def cancel_listener(self):
        show_toast("Login cancelled")
    
    def error_listener(self):
        show_toast("Error logging in.")

if __name__ == "__main__":
    LoginDemo().run()
