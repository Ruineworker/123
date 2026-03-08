[app]

# (str) Title of your application
title = FinWise

# (str) Package name
package.name = finwise

# (str) Package domain (needed for android/ios packaging)
package.domain = org.finwise

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==2.0.0,matplotlib,pillow,requests,android,pyjnius

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) The directory in which to place the android build
build_dir = ./buildozer/android

# (str) The directory where the APK will be stored
bin_dir = ./bin

# (bool) Enable Android auto backup
android.allow_backup = True

# (str) Backup rules for Android auto backup
android.backup_rules = 

# (str) Log level
log_level = 2

# (str) Path to a custom keystore file (optional)
# android.keystore = /path/to/keystore

# (str) Keystore alias name
# android.keystore_alias = finwise

# (str) Keystore password
# android.keystore_password = 

# (str) Entry point for the app (default is main.py)
# Puts your main.py at the root of the APK
presplash_filename = ./assets/splash.png

# (list) Icon filenames for different densities
icon.filename = ./assets/icon.png
icon.icon_name_ic_launcher = ./assets/icon.png
icon.icon_name_ic_launcher_round = ./assets/icon.png

# (bool) Create a release build
# android.release_artifact = aab

# (bool) Include debug symbols in the build
# android.debug_symbols = True

# (str) Splash screen color (hex format)
android.splash_color = #00C49A

# Customizations
android.add_aars = 
android.add_jars = 

# Gradle dependencies
android.gradle_dependencies = 

# Enable AndroidX
android.use_androidx = true

# Enable multidex support
android.enable_multidex = true
