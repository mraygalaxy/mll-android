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

print "Loading mica services"

if __name__ == '__main__':
    couch = CouchBase(String(app["local_username"]), String(app["local_password"]), app["local_port"], String(cert), PythonService.mService)

    from mica.mica import go
    parameters["couch"] = couch
    go(parameters)

    while True:
        print "Uh oh. Problem in MICA. May need to restart application."
        sleep(1)
        
