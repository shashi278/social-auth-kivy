### Integrate Github and Twitter Login in Kivy Applications

#### Firebase has been used to integrate Github and Twitter logins

##### Prerequisites
* Declare Firebase as a gradle dependency in your `buildozer.spec` file:
 ```spec
 android.gradle_dependencies = com.google.firebase:firebase-auth:19.3.1
 ```
* For using firebase in kivy applications, we need to tweak few settings internally:
  * Build your application once, doesn't matter if it crashes
  * Then find *build.tmpl.gradle* inside *.buildozer/android/platform/build-armeabi-v7a/dists/app-name__armeabi-v7a/templates/* and change gradle plugin version from 3.1.4 to 3.5.2(I've already created a PR for the same in p4a. Hope they merge it) and add google-services plugin as it's required by firebase and apply the plugin:
  ```java
  buildscript {
    repositories {
       //...
    }
    dependencies {
        //make sure its 3.5.2 here instead of 3.1.4 
        classpath 'com.android.tools.build:gradle:3.5.2'
        
        //google-services plugin, required by firebase
        classpath 'com.google.gms:google-services:4.3.3'
    }
  }
  
  //...
  
  // At the bottom
  apply plugin: 'com.google.gms.google-services'
  ```
  * Make sure gradle version is set to latest(6.4.1) inside *gradle-wrapper.properties*(It's been updated in develop branch. If you're using master branch of p4a, you may need to update it manually). This file is located at: *.buildozer/android/platform/build-armeabi-v7a/dists/app-name__armeabi-v7a/gradle/wrapper/*
  
  * Copy your *google-services.json* inside *.buildozer/android/platform/build-armeabi-v7a/dists/app-name__armeabi-v7a/*. Its required for firebase authentication.

##### Start Integrating
  * Feel free to look at their [docs](https://firebase.google.com/docs/auth/android/start) for more.
  * Add few required java classes for firebase authentication
  ```python
  #----Firebase classes for Github and Twitter Login----#
  FirebaseAuth= autoclass('com.google.firebase.auth.FirebaseAuth')
  FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
  OAuthProvider = autoclass('com.google.firebase.auth.OAuthProvider')
  FirebaseUser = autoclass('com.google.firebase.auth.FirebaseUser')
  ```
  * We need to implement two java classes to handle success and failure while logging in.
  ```python
    class OnSuccessListener(PythonJavaClass):
      __javainterfaces__=['com/google/android/gms/tasks/OnSuccessListener']
      __javacontext__= 'app'

      @java_method('(Ljava/lang/Object;)V')
      def onSuccess(self, result):
          # User is signed in
          # You may get user information like name,email, etc. now and perform after-login stuffs.
          user = FirebaseAuth.getInstance().getCurrentUser()

          # user.getDisplayName()
          # user.getEmail()
          # user.getPhotoUrl().toString()

    class OnFailureListener(PythonJavaClass):
        __javainterfaces__=['com/google/android/gms/tasks/OnFailureListener']
        __javacontext__= 'app'

        @java_method('(Ljava/lang/Exception;)V')
        def onFailure(self, e):
            #handle exception
  ```
  
  * Next, get an instance of `FirebaseAuth` inside `build` method of your app:
  ```python
    self.mAuth= FirebaseAuth.getInstance()
  ```
  * Finally, add below codes to start login process inside a method to be called when user clicks the login button:
  ```python
    provider = OAuthProvider.newBuilder("github.com") # "twitter.com" for twitter login
    pendingResultTask = FirebaseAuth.getPendingAuthResult()
    if pendingResultTask:
        #There's something already here! Finish the sign-in for your user.
        task= pendingResultTask.addOnSuccessListener(OnSuccessListener())
        task= task.addOnFailureListener(OnFailureListener())
    else:
        #There's no pending result so you need to start the sign-in flow.

        task= FirebaseAuth.startActivityForSignInWithProvider(context, provider.build())
        task= task.addOnSuccessListener(OnSuccessListener())
        task= task.addOnFailureListener(OnFailureListener())
  ```
  
