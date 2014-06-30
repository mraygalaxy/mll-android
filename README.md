mica-android
============

MICA Reader: A Kivy/Python-for-Android project which runs the mobile version of MICA: A Chinese Learning system: http://github.com/hinesmr/mica

The mobile reader version is a completely offline, synchronizable, fully-functional version of MICA.

It works by replicating your reading with the server using the couchdb REST API and runs exactly the same
python-version of MICA on the phone.

This includes a buildozer.spec file as well as two additional recipe dependencies: python-cjklib and python-webob

INSTALL:
==========

First, you need my fork of python-for-android for two missing python projects to be included in the APK:

$ git clone http://github.com/hinesmr/python-for-android /path/to/mica-android/../python-for-android
 
   - PLEASE CLONE THIS at the same folder-level as mica-android itself. The APK configuration file build system (buildozer)
     will assume you have cloned this. Otherwise, you will end up building an API with missing pieces. So, you should end up with
     two cloned projects. This one and <a href='http://github.com/hinesmr/python-for-android'>my fork of python-for-android</a>
     both sitting side-by-side on disk.

$ git clone http://github.com/hinesmr/mica /path/to/mica-android/service/mica
 
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
first install MICA itself on the server side, upload and translate your stories and then use the APK.
Once they stories are translated on the server side and replicated to the phone (which you can track with adb logcat | grep System.out),
you will be able to use the mobile and server versions seamlessly and interchangeably.

BUGS:
===========

1. Replication is very silent right now. There is a lot of work to do on the mobile version to better notify the user when a missing data has not yet been replicated (in both directions), but that support will come soon. The only way to verify that replication is complete (before you start reading offline) is to open the REST API in your browser on both the server and the phone's IP addresses (located at http://admin:secret_password@ip_address:5984) and verify that the number of documents on the phone is equal to the number of documents on the server side. "Rest" assured (no pun intended) that this problem is on the top of the priority list to be solved.

2. There is no syntax checking on the service/params.py file yet.

3. Probably other bugs, but I've been using the reader continuously for several weeks without any serious bugs, so I think I've worked out most of the complex issues so far.

Happy studying. =)
