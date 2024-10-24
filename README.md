<p align="center"> <img src="https://raw.githubusercontent.com/shashi278/social-auth-kivy/master/demo/kivyauth_logo.png" width="30%" ></img> </p>


# KivyAuth
#### *Integrate Google, Facebook, GitHub &amp; Twitter login in kivy applications*
[![build](https://travis-ci.org/shashi278/social-auth-kivy.svg?branch=master)](https://travis-ci.org/github/shashi278/social-auth-kivy/) [![Python 3.6](https://img.shields.io/pypi/pyversions/kivymd)](https://www.python.org/downloads/release/python-360/) [![pypi](https://img.shields.io/pypi/v/kivyauth)](https://pypi.org/project/KivyAuth/) [![license](https://img.shields.io/pypi/l/kivyauth)](https://github.com/shashi278/social-auth-kivy/blob/master/LICENSE) [![format](https://img.shields.io/pypi/format/kivyauth)](https://pypi.org/project/KivyAuth/#modal-close) [![downloads](https://img.shields.io/pypi/dm/kivyauth)](https://pypi.org/project/KivyAuth/) [![code size](https://img.shields.io/github/languages/code-size/shashi278/social-auth-kivy)]() [![repo size](https://img.shields.io/github/repo-size/shashi278/social-auth-kivy)]()

### KivyAuth on Android
![Demo Gif](https://raw.githubusercontent.com/shashi278/social-auth-kivy/master/demo/demo.gif)

<a href='https://play.google.com/store/apps/details?id=com.watney.glogin' ><img src='https://raw.githubusercontent.com/steverichey/google-play-badge-svg/266d2b2df26f10d3c00b8129a0bd9f6da6b19f00/img/en_get.svg' alt='Get it on Playstore' width=200/> </a>

##
### KivyAuth on Desktop
![Desktop_demo_test gif](https://raw.githubusercontent.com/shashi278/social-auth-kivy/cross-platform/demo/kivyauth_desktop_alpha.gif)


### Run [demo](demo/) app on desktop:
 * **Make Sure you've created OAuth apps and have their CLIENT_ID and CLIENT_SECRET handy before running demo application**
 * Create a .env file in the app directory with the below format:
  ```properties
  GOOGLE_CLIENT_ID=<Your-client-id-from-google-cloud-console>
  GOOGLE_CLIENT_SECRET=<Your-Client-Secret>

  FACEBOOK_CLIENT_ID=<Your-Facebook-Client-id>
  FACEBOOK_CLIENT_SECRET=<Your-Facebook-Client-secret>

  GITHUB_CLIENT_ID=<Github-Client-id>
  GITHUB_CLIENT_SECRET=<Github-Client-secret>

  ```

##
## How to use

### Instruction for using KivyAuth on Desktop:
* pip install kivyauth==2.3.3

### Note for Android:
  Make sure you go through the [prerequisites](https://github.com/shashi278/social-auth-kivy/blob/master/docs/prerequisites.md)
  for the login methods, you're going to integrate them into your application before moving further

#
The example below shows integrating Google login. Similarly, other login methods can also be used.

* Include necessary imports for Google login
```python
from kivyauth.google_auth import initialize_google, login_google, logout_google
```

* Initialize Google login inside your app's build method
```python
def build(self):
  initialize_google(self.after_login, self.error_listener)
```
`after_login` is a function to be called upon successful login with `name`, `email`, `photo url` `family name`, `given name` of the user. So, create a success listener function that accepts three parameters and performs after-login stuff (like updating UI, etc.). `error_listener` is called in case of any error and it doesn't accept any argument.

* You can also add auto-login( if the user is already logged in then directly move to after-login stuff) inside app's `on_start` method as below(mention only login providers you are using in your app):
```python
def on_start(self):

    if auto_login(login_providers.google):
        self.current_provider = login_providers.google
    elif auto_login(login_providers.facebook):
        self.current_provider = login_providers.facebook
    elif auto_login(login_providers.github):
        self.current_provider = login_providers.github
    elif auto_login(login_providers.twitter):
        self.current_provider = login_providers.twitter
```

* Next, call `login_google()` upon a button click to initiate the login process.

* Similarly, to logout, call `logout_google` as
```python
logout_google(self.after_logout)
```
`after_logout` is a function to be called after user gets logged out. For example, to update UI.

* Make sure to include `kivyauth` as a requirement in the buildozer.spec file
```spec
requirements = python3,kivy,kivyauth==2.3.3
```


##  
### TODO:
  * Support iOS

##
### Changelog
#### v2.3.3
  *  Fixed werkzeug server not shutting down


#### v2.3.2
  *  Fixed crashing when the user doesn't have a photo


#### v2.3.1 - KivyAuth cross-platform
  * Kivyauth APIs are now platform-independent
  * Desktop support for Linux, win, and possibly Mac


#### v2.3 - KivyAuth cross-platform
  * Desktop support added(in alpha)
  * All Android auths are inside `kivyauth.android` while those for desktops are inside `kivyauth.desktop`


#### v2.2
  * Added Auto-login feature
  * `login_providers` are now inside `kivyauth` rather than `kivyauth.providers`


#### v2.0
  * Individual login providers are moved into respective folders
  * Fix the problem of not being able to use individual login methods
  * Now it's relatively easier to use the library

### Other
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

**Contributing**: Contributions are more than welcome. Looking for contributions in making it cross-platform(specifically for iOS) and better documentation.


Feel free to ping me or raise an issue if you want to talk about this project or Kivy in general.
