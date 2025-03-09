from __future__ import annotations

import random
import string
import sqlite3
from pathlib import Path
from typing import Union
import json


class Util:
    class Trim:
        pass

    class Increment:
        def __init__(self, value) -> None:
            self.val = value

    class Append:
        def __init__(self, value) -> None:
            self.val = value

    def trim(self) -> Trim:
        """
        Remove element from dict
        """
        return self.Trim()

    def increment(self, value: Union[int, float, None] = 1) -> Increment:
        """
        Increment element by value

        Args:
            value: The value to increment by
        """
        return self.Increment(value)

    def append(self, value: Union[dict, list, str, int, float, bool]) -> Append:
        """
        Append element to list

        Args:
            value: The value to append
        """
        return self.Append(value)


class _Base:
    def __init__(self, name: str, data_dir: str) -> None:
        self.name = name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(Path(data_dir, "arowana.db"))
        self._initialize()
        self.util = Util()

    def random_key(self, length: int = 12) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def _initialize(self) -> None:
        self._connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.name} (
                key TEXT PRIMARY KEY,
                data TEXT);
            """)
        self._connection.commit()

    def put(self, data: Union[dict, list, str, int, bool, float], key: Union[str, int, None] = None) -> dict:
        """
        Put item into base. Overrides existing item if key already exists

        Args:
            data: The data to be stored
            key: The key to store the data under. If None, a new key will be generated

        Returns:
            dict: Added item details
        """

        _key = data.pop("key", None) if isinstance(data, dict) else None
        key = str(key or _key or self.random_key())

        cursor = self._connection.cursor()
        cursor.execute(
            f"""INSERT OR REPLACE INTO {self.name} (key, data) VALUES (?, ?)""",
            (key, json.dumps(data)),
        )
        self._connection.commit()

        if isinstance(data, dict):
            data["key"] = key
            return data
        else:
            return {"key": key, "value": data}

    def insert(self, data: Union[dict, list, str, int, bool, float], key: Union[str, int, None] = None) -> dict:
        """
        Insert item to base. Does not override existing item if key already exists

        Args:
            data: The data to be stored
            key: The key to store the data under. If None, a new key will be generated

        Returns:
            dict: Added item details
        """

        _key = data.pop("key", None) if isinstance(data, dict) else None
        key = str(key or _key or self.random_key())

        try:
            cursor = self._connection.cursor()
            cursor.execute(f"""INSERT INTO {self.name} (key, data) VALUES (?, ?)""", (key, json.dumps(data)))
            self._connection.commit()
        except sqlite3.IntegrityError:
            raise Exception(f"Key '{key}' already exists")

        if isinstance(data, dict):
            data["key"] = key
            return data
        else:
            return {"key": key, "value": data}

    def get(self, key: str) -> dict:
        """
        Get item from base.

        Args:
            key: key of the item to retrieve

        Returns:
            dict: Retrieved item details
        """

        cursor = self._connection.cursor()
        cursor.execute(f"""SELECT data FROM {self.name} WHERE key = ?""", (key,))
        result = cursor.fetchone()

        if result is None:
            raise Exception(f"Key '{key}' not found")

        data = json.loads(result[0])

        if isinstance(data, dict):
            data["key"] = key
            return data
        else:
            return {"key": key, "value": data}

    def delete(self, key: str) -> None:
        """
        Delete item from base

        Args:
            key: key of the item to delete
        """

        cursor = self._connection.cursor()
        cursor.execute(f"""DELETE FROM {self.name} WHERE key = ?""", (key,))
        self._connection.commit()

    def puts(self, items: list[Union[dict, list, str, int, bool, float]]) -> dict:
        """
        Put multiple items into base

        Args:
            items: Items to add

        Returns:
            dict: Added items details
        """

        _items = []
        returns = []

        for item in items:
            key = self.random_key()

            if isinstance(item, dict):
                key = item.pop("key", None) or key
                _items.append((key, json.dumps(item)))
                item_copy = item.copy()
                item_copy["key"] = key
                returns.append(item_copy)
            else:
                _items.append((key, json.dumps(item)))
                returns.append({"key": key, "value": item})

        cursor = self._connection.cursor()
        cursor.executemany(f"""INSERT OR REPLACE INTO {self.name} (key, data) VALUES (?, ?)""", _items)
        self._connection.commit()

        return {"items": returns}

    def update(self, data: dict, key: str) -> None:
        """
        Update item in base

        Args:
            data: Attributes to update
            key: Key of the item to update
        """
        cursor = self._connection.cursor()

        for attr, value in data.items():
            if isinstance(value, Util.Trim):
                cursor.execute(
                    f"""UPDATE {self.name} SET data = json_remove(data, '$.{attr}') WHERE key = ?""",
                    (key,),
                )
            elif isinstance(value, Util.Increment):
                cursor.execute(
                    f"""
                    UPDATE {self.name}
                    SET data = json_replace(data, '$.{attr}', json_extract(data, '$.{attr}') + ?)
                    WHERE key = ?
                    """,
                    (
                        value.val,  # perhapse use json.dumps to handle certain datatypes
                        key,
                    ),
                )
            elif isinstance(value, Util.Append):
                cursor.execute(
                    f"""
                    UPDATE {self.name}
                    SET data = json_replace(data, '$.{attr}', json_insert(json_extract(data, '$.{attr}'), '$[#]', ?))
                    WHERE key = ?
                    """,
                    (
                        value.val,  # perhapse use json.dumps to handle certain datatypes
                        key,
                    ),
                )
            else:
                cursor.execute(
                    f"""
                    INSERT OR REPLACE INTO {self.name} (key, data)
                    VALUES (?,
                            CASE
                                WHEN EXISTS(SELECT 1 FROM {self.name} WHERE key = ?)
                                THEN json_replace((SELECT data FROM {self.name} WHERE key = ?), '$.{attr}', json(?))
                                ELSE json_object('{attr}', json(?))
                            END
                    )
                    """,
                    (key, key, key, json.dumps(value), json.dumps(value)),
                )

        self._connection.commit()

    """
    def fetch(self, query: Union[dict, list, None] = None, limit: int = 1000):  # order, pagination
        pass
    """

    def all(self) -> dict:
        """
        Get all items in base

        Returns:
            dict: All items
        """
        cursor = self._connection.cursor()
        cursor.execute(f"""SELECT key, data FROM {self.name}""")
        results = cursor.fetchall()

        items = []
        for key, data_str in results:
            data = json.loads(data_str)
            if isinstance(data, dict):
                data["key"] = key
                items.append(data)
            else:
                items.append({"key": key, "value": data})

        return {"items": items}

    def drop(self) -> None:
        """
        Delete base from database
        """
        cursor = self._connection.cursor()
        cursor.execute(f"""DROP TABLE IF EXISTS {self.name}""")
        self._connection.commit()
