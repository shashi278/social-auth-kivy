from kivy import platform
from kivy.logger import Logger
# from kivy.lang.builder import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivymd.app import MDApp

# MDApp()

content = """
<Content>
    spacing: "12dp"
    size_hint_y: None
    height: "70dp"

    AnchorLayout:
        size_hint_x: None
        width: dp(50)
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .5}
        MDLabel:
            text:"OK"

    AnchorLayout:
        MDLabel:
            text: "Login in progress. "
"""

# class Content(BoxLayout):
#     pass

#Builder.load_string(content)

if platform == "android":
    Logger.error("KivyAuth: Seems like you tried from kivyauth.android while being on a non-android device. Import from kivyauth.desktop")