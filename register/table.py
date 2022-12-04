import json
import sqlite3
from typing import Optional, overload, List

from .item import Item


# Columns:
# uid TEXT PRIMARY KEY
# endpoint TEXT NOT NULL
# timestamp REAL NOT NULL
# others TEXT NOT NULL


class Cursor:
    def __init__(self, database: str):
        self._database = database

    def __enter__(self):
        self._connection = sqlite3.connect(self._database)
        self._cursor = self._connection.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
        self._connection.commit()
        self._connection.close()


class Table:
    def __init__(self, database: str, table: str):
        self._database = database
        self._table = table
        with Cursor(self._database) as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {self._table}")
            cursor.execute(f"""
                CREATE TABLE {self._table} (
                    uid TEXT PRIMARY KEY,
                    endpoint TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    others TEXT NOT NULL
                )
            """)

    def update(self, item: Item):
        others = json.dumps(item.others)
        with Cursor(self._database) as cursor:
            cursor.execute(f"""
                UPDATE {self._table}
                SET endpoint = ?, timestamp = ?, others = ?
                WHERE uid = ?
            """, [item.endpoint, item.timestamp, others, item.uid])
            if cursor.rowcount == 0:
                cursor.execute(f"""
                    INSERT INTO {self._table} (uid, endpoint, timestamp, others)
                    VALUES (?, ?, ?, ?)
                """, [item.uid, item.endpoint, item.timestamp, others])

    @overload
    def select(self) -> List[Item]:
        ...

    @overload
    def select(self, uid: str) -> Optional[Item]:
        ...

    def select(self, uid=None):
        with Cursor(self._database) as cursor:
            query = f"""
                SELECT uid, endpoint, timestamp, others
                FROM {self._table}
            """
            if uid is None:
                result = cursor.execute(query)
            else:
                query += f"WHERE uid = ?"
                result = cursor.execute(query, [uid])
            items = [Item(
                uid=_uid,
                endpoint=endpoint,
                timestamp=timestamp,
                **json.loads(others)
            ) for _uid, endpoint, timestamp, others in result]
            if uid is None:
                return items
            elif len(items) == 1:
                return items[0]
            else:
                return None

    def delete(self, uid: str):
        with Cursor(self._database) as cursor:
            cursor.execute(f"""
                DELETE FROM {self._table}
                WHERE uid = ?
            """, [uid])
