import os
from dotenv import load_dotenv

from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy import platform
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.behaviors.elevation import CommonElevationBehavior

from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivyauth.facebook_auth import initialize_fb, login_facebook, logout_facebook
from kivyauth.github_auth import initialize_github, login_github, logout_github
from kivyauth.twitter_auth import initialize_twitter, login_twitter, logout_twitter
from kivyauth.utils import stop_login
from kivyauth.utils import login_providers, auto_login

load_dotenv()

if platform == "android":
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, cast

    Toast = autoclass("android.widget.Toast")
    String = autoclass("java.lang.String")
    CharSequence = autoclass("java.lang.CharSequence")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    NewRelic = autoclass("com.newrelic.agent.android.NewRelic")
    LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
    AndroidColor = autoclass("android.graphics.Color")

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    context = PythonActivity.mActivity

    @run_on_ui_thread
    def show_toast(text):
        t = Toast.makeText(
            context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT
        )
        t.show()

    @run_on_ui_thread
    def set_statusbar_color():
        window = context.getWindow()
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(AndroidColor.TRANSPARENT)


kv = """
#:import Clock kivy.clock.Clock
#:import platform kivy.platform
ScreenManager:
    
    LoginScreen:
        id: login_screen
    
    HomeScreen:
        id: home_screen

<LoginScreen>:
    name:"loginscreen"
    BoxLayout:
        orientation:"vertical"

        MDTopAppBar:
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
                icon: "facebook"
                text_color: 1,1,1,1
                can_color: 59/255, 89/255, 152/255, 1
                release_action: app.fb_login
            
            LoginButton
                text: "Sign In with Github"
                icon: "github-circle" if platform == "android" else  "github"
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
        width: dp(270)
        height: dp(50)
        canvas.before:
            Color:
                rgba: root.can_color
            Rectangle:
                pos: self.pos
                size: self.size
        

        elevation: 8
        icon: root.icon
        text: root.text
        font_size: dp(8) if platform == "android" else dp(18)
        text_color: root.text_color
        on_release:
            if root.release_action: Clock.schedule_once(root.release_action, 0)
        

<HomeScreen@Screen>:
    name:"homescreen"

    BoxLayout:
        id: main_box
        orientation:"vertical"

        MDTopAppBar:
            id: user_name
            title: ""
            elevation: 9
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
                text_color: 0,0,0,1
                on_release:
                    app.logout_()


<Content>:
    orientation: "vertical"
    size_hint_y: None
    height: "90dp"

    AnchorLayout:
        MDSpinner:
            size_hint: None, None
            size: dp(30), dp(30)
            pos_hint: {'center_x': .5, 'center_y': .5}
    
    AnchorLayout:
        MDLabel:
            text: "Logging in..."
            halign: "center"
"""

class Content(BoxLayout):
    pass

class Content(BoxLayout):
    pass


class LoginScreen(Screen):
    pass


class RectangleRaisedIconButton(
    MDRectangleFlatIconButton, CommonElevationBehavior
):
    pass


class LoginDemo(MDApp):
    current_provider = ""

    def build(self):
        initialize_google(
            self.google_after_login,
            self.error_listener,
            os.getenv("GOOGLE_CLIENT_ID"),
            os.getenv("GOOGLE_CLIENT_SECRET"),
        )
        initialize_fb(
            self.after_login,
            self.error_listener,
            os.getenv("FACEBOOK_CLIENT_ID"),
            os.getenv("FACEBOOK_CLIENT_SECRET"),
        )
        initialize_github(
            self.after_login,
            self.error_listener,
            os.getenv("GITHUB_CLIENT_ID"),
            os.getenv("GITHUB_CLIENT_SECRET"),
        )

        if platform == "android":
            set_statusbar_color()
        tmp = Builder.load_string(kv)
        if platform != "android":
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.button import MDFlatButton

            btn = MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color)
            btn.bind(on_release=lambda *args: (stop_login(), self.dialog.dismiss()))
            self.dialog = MDDialog(
                title="",
                size_hint_x=None,
                size_hint_y=None,
                width="250dp",
                type="custom",
                auto_dismiss=False,
                content_cls=Content(),
                buttons=[btn],
            )
        return tmp

    def on_start(self):
        if platform == "android":
            if auto_login(login_providers.google):
                self.current_provider = login_providers.google
            elif auto_login(login_providers.facebook):
                self.current_provider = login_providers.facebook
            elif auto_login(login_providers.github):
                self.current_provider = login_providers.github
            elif auto_login(login_providers.twitter):
                self.current_provider = login_providers.twitter
            primary_clr= [ 108/255, 52/255, 131/255 ]
            hex_color= '#%02x%02x%02x' % (int(primary_clr[0]*200), int(primary_clr[1]*200), int(primary_clr[2]*200))
            set_statusbar_color()
        pass

    def show_login_progress(self):
        if platform != "android":
            self.dialog.open()

    def hide_login_progress(self):
        if platform != "android":
            self.dialog.dismiss()

    def fb_login(self, *args):
        login_facebook()
        self.current_provider = login_providers.facebook
        self.show_login_progress()

    def gl_login(self, *args):
        login_google()
        self.current_provider = login_providers.google
        self.show_login_progress()

    def git_login(self, *args):
        login_github()
        self.current_provider = login_providers.github
        self.show_login_progress()

    def twitter_login(self, *args):
        login_twitter()
        self.current_provider = login_providers.twitter
        self.show_login_progress()

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
        self.hide_login_progress()

        if platform == "android":
            show_toast("Logged in using {}".format(self.current_provider))
        else:
            Snackbar(text="Logged in using {}".format(self.current_provider)).open()

        self.root.current = "homescreen"
        self.update_ui(name, email, photo_uri)

    def google_after_login(self, *args):
        self.hide_login_progress()

        if platform == 'android':
            keys = ['sub', 'name', 'email', 'family_name', 'given_name',  'picture']
            user_dict = dict(zip(keys, args))
            user_data = user_dict
            show_toast("Logged in using {}".format(self.current_provider))
        else:
            user_data = args[0]
            Snackbar(text="Logged in using {}".format(self.current_provider)).open()

        user_id = user_data['sub']
        user_name = user_data['name']
        user_email = user_data['email']
        user_pic = user_data['picture']

        self.root.current = "homescreen"
        self.update_ui(user_name, user_email, user_pic)

    def after_logout(self):
        self.update_ui("", "", "")
        self.root.current = "loginscreen"
        if platform == "android":
            show_toast(text="Logged out from {} login".format(self.current_provider))
        else:
            Snackbar(
                text="Logged out from {} login".format(self.current_provider)
            ).open()

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

    def error_listener(self):
        if platform == "android":
            show_toast("Error logging in.")
        else:
            Snackbar(text="Error logging in. Check connection or try again.").show()
        Clock.schedule_once(lambda *args: self.hide_login_progress())

    def send_to_github(self):
        if platform == "android":
            intent = Intent()
            intent.setAction(Intent.ACTION_VIEW)
            intent.setData(Uri.parse("https://github.com/shashi278/social-auth-kivy"))

            context.startActivity(intent)
        else:
            import webbrowser
            webbrowser.open("https://github.com/shashi278/social-auth-kivy")


if __name__ == "__main__":
    LoginDemo().run()
