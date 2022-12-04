from typing import Dict, Any


class Item:
    def __init__(self,
                 uid: str,
                 endpoint: str,
                 timestamp: float,
                 **kwargs):
        self.uid = uid
        self.endpoint = endpoint
        self.timestamp = timestamp
        self.others = kwargs

    def to_dict(self):
        return dict(self.others,
                    uid=self.uid,
                    endpoint=self.endpoint,
                    timestamp=self.timestamp)
