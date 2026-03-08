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
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) The directory in which to copy the built private data
android.private_storage = True

# (str) The Android SDK to install
#android.sdk_path = 

# (str) The path to the Android NDK
#android.ndk_path = 

# (str) The path to the Android SDK
#android.sdk_dir = 

# (str) The path to the ant binary
#android.ant_path = 

# (bool) Enable Android auto backup
android.allow_backup = True

# (str) Backup rules file
#android.backup_rules = 

# (str) XML configuration file for backup
#android.backup_describe = 

# (list) Add android bootstrap modules
#android.bootstrap = sdl2

# (int) Override the app's version code
#android.version_code = 

# (str) The Gradle template to use
#android.gradle_template = 

# (bool) Use legacy build system (ant) instead of gradle
#android.use_legacy_build = False

# (str) Additional gradle repositories
#android.gradle_repositories = 

# (str) Additional pip packages to install
#additional_pip_deps = 

# (list) List of directories to exclude from the build
#exclude_dirs = 

# (list) List of patterns to exclude from the build
#exclude_patterns = 

# (bool) Allow only landscape mode
#orientation = landscape

# (list) Android services to add
#android.services = 

# (str) Color of the status bar
android.statusbar_color = #14B8A6

# (bool) Whether to show the navigation bar
android.windowLayout = displayCutout

# (str) Splash screen background color
android.background_color = #F0FDFA

# (str) Access window insets
android.windowConfig = 

# (str) Configuration file for app permissions
#android.manifest.extra_permissions = 

# (str) Extra arguments to pass to the build
#android.extra_args = 

# (str) Custom Android manifest file
#android.manifest.template = 

# (str) Custom Gradle build file
#android.gradle_build_template = 

# (str) Custom launcher template
#android.launcher.template = 

# (str) Custom activity template
#android.activity.template = 

# (str) Custom service template
#android.service.template = 

# (str) Custom receiver template
#android.receiver.template = 

# (str) Custom provider template
#android.provider.template = 

# (str) Custom application class
#android.application_class = 

# (str) Custom activity class
#android.activity_class = 

# (str) Custom service class
#android.service_class = 

# (str) Custom receiver class
#android.receiver_class = 

# (str) Custom provider class
#android.provider_class = 

# (str) Custom meta-data
#android.meta_data = 

# (str) Custom uses-feature
#android.uses_feature = 

# (str) Custom uses-permission
#android.uses_permission = 

# (str) Custom uses-configuration
#android.uses_configuration = 

# (str) Custom supports-screens
#android.supports_screens = 

# (str) Custom compatible-screens
#android.compatible_screens = 

# (str) Custom supports-gl-texture
#android.supports_gl_texture = 

# (str) Custom application label
#android.label = 

# (str) Custom application name
#android.app_name = 

# (str) Custom package path
#android.package_path = 

# (str) Custom entry point
#android.entry_point = 

# (str) Custom icon path
#android.icon_path = 

# (str) Custom presplash path
#android.presplash_path = 

# (str) Custom OUYA icon path
#android.ouya_icon_path = 

# (list) OUYA category
#android.ouya_category = 

# (bool) OUYA enable
#android.ouya_enabled = False

# (str) Archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable debug mode
#debug = false

# (bool) Release mode
release = true

# (str) Keystore path for signing
#android.keystore_path = 

# (str) Keystore alias
#android.keystore_alias = 

# (str) Keystore password
#android.keystore_password = 

# (str) Key password
#android.key_password = 

# (str) Build directory
#build_dir = 

# (str) Dist directory
#dist_dir = 

# (str) Log directory
#log_dir = 

# (str) Temp directory
#temp_dir = 

# (str) Cache directory
#cache_dir = 

# (str) Output directory
#output_dir = 

# (str) Work directory
#work_dir = 

# (str) Project directory
#project_dir = 

# (str) App directory
#app_dir = 

# (str) Data directory
#data_dir = 

# (str) Files directory
#files_dir = 

# (str) Private directory
#private_dir = 

# (str) Public directory
#public_dir = 

# (str) External directory
#external_dir = 

# (str) Internal directory
#internal_dir = 

# (str) Root directory
#root_dir = 

# (str) Base directory
#base_dir = 

# (str) Home directory
#home_dir = 

# (str) Documents directory
#documents_dir = 

# (str) Downloads directory
#downloads_dir = 

# (str) Pictures directory
#pictures_dir = 

# (str) Music directory
#music_dir = 

# (str) Movies directory
#movies_dir = 

# (str) DCIM directory
#dcim_dir = 

# (str) Notifications directory
#notifications_dir = 

# (str) Ringtones directory
#ringtones_dir = 

# (str) Alarms directory
#alarms_dir = 

# (str) Podcasts directory
#podcasts_dir = 

# (str) Audiobooks directory
#audiobooks_dir = 

# (str) Recordings directory
#recordings_dir = 

# (str) Screenshots directory
#screenshots_dir = 

# (str) Backups directory
#backups_dir = 

# (str) Logs directory
#logs_dir = 

# (str) Config directory
#config_dir = 

# (str) Temp files directory
#tmp_dir = 

# (str) Cache files directory
#cache_files_dir = 

# (str) App cache directory
#app_cache_dir = 

# (str) System cache directory
#system_cache_dir = 

# (str) Dalvik cache directory
#dalvik_cache_dir = 

# (str) Vendor directory
#vendor_dir = 

# (str) System directory
#system_dir = 

# (str) Product directory
#product_dir = 

# (str) OEM directory
#oem_dir = 

# (str) Carrier directory
#carrier_dir = 

# (str) Cust directory
#cust_dir = 

# (str) Region directory
#region_dir = 

# (str) Operator directory
#operator_dir = 

# (str) Customer directory
#customer_dir = 

# (str) Brand directory
#brand_dir = 

# (str) Model directory
#model_dir = 

# (str) Device directory
#device_dir = 

# (str) Hardware directory
#hardware_dir = 

# (str) Platform directory
#platform_dir = 

# (str) Board directory
#board_dir = 

# (str) SOC directory
#soc_dir = 

# (str) Chipset directory
#chipset_dir = 

# (str) CPU directory
#cpu_dir = 

# (str) GPU directory
#gpu_dir = 

# (str) NPU directory
#npu_dir = 

# (str) DSP directory
#dsp_dir = 

# (str) ISP directory
#isp_dir = 

# (str) VPU directory
#vpu_dir = 

# (str) APU directory
#apu_dir = 

# (str) TPU directory
#tpu_dir = 

# (str) BPU directory
#bpu_dir = 

# (str) HPU directory
#hpu_dir = 

# (str) IPU directory
#ipu_dir = 

# (str) JPU directory
#jpu_dir = 

# (str) KPU directory
#kpu_dir = 

# (str) LPU directory
#lpu_dir = 

# (str) MPU directory
#mpu_dir = 

# (str) QPU directory
#qpu_dir = 

# (str) RPU directory
#rpu_dir = 

# (str) SPU directory
#spu_dir = 

# (str) UPU directory
#upu_dir = 

# (str) VPU directory
#vpu2_dir = 

# (str) WPU directory
#wpu_dir = 

# (str) XPU directory
#xpu_dir = 

# (str) YPU directory
#ypu_dir = 

# (str) ZPU directory
#zpu_dir = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build folder storage
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
