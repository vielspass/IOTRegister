import json
import time
from typing import Any, Dict

import cherrypy

from .cors import set_cors
from .item import Item
from .table import Table

_generic_error = cherrypy.HTTPError(
    400, "Error! Read the documentation: https://github.com/vielspass/IOTServiceRegister/")
_missing_service = cherrypy.HTTPError(404, "This item is not available.")


class Server:
    exposed = True

    def __init__(self, offline_timeout: float, database: str, table: str, **kwargs):
        self._offline_timeout = offline_timeout
        self._table = Table(database, table)

    def parse_item(self, item: Item) -> Dict[str, Any]:
        dct = item.to_dict()
        dct["online"] = time.time() - dct["timestamp"] < self._offline_timeout
        del dct["timestamp"]
        return dct

    def POST(self, *path: str, **params: Any):
        set_cors()
        if len(path) == 1 and path[0] == "register":
            try:
                self._table.update(Item(timestamp=time.time(), **params))
                return

            except (KeyError, ValueError):
                pass

        raise _generic_error

    def GET(self, *path: str, **params: Any):
        set_cors()
        if len(path) == 1:
            if path[0] == "item":
                try:
                    result = self._table.select(params["uid"])
                    if result is None:
                        raise _missing_service

                    return json.dumps(self.parse_item(result))

                except (KeyError, ValueError):
                    pass

            elif path[0] == "catalog":
                return json.dumps([self.parse_item(item)
                                   for item in self._table.select()])

        raise _generic_error

    def DELETE(self, *path: str, **params: Any):
        set_cors()
        if len(path) == 1 and path[0] == "unregister":
            try:
                self._table.delete(params["uid"])
                return

            except (TypeError, ValueError):
                pass

        raise _generic_error

    def OPTIONS(self, *path: str, **params: Any):
        set_cors("OPTIONS")
