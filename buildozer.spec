[app]

# (str) Title of your application
title = MoDee

# (str) Package name
package.name = modee

# (str) Package domain (should be unique)
package.domain = org.surajchaurasia

# (str) Source code directory (where your main.py is)
source.dir = .

# (str) Main entry point file
source.main = main.py

# (list) Permissions your app needs
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Features (optional)
# android.features = android.hardware.camera, android.hardware.location

# (str) Icon of your app (optional)
icon.filename = %(source.dir)s/assets/icon.png

# (bool) Indicate if your application should be fullscreen or not
fullscreen = 1

# (str) Supported orientation (portrait, landscape, sensor)
orientation = portrait

# (str) Application versioning
version = 1
version.name = 1.0.0

# (list) List of requirements to include in the package
# Always include python3 and kivy. Add others like requests, numpy, etc. if used.
requirements = python3, kivy

# (str) Custom source folders for Python modules
# (Separate multiple paths with commas)
# source.include_exts = py,png,jpg,kv,atlas

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/assets/presplash.png

# (list) Permissions for Android
# android.permissions = INTERNET, CAMERA

# (bool) If True, logcat logs show up in real-time when connected to Android device
log_level = 2

# (bool) Android entry point for fullscreen
android.entrypoint = org.kivy.android.PythonActivity

# (bool) Hide title bar
android.hide_titlebar = 1

# (str) Package format: apk or aab (Google Play requires .aab)
android.package_format = apk

# (str) Orientation
android.orientation = portrait

# (bool) Use legacy toolchain or not
# android.use_legacy_toolchain = 0

# (bool) Indicate if application should use OpenGL ES2
# android.opengl_es2 = 1

# (str) Android API levels
android.api = 33
android.minapi = 21

# (str) Android SDK/NDK versions
android.ndk = 25b
android.sdk = 33
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = ~/.buildozer/android/platform/android-sdk

# (str) Android entry point
# android.entrypoint = org.kivy.android.PythonActivity

# (list) Gradle dependencies (optional)
# android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# (list) Java classes to include (optional)
# android.add_jars = libs/some_lib.jar

# (str) Entry point for the Kivy app (default: main.py)
# source.main = main.py

# (bool) Copy all the files from your project directory inside APK
copy_libs = 1

# (list) Exclude some files or folders
exclude_patterns = tests, bin, .git, __pycache__

# (bool) Include SQLite3
sqlite3 = 1

# (str) Requirements for buildozer
# requirements = python3, kivy, requests, pillow

# (bool) Enable debug mode
# android.debug = 1

# (bool) Add Android logcat filter
# logcat_filters = python

[buildozer]
# (str) Log level (0 = quiet, 1 = normal, 2 = verbose)
log_level = 2

# (bool) Warn when running as root
warn_on_root = 1

# (str) Path to Android SDK/NDK
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r25b

# (bool) Use optimized python
# python.optimize = true

# (str) Command line arguments for Gradle
# android.gradle_args = --no-daemon

# (bool) Skip updating dependencies
# skip_update = False

# (str) Folder where build outputs go
build_dir = bin

# (bool) Copy binary output to bin/
copy_to_bin = 1

# (str) Packaging format
package_format = apk

# (bool) Enable build cache for faster builds
use_cache = True
