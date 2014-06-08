mica-android
============

MICA Reader: A Kivy/Python-for-Android project which runs the mobile version of MICA: A Chinese Learning system: http://github.com/hinesmr/mica

This includes a buildozer.spec file as well as two additional recipe dependencies: python-cjklib and python-webob

Some initializations:

$ ln -s ~/python-for-android/recipes/webob .buildozer/android/platform/python-for-android/recipes/webob
$ ln -s ~/python-for-android/recipes/cjklib .buildozer/android/platform/python-for-android/recipes/cjklib

# Comment out "_csv" in these two files:
$ vim .buildozer/android/platform/python-for-android/src/blacklist.txt 
$ vim .buildozer/android/platform/python-for-android/build/blacklist.txt
