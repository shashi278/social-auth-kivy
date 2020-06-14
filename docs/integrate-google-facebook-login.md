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
 
##

### Facebook Login:

#### Prerequisite
* We'll be creating our own version of facebook login i.e. using python and kivy by following each step from their [doc](https://developers.facebook.com/docs/facebook-login/android/). So, open it in a new tab and follow it along-side.

#### Start Integrating
* Follow their instructions in step 1 and create an OAuth App. You may skip step 2.

* For step 3, add Facebook-login SDK as a gradle dependency in your `buildozer.spec` file:
 ```spec
 android.gradle_dependencies = com.facebook.android:facebook-login:7.0.0
 ```

* For 4th step,
  * Add `INTERNET` permission in `buildozer.spec` file
    ```spec
    android.permissions = INTERNET
    ```
  * Find `android.meta_data` in buildozer.spec file and make it to look like
    ```spec
    android.meta_data = com.facebook.sdk.ApplicationId=fb<App-ID-of-your-OAuth-App>
    ```
  * Next, find `android.add_activities` in buildozer.spec file and add some activity classes
    ```spec
    android.add_activites = com.facebook.FacebookActivity, com.facebook.CustomTabActivity
    ```
  * Lastly, create an xml file in the same directory as `main.py`. Name it whatever you like and add this into that xml file
    ```xml
    <intent-filter>
             <action android:name="android.intent.action.VIEW" />
             <category android:name="android.intent.category.DEFAULT" />
             <category android:name="android.intent.category.BROWSABLE" />
         </intent-filter>
    ```
    Now add this xml as an intent filter in the spec file
    ```spec
    android.manifest.intent_filters = <file-name>.xml
    ```

* Do as instructed in step 5 and 6

* Skip steps 7 and 8

* For next steps, we'll be implementing few java interfaces in python.
  
  * Include few required java classes:
    ```python
    #----Java Classes For Facebook Login----#
    AccessToken= autoclass('com.facebook.AccessToken')
    CallbackManagerFactory= autoclass('com.facebook.CallbackManager$Factory')
    FacebookCallback= autoclass('com.facebook.FacebookCallback')
    FacebookException= autoclass('com.facebook.FacebookException')
    FacebookSdk= autoclass('com.facebook.FacebookSdk')
    LoginManager= autoclass('com.facebook.login.LoginManager')
    GraphRequest= autoclass('com.facebook.GraphRequest')
    ImageRequest= autoclass('com.facebook.internal.ImageRequest')

    ```
  * Now, to respond to a login result, you need to register a callback with `LoginManager`. Before that, 
    we need to implement `GraphJSONObjectCallback` class which will be used when login request succeeds and within which
    we can get user information(like, name, email, etc.)
    ```python
    class PythonGraphJSONObjectCallback(PythonJavaClass):
        __javainterfaces__= ['com/facebook/GraphRequest$GraphJSONObjectCallback']
        __javacontext__= 'app'

        @java_method('(Lorg/json/JSONObject;Lcom/facebook/GraphResponse;)V')
        def onCompleted(self, me, response):
            if response.getError():
                #handle error
                
            else:
            
                if AccessToken.isCurrentAccessTokenActive():
                    access_token= AccessToken.getCurrentAccessToken().getToken()
                else:
                    access_token= ""

                uri= ImageRequest.getProfilePictureUri(
                    me.optString("id"),  #user id
                    100,                 #image height
                    100,                 #image width
                    access_token         #access token
                )
                
                # user has been logged in. Get other info
                # and do after login stuffs(like, updating UI, etc.)
    ```
  
  * Next, we need to implement `FacebookCallback` class which will be registered with `LoginManager`.
    ```python
    class PythonFacebookCallback(PythonJavaClass):
        __javainterfaces__= ['com/facebook/FacebookCallback']
        __javacontext__= 'app'

        @java_method('(Ljava/lang/Object;)V')
        def onSuccess(self, result):

            request= GraphRequest.newMeRequest(
                result.getAccessToken(),
                PythonGraphJSONObjectCallback()
            )

            params= Bundle()
            params.putString("fields", "last_name,first_name,email")
            request.setParameters(params)
            request.executeAsync()


        @java_method('()V')
        def onCancel(self):
            #Login has been cancelled
            

        @java_method('(Lcom/facebook/FacebookException;)V')
        def onError(self, error):
            #Error in logging in
            
    ```
  
  * We then need o initialize Facebook SDK inside App's `build` method:
    ```python
    FacebookSdk.sdkInitialize(context.getApplicationContext())
    ```
  * And then register the callback with `LoginManager` inside `build` method:
    ```python
    mCallbackManager = CallbackManagerFactory.create()
    mFacebookCallback = PythonFacebookCallback()
    self.mLoginMgr = LoginManager.getInstance()
    self.mLoginMgr.registerCallback(mCallbackManager, mFacebookCallback)
    ```
  * Finally, in your `onActivityResult` method, call `callbackManager.onActivityResult` to pass the login results to the `LoginManager` via `callbackManager`. For this we just need to add one more line to our `build` method:
    ```python
    result_bind(on_activity_result=mCallbackManager.onActivityResult)
    ```
    Make sure you've `result_bind` imported:
    ```python
    from android.activity import bind as result_bind
    ```
  
  * Finally, perform the actual login with required scopes upon clicking a button. Add below codes inside a function to be called upon a button's pressing/releasing event. 
  ```python
  self.mLoginMgr.logInWithReadPermissions(
                cast(autoclass('android.app.Activity'),
                context), Arrays.asList("email", "public_profile")
                )
  ```
    
