# coding: utf-8
from jnius import autoclass
from time import sleep
import sys
import codecs

print "Loading initial parameters"
from params import parameters, app
print "Loading mica services"

print "Loading certificate file for couch"
fh = codecs.open(parameters["cert"], 'r', "utf-8")
cert = fh.read()
fh.close()

if __name__ == '__main__':

    PythonService = autoclass("org.renpy.android.PythonService")
    CouchBase = autoclass("org.renpy.android.Couch")
    couch = CouchBase(PythonService.mService)
    port = couch.start(app["local_username"], app["local_password"], app["local_port"], app["local_database"], cert, PythonService.mService)

    if port == -1 :
        print "AAAHHHHHH. FAILURE."
    else :
        print "Trying to start replication"
        user = app["remote_user"] 
        pw = app["remote_password"] 
        url = app["remote_protocol"] + "://" + user + ":" + pw + "@" + app["remote_host"] + ":" + str(app["remote_port"])
        if couch.replicate(app["remote_database"], url, user, pw) == -1 :
            print "Replication failed. Boo. =("
        else :
            print "Replication started. Yay."

    from mica.mica import go
    parameters["couch"] = couch
    go(parameters)

    while True:
        print "Uh oh. Problem in MICA. May need to restart application."
        sleep(1)
        
