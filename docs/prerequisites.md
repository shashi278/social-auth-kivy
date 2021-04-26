### For Google Login
#
* Goto https://console.cloud.google.com/
* While on cloud console, head to `APIs & Services` > `Credentials` > Click on `+ Create Credentials` and select `OAuth client ID`
* On the following screen select `Android` under `Application Type` field and follow on-screen instructions to fill all the fields and create a client ID for Android.
* Declare Google Play services as a gradle dependency in your `buildozer.spec` file:

```spec
android.gradle_dependencies = com.google.android.gms:play-services-auth:18.0.0
```

* Add `INTERNET` permission in `buildozer.spec` file
    ```spec
    android.permissions = INTERNET
    ```

#
### For Facebook Login
##
* You need to follow their [doc](https://developers.facebook.com/docs/facebook-login/android/) along-side. So open it up in a new tab.

* Follow their instruction in step 1 and create an OAuth App. You may skip step 2.

* For step 3, add Facebook-login SDK as a gradle dependency in your `buildozer.spec` file:
 ```spec
 android.gradle_dependencies = com.facebook.android:facebook-login:7.0.0
 ```
 
* For 4th step,
  * Add `INTERNET` permission in `buildozer.spec` file
    ```spec
    android.permissions = INTERNET
    ```
  * Copy your OAuth App ID and find `android.meta_data` in buildozer.spec file and make it to look like
    ```spec
    android.meta_data = com.facebook.sdk.ApplicationId=fb<App-ID-of-your-OAuth-App>
    ```
  * Next, find `android.add_activities` in buildozer.spec file and add some activity classes
    ```spec
    android.add_activites = com.facebook.FacebookActivity, com.facebook.CustomTabActivity
    ```
  * Lastly, create an xml file in the same directory as `main.py`. Name it whatever you like and paste below text into that xml file
    ```xml
    <intent-filter>
             <action android:name="android.intent.action.VIEW" />
             <category android:name="android.intent.category.DEFAULT" />
             <category android:name="android.intent.category.BROWSABLE" />
             <data android:scheme="fb<App-ID-of-your-OAuth-App>" />
    </intent-filter>
    ```
    Now add this xml as an intent filter in the spec file
    ```spec
    android.manifest.intent_filters = <file-name>.xml
    ```
#
### For Firebase Login
##
* Make sure you've created OAuth apps for [Github](https://github.com/settings/applications/new) and/or [Twitter](https://developer.twitter.com/en/apps/create) logins before proceeding further.

* Go to [firebase console](https://console.firebase.google.com) and create a project for your application.

* Once you've created a project, add your android app into the project from the Project Overview screen and follow the on-screen instructions and finally download
the `google-services.json` file.

* Declare Firebase as a gradle dependency in your `buildozer.spec` file:
 ```spec
 android.gradle_dependencies = com.google.firebase:firebase-auth:19.3.1
 ```
 
 * Add `INTERNET` permission in `buildozer.spec` file
    ```spec
    android.permissions = INTERNET
    ```

* Next, from your project's console head to the Authentication section and then switch to the Sign-in method tab and enable the sign-in methods you want for your
app.(For kivyauth you only need to enable Github and Twitter and follow on-screen instructions)

* Now you need to tweak few settings internally:
  * Build your application once, doesn't matter if it crashes
  * Then find ***build.tmpl.gradle*** inside *.buildozer/android/platform/python-for-android/pythonforandroid/bootstraps/common/build/templates* and change gradle plugin version
  from 3.1.4 to 3.5.2 and add google-services plugin as it's required by firebase and apply the plugin:
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
  
  * Paste your ***google-services.json*** inside *.buildozer/android/platform/python-for-android/pythonforandroid/bootstraps/common/build/*.
* Re-build your application
  
