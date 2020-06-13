## Integrate Google and Facebook Login in Kivy Applications

##
### Google Login:

#### Prerequisite
 * Declare Google Play services as a gradle dependency in your `buildozer.spec` file:
 ```spec
 android.gradle_dependencies = com.google.android.gms:play-services-auth:18.0.0
 ```

#### Start Integrating
 * Feel free to look at their [doc](https://developers.google.com/identity/sign-in/android/sign-in) for more info
 * Add java classes required for google authentication in your `.py` file:
 ```python
 #----Java Classes For Google Login----#
 Gso= autoclass('com.google.android.gms.auth.api.signin.GoogleSignInOptions')
 GsoBuilder= autoclass('com.google.android.gms.auth.api.signin.GoogleSignInOptions$Builder')
 GSignIn= autoclass('com.google.android.gms.auth.api.signin.GoogleSignIn')
 ApiException= autoclass('com.google.android.gms.common.api.ApiException')
 ```
 * Create instance of `GoogleSignInClient` inside `build` method of your kivy App:
 ```python
 gso= GsoBuilder(Gso.DEFAULT_SIGN_IN).requestEmail().build()
 self.mGSignInClient= GSignIn.getClient(context, gso)
 ```
   Make sure you've,
 ```python
 PythonActivity= autoclass('org.kivy.android.PythonActivity')
 context= PythonActivity.mActivity
 ```
 * After the user signs in, you can get a `GoogleSignInAccount` object for the user in the activity's `onActivityResult` method.
   For this, we need to bind our function we want to be called when `onActivityResult` gets called during authentication. We can
   bind our function using bind function from android.activity as:
   ```python
   from android.activity import bind as result_bind
   
   # inside build method
   result_bind(on_activity_result=activity_listener_google)
   ```
 * Create your activity listener function:
 ```python
 def activity_listener_google(request_code, result_code, data):
    if request_code == RC_SIGN_IN:
        task= GSignIn.getSignedInAccountFromIntent(data)
        try:
            account= task.getResult(ApiException)
            if account:
                #user is logged in
                #Do stuffs you want after a user gets authenticated
                #eg. update UI, change screen, etc.
            
            else:
                #unable to get account

        except Exception as e:
            #Error in signing in
            
 ```
 `RC_SIGN_IN` is just a unique request code used to differentiate among different requests passed to `onActivityResult`. Define it an
 integer constant.
 
 * Finally, start sign in process when user clicks a button. Create a function in your `App` class to be called upon clicking login
  button and include below codes:
 ```python
 signInIntent= self.mGSignInClient.getSignInIntent()
 context.startActivityForResult(signInIntent, RC_SIGN_IN)
 
 ```
 

### Facebook Login:
#### coming soon
