from kivy.logger import Logger
from kivy.utils import platform

__version__ = "2.3.3"
_log_message = "KivyAuth:" + f" {__version__}" + f' (installed at "{__file__}")'

__all__ = ("login_providers", "auto_login")

Logger.info(_log_message)
