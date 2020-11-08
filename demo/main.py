import os

import certifi
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import (MDRectangleFlatIconButton,
                               RectangularElevationBehavior)

from kivyauth import auto_login, login_providers
from kivyauth.facebook_auth import *
from kivyauth.firebase_auth import *
from kivyauth.google_auth import *

os.environ["SSL_CERT_FILE"] = certifi.where()

Toast = autoclass("android.widget.Toast")
String = autoclass("java.lang.String")
CharSequence = autoclass("java.lang.CharSequence")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")

PythonActivity = autoclass("org.kivy.android.PythonActivity")

context = PythonActivity.mActivity
RC_SIGN_IN = 999


@run_on_ui_thread
def show_toast(text):
    t = Toast.makeText(context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT)
    t.show()


kv = """
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
            title: "KivyAuth Demo"
            elevation:9
            opposite_colos: True
            left_action_items: [['menu', lambda x: None]]
            right_action_items: [['source-fork', lambda x: app.send_to_github()]]

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


class RectangleRaisedIconButton(
    MDRectangleFlatIconButton, RectangularElevationBehavior
):
    elevation_normal = 16


class LoginDemo(MDApp):
    current_provider = ""

    def build(self):
        initialize_google(self.after_login, self.error_listener)
        initialize_fb(self.after_login, self.cancel_listener, self.error_listener)
        initialize_firebase(self.after_login, self.error_listener)

        return Builder.load_string(kv)

    def on_resume(self):
        return True

    def on_start(self):

        if auto_login(login_providers.google):
            self.current_provider = login_providers.google
        elif auto_login(login_providers.facebook):
            self.current_provider = login_providers.facebook
        elif auto_login(login_providers.github):
            self.current_provider = login_providers.github
        elif auto_login(login_providers.twitter):
            self.current_provider = login_providers.twitter

    def fb_login(self, *args):
        login_facebook()
        self.current_provider = login_providers.facebook

    def gl_login(self, *args):
        login_google()
        self.current_provider = login_providers.google

    def git_login(self, *args):
        login_github()
        self.current_provider = login_providers.github

    def twitter_login(self, *args):
        login_twitter()
        self.current_provider = login_providers.twitter

    def logout_(self):

        if self.current_provider == login_providers.google:
            logout_google(self.after_logout)
        if self.current_provider == login_providers.facebook:
            logout_facebook(self.after_logout)
        if self.current_provider == login_providers.github:
            logout_github(self.after_logout)
        if self.current_provider == login_providers.twitter:
            logout_twitter(self.after_logout)

    def after_login(self, name, email, photo_uri):
        show_toast("Logged in using {}".format(self.current_provider))
        self.root.current = "homescreen"
        self.update_ui(name, email, photo_uri)

    def after_logout(self):
        self.update_ui("", "", "")
        self.root.current = "loginscreen"
        show_toast("Logged out from {} login".format(self.current_provider))

    def update_ui(self, name, email, photo_uri):
        self.root.ids.home_screen.ids.user_photo.add_widget(
            AsyncImage(
                source=photo_uri, size_hint=(None, None), height=dp(60), width=dp(60)
            )
        )
        self.root.ids.home_screen.ids.user_name.title = "Welcome, {}".format(name)
        self.root.ids.home_screen.ids.user_email.text = (
            "Your Email: {}".format(email)
            if email
            else "Your Email: Could not fetch email"
        )

    def cancel_listener(self):
        show_toast("Login cancelled")

    def error_listener(self):
        show_toast("Error logging in.")

    def send_to_github(self):
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse("https://github.com/shashi278/social-auth-kivy"))

        context.startActivity(intent)


if __name__ == "__main__":
    LoginDemo().run()
