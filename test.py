#!/usr/bin/env python

from mica import go
from params import parameters
from mica.params import parameters as server_params

# Emulate a mobile device so we can test it in development, first.

parameters["fake_mobile"] = True
parameters["keepsession"] = False
parameters["log"] : cwd + "logs/mica.log"
parameters["tlog"] : cwd + "logs/twisted.log"

parameters["couch_adapter_type"] = server_params["couch_adapter_type"]
parameters["main_server"] = server_params["main_server"]
parameters["couch_server"] = server_params["couch_server"]
parameters["couch_proto"] = server_params["couch_server"]
parameters["couch_port"] = server_params["couch_server"]
parameters["couch_path"] = server_params["couch_server"]

go(parameters)
