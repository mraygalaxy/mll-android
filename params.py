# coding: utf-8
import os
import sys
import re

cwd = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)

parameters = {
           "port" : 10000,
           "sslport" : -1,
           "host" : "0.0.0.0",
           "keepsession" : True,
           "debug_host" : False,
           "log" : False,
           "tlog" : False,
           "cert" : cwd + "mica/mica.crt",
           "privkey" : False,
           "slaves" : False,
           "slave_port" : False,
           "cedict" : cwd + "mica/cedict.db",
           "cjklib" : cwd + "mica/cjklib.db",
           "tonefile" : cwd + "mica/chinese.txt",
           "duplicate_logger" : False,
           "couch_adapter_type" : "AndroidMicaServerCouchbaseMobile",
           "transreset" : False,
           "transcheck" : False,
           "mobileinternet" : False,

           "couch_server" : "mica.hinespot.com",
           "couch_proto" : "https",
           "couch_port" : "6984",

            # Only used during development by uncommenting
            # a hard-coded HTTP listener for debugging purposes.
            # couchdb listener is not enabled in the app store
           "local_database" : "mica",
           "local_username" : "admin",
           "local_password" : "devtest",
           "local_port" : 5984,
}
