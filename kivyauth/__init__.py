
from kivy.utils import platform
from kivy.logger import Logger

if platform!='android':
    Logger.error("KivyAuth: KivyAuth currently only supports android platform.")
    exit(1)