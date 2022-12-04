import cherrypy


def set_cors(method: str = None):
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = \
        "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range"
    if method == "OPTIONS":
        cherrypy.response.headers["Content-Type"] = "text/plain; charset=utf-8"
        cherrypy.response.headers["Content-Length"] = 0
        cherrypy.response.status = 204
    else:
        cherrypy.response.headers["Access-Control-Expose-Headers"] = "Content-Length,Content-Range"
