mll-android
============

Read Alien: A Kivy/Python-for-Android project which runs the mobile version of MLL: Meta-Language Learning Systems: http://github.com/hinesmr/mica

The mobile reader version is a completely offline, synchronizable, fully-functional version.

It works by replicating your reading with the server using the couchdb REST API and runs exactly the same
python-version on the phone.

This includes a buildozer.spec file as well as two additional recipe dependencies: python-cjklib and python-webob

INSTALL:
==========

First, you need my fork of python-for-android for two missing python projects to be included in the APK:

$ git clone http://github.com/hinesmr/python-for-android /path/to/mica-android/../python-for-android
 
   - PLEASE CLONE THIS at the same folder-level as mica-android itself. The APK configuration file build system (buildozer)
     will assume you have cloned this. Otherwise, you will end up building an API with missing pieces. So, you should end up with
     two cloned projects. This one and <a href='http://github.com/hinesmr/python-for-android'>my fork of python-for-android</a>
     both sitting side-by-side on disk.

$ git clone http://github.com/hinesmr/mica /path/to/mll-android/service/mica
 
   - This clones a complete copy of MICA itself (which is this same core code used to power the mobile version) into a sub-directory
     of the mobile reader. Make sure it goes into the sub-directory "service/"

$ cp mica-android/service/params.py.tmpl mica-android/service/params.py # create a config file from the template version

$ edit the new params.py file and modify ONLY the "app = {" section.
  - Please leave the "parameters" variables untouched.
   

$ buildozer android debug # this will build the APK and put into the folder mica-android/bin directory.

$ adb push # or buildozer android deploy this file to your device

USAGE:
===========

The mobile reader does not allow you to import stories from scratch. It uses the couchdb REST
protocol to work offline by replicating the server database onto the phone in its entirety. So you must
first install MLL itself on the server side, upload and translate your stories and then use the APK.
Once they stories are translated on the server side and replicated to the phone
you will be able to use the mobile and server versions seamlessly and interchangeably.
