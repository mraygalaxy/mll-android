[app]

# (str) Title of your application
title = MICA Learning 

# (str) Package name
package.name = mica

# (str) Package domain (needed for android/ios packaging)
package.domain = com.hinespot

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,crt,js,css,html,gif,ico,svg,eot,woff,woff2,ttf,csv,sql,mo,p,wav

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = mica/params.py

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, mica/util, mica/data, mica/.git, mica/logs, mica/Data, mica/.git, mica/build, mica/ictc_32bit, mica/ictc_64bit, .git

# (list) List of exclusions using pattern matching
source.exclude_patterns = mica/params.py

# (str) Application versioning (method 1)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (str) Application versioning (method 2)
# version = 1.2.0

# (list) Application requirements
requirements = openssl,pyopenssl,sqlite3,twisted,kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
presplash.filename = %(source.dir)s/splash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = all

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 19

# (int) Minimum API required (8 = Android 2.2 devices)
android.minapi = 19 

# (int) Android SDK version to use
#android.sdk = 21

# (str) Android NDK version to use
#android.ndk = 9c

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
android.p4a_dir = %(source.dir)s/../../../../python-for-android 

# (list) python-for-android whitelist
#android.p4a_whitelist =

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar

#android.add_jars = %(source.dir)s/jars/couchbase-lite-java-core-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-android-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-javascript-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-listener-1.0.2.jar,%(source.dir)s/jars/rhino-1.7R3.jar,%(source.dir)s/jars/commons-io-2.0.1.jar,%(source.dir)s/jars/jackson-core-asl-1.9.2.jar,%(source.dir)s/jars/jackson-mapper-asl-1.9.2.jar,%(source.dir)s/jars/servlet-2-3.jar,%(source.dir)s/jars/webserver-2-3.jar
#android.add_jars = %(source.dir)s/jars/couchbase-lite-java-core-custom.jar,%(source.dir)s/jars/couchbase-lite-android-custom.jar,%(source.dir)s/jars/couchbase-lite-java-javascript-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-listener-1.0.2.jar,%(source.dir)s/jars/rhino-1.7R3.jar,%(source.dir)s/jars/commons-io-2.0.1.jar,%(source.dir)s/jars/jackson-core-asl-1.9.2.jar,%(source.dir)s/jars/jackson-mapper-asl-1.9.2.jar,%(source.dir)s/jars/servlet-2-3.jar,%(source.dir)s/jars/webserver-2-3.jar
#android.add_jars = %(source.dir)s/jars/couchbase-lite-java-core-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-android-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-javascript-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-listener-1.0.2.jar,%(source.dir)s/jars/rhino-1.7R3.jar,%(source.dir)s/jars/commons-io-2.0.1.jar,%(source.dir)s/jars/jackson-core-asl-1.9.2.jar,%(source.dir)s/jars/jackson-mapper-asl-1.9.2.jar,%(source.dir)s/jars/servlet-2-3.jar,%(source.dir)s/jars/webserver-2-3.jar
#android.add_jars = %(source.dir)s/jars/couchbase-lite-java-core-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-android-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-javascript-1.0.2.jar,%(source.dir)s/jars/couchbase-lite-java-listener-1.0.0-72-CORS.jar,%(source.dir)s/jars/rhino-1.7R3.jar,%(source.dir)s/jars/commons-io-2.0.1.jar,%(source.dir)s/jars/jackson-core-asl-1.9.2.jar,%(source.dir)s/jars/jackson-mapper-asl-1.9.2.jar,%(source.dir)s/jars/servlet-2-3.jar,%(source.dir)s/jars/webserver-2-3.jar
android.add_jars = %(source.dir)s/jars/couchbase-lite-java-core-1.3.0.jar,%(source.dir)s/jars/couchbase-lite-java-javascript-1.3.0.jar,%(source.dir)s/jars/couchbase-lite-java-listener-1.3.0.jar,%(source.dir)s/jars/rhino-1.7R3.jar,%(source.dir)s/jars/commons-io-2.0.1.jar,%(source.dir)s/jars/jackson-core-2.5.0.jar,%(source.dir)s/jars/jackson-annotations-2.5.0.jar,%(source.dir)s/jars/jackson-databind-2.5.0.jar,%(source.dir)s/jars/servlet-2-3.jar,%(source.dir)s/jars/webserver-2-3.jar,%(source.dir)s/jars/stateless4j-2.4.0.jar,%(source.dir)s/jars/okio-1.8.0.jar,%(source.dir)s/jars/okhttp-3.3.1.jar,%(source.dir)s/jars/couchbase-lite-android-1.3.0.jar,%(source.dir)s/jars/couchbase-lite-android-forestdb-1.3.0.jar,%(source.dir)s/jars/couchbase-lite-android-sqlcipher-1.3.0.jar,%(source.dir)s/jars/couchbase-lite-android-sqlite-custom-1.3.0.jar


# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src = %(source.dir)s/Couch.java,%(source.dir)s/MLog.java,%(source.dir)s/Internet.java,%(source.dir)s/MyWebView.java

# (str) python-for-android branch to use, if not master, useful to try
# not yet merged features.
#android.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
android.manifest.intent_filters = intent_filters.xml

# (list) Android additionnal libraries to copy into libs/armeabi
android.add_libs_armeabi = %(source.dir)s/jars/libcbljavakey.so,%(source.dir)s/jars/libcbljavasqlcipher.so,%(source.dir)s/jars/libcbljavasqlitecustom.so,%(source.dir)s/jars/libsqlite3.so,%(source.dir)s/jars/libsqlcipher.so,%(source.dir)s/jars/libCouchbaseLiteJavaForestDB.so,%(source.dir)s/jars/libcom_couchbase_touchdb_TDCollateJSON.so,%(source.dir)s/jars/libcom_couchbase_touchdb_RevCollator.so
#android.add_libs_armeabi = %(source.dir)s/jars/libcom_couchbase_touchdb_TDCollateJSON.so,%(source.dir)s/jars/libcom_couchbase_touchdb_RevCollator.so


#android.add_libs_armeabi_v7a = %(source.dir)s/jars/armeabi-v7a/libcom_couchbase_touchdb_TDCollateJSON.so,%(source.dir)s/jars/armeabi-v7a/libcom_couchbase_touchdb_RevCollator.so
#android.add_libs_x86 = %(source.dir)s/jars/x86/libcom_couchbase_touchdb_TDCollateJSON.so,%(source.dir)s/jars/x86/libcom_couchbase_touchdb_RevCollator.so
#android.add_libs_mips = %(source.dir)s/jars/mips/libcom_couchbase_touchdb_TDCollateJSON.so,%(source.dir)s/jars/mips/libcom_couchbase_touchdb_RevCollator.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data = android:largeHeap="true",com.sec.android.support.multiwindow="true",com.sec.android.multiwindow.DEFAULT_SIZE_W=632.0dip,com.sec.android.multiwindow.DEFAULT_SIZE_H=598.0dip,com.sec.android.multiwindow.MINIMUM_SIZE_W=632.0dip,com.sec.android.multiwindow.MINIMUM_SIZE_H=598.0dip


# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

#
# iOS specific
#

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2


# -----------------------------------------------------------------------------
# List as sections
#
# You can define all the "list" as [section:key].
# Each line will be considered as a option to the list.
# Let's take [app] / source.exclude_patterns.
# Instead of doing:
#
#     [app]
#     source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
# This can be translated into:
#
#     [app:source.exclude_patterns]
#     license
#     data/audio/*.wav
#     data/images/original/*
#


# -----------------------------------------------------------------------------
# Profiles
#
# You can extend section / key with a profile
# For example, you want to deploy a demo version of your application without
# HD content. You could first change the title to add "(demo)" in the name
# and extend the excluded directories to remove the HD content.
#
#     [app@demo]
#     title = My Application (demo)
#
#     [app:source.exclude_patterns@demo]
#     images/hd/*
#
# Then, invoke the command line with the "demo" profile:
#
#     buildozer --profile demo android debug
