from kivy import platform
from kivy.logger import Logger
if platform != "android":
    Logger.error("KivyAuth: Seems like you've imported from the wrong directory. Import from kivyauth.android")