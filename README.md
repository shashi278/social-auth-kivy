# KivyAuth
#### *Integrate Google, Facebook, Github &amp; Twitter login in kivy applications*
![build](https://travis-ci.org/shashi278/social-auth-kivy.svg?branch=master) [![Python 3.6](https://img.shields.io/pypi/pyversions/kivymd)](https://www.python.org/downloads/release/python-360/) ![pypi](https://img.shields.io/pypi/v/kivyauth) ![license](https://img.shields.io/pypi/l/kivyauth) ![format](https://img.shields.io/pypi/format/kivyauth) ![downloads](https://img.shields.io/pypi/dm/kivyauth) 

###
![demo.gif](demo/demo.gif)

##
### Installation
It can be installed via pip
```bash
pip install kivyauth
```

### How to use
The example below shows the basic usage of the library by integrating google login.

* Add [prerequisite](docs/integrate-google-facebook-login.md#prerequisite) for google login before proceeding further

* Include necessary imports, for example, in case of google login
```python
from kivyauth.initialize import initialize_google
from kivyauth.logins import login_google, logout, login_providers
```

* Initialize google login inside your app's build method
```python
def build(self):
  #..
  self.mGSignInClient= initialize_google(self.success_listener, self.error_listener, RC_SIGN_IN)
  #..
```
`success_listener` is a function to be called upon successful login with `name`, `email`, and `photo url` of the user. So, create a success listener function which accepts three parameters and perform after-login stuffs. `error_listener` doesn't accept any argument.
`RC_SIGN_IN` is just a unique request code used to differentiate among different requests. Define it an integer constant.

* Next, add below code inside a function to be called when user clicks the login button.
```python
login_google(self.mGSignInClient, RC_SIGN_IN)
self.current_provider= login_providers.google
```

* To logout
```python
logout(self.current_provider, self.after_logout)
```

* Make sure to include `kivyauth` as a requirement in the buildozer.spec file
```spec
requirements = python3,kivy,kivyauth
```

* See [demo](demo/) for refrence

A more comprehensive documentation is on it's way.

### Other
Feel free to ping me or raise issues if there's any difficulty in packaging it up.

Star this repo if you think it's useful.
