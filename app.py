import json
import os
from typing import Dict, Any

import cherrypy

from register import Server

# Load config
with open("config.json") as file:
    config: Dict[str, Any] = json.load(file)
    for key, val in config.items():
        os_key = key.upper()
        if os_key in os.environ:
            config[key] = type(config[key])(os.environ[os_key])

# Mount service
cherrypy.tree.mount(Server(**config), "/", {
    "/": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher()
    }
})

if "DEBUG_MODE" in os.environ and os.environ["DEBUG_MODE"] == "1":
    # Run in debug mode
    cherrypy.engine.start()
    cherrypy.engine.block()

else:
    # Initialize cherrypy for gunicorn
    cherrypy.server.unsubscribe()
    cherrypy.config.update({'engine.autoreload.on': False})
    cherrypy.engine.signals.subscribe()
    cherrypy.config.update({'environment': 'embedded'})

    # Expose app variable for gunicorn
    app = cherrypy.tree
