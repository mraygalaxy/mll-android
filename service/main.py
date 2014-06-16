# coding: utf-8
from jnius import autoclass
from time import sleep
import sys
import codecs

print "Loading initial parameters"
from params import parameters, app

print "Loading certificate file for couch"
fh = codecs.open(parameters["cert"], 'r', "utf-8")
cert = fh.read()
fh.close()

String = autoclass('java.lang.String')
PythonService = autoclass("org.renpy.android.PythonService")
CouchBase = autoclass("org.renpy.android.Couch")
MobileInternet = autoclass("org.renpy.android.Internet")


print "Loading mica services"

if __name__ == '__main__':
    mobile_internet = MobileInternet(PythonService.mService)

    couch = CouchBase(String(app["local_username"]), String(app["local_password"]), app["local_port"], String(cert), PythonService.mService)

    port = couch.start(String(app["local_database"]))
    
    if port == -1 :
        print "AAAHHHHHH. FAILURE."
    else :
        print "Trying to start replication"
        user = app["remote_user"] 
        pw = app["remote_password"] 
        url = app["remote_protocol"] + "://" + user + ":" + pw + "@" + app["remote_host"] + ":" + str(app["remote_port"])
        if couch.replicate(String(app["remote_database"]), String(url), String(user), String(pw)) == -1 :
            print "Replication failed. Boo. =("
        else :
            print "Replication started. Yay."

    from mica.mica import go
    parameters["couch"] = couch
    parameters["mobileinternet"] = mobile_internet
    go(parameters)

    while True:
        print "Uh oh. Problem in MICA. May need to restart application."
        sleep(1)
        
