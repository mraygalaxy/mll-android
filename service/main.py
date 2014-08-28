# coding: utf-8
from jnius import autoclass
from time import sleep
import sys
import codecs

MLog = autoclass("org.renpy.android.MLog")
PythonService = autoclass("org.renpy.android.PythonService")
log = MLog(PythonService.mService)
String = autoclass('java.lang.String')

log.debug(String("Loading initial parameters"))

from params import parameters, app

log.debug(String("Loading certificate file for couch"))

fh = codecs.open(parameters["cert"], 'r', "utf-8")
cert = fh.read()
fh.close()

CouchBase = autoclass("org.renpy.android.Couch")
MobileInternet = autoclass("org.renpy.android.Internet")

log.debug(String("Loading mica services"))

if __name__ == '__main__':
    mobile_internet = MobileInternet(PythonService.mService)

    couch = CouchBase(String(app["local_username"]), String(app["local_password"]), app["local_port"], String(cert), PythonService.mService)

    port = couch.start(String(app["local_database"]))
    
    if port == -1 :
        log.error(String("AAAHHHHHH. FAILURE."))
    else :
        log.debug(String("Trying to start replication"))
        user = app["remote_user"] 
        pw = app["remote_password"] 
        url = app["remote_protocol"] + "://" + user + ":" + pw + "@" + app["remote_host"] + ":" + str(app["remote_port"])
        if couch.replicate(String(app["remote_database"]), String(url), False) == -1 :
            log.error(String("Replication failed. Boo. =("))
        else :
            log.debug(String("Replication started. Yay."))

    from mica.mica import go
    parameters["couch"] = couch
    parameters["mobileinternet"] = mobile_internet
    parameters["duplicate_logger"] = log
    go(parameters)

    while True:
        log.error(String("Uh oh. Problem in MICA. May need to restart application."))
        sleep(1)
        
