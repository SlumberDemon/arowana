from __future__ import annotations

import os

from .base import _Base
from .drive import _Drive


class Arowana:
    def __init__(self, data_dir: str | None = None) -> None:
        """
        Initialize an Arowana instance. It's recommend to use the standalone Base and Drive.
        However this class is kept for convince sake (but limited).

        Args:
            data_dir (str): The directory where data is stored.
                Defaults to the environment variable FISHWEB_DATA_DIR when running in fishweb and not set.
        """
        self.data_dir = data_dir or os.getenv("FISHWEB_DATA_DIR", "")

        if not data_dir:
            raise AssertionError("No data dir defined")

    def Drive(self, name: str) -> _Drive:
        """
        Create or retrieve Drive instance.

        Args:
            name (str): The name of the Drive.

        Returns:
            Drive: The Drive instance associated with the name.
        """
        return _Drive(name=name, data_dir=self.data_dir)

    def Base(self, name: str) -> _Base:
        """
        Create or retrieve Base instance.

        Args:
            name (str): The name of the Base.

        Returns:
            Base: The Base instance associated with the name.
        """
        return _Base(name=name, data_dir=self.data_dir)


def Drive(name: str, data_dir: str | None = None) -> _Drive:
    """
    Create or retrieve Drive instance.

    Args:
        name (str): The name of the Drive.
        data_dir (str): The directory where data is stored.

    Returns:
        Drive: The Drive instance associated with the name.
    """

    data_dir = data_dir or os.getenv("FISHWEB_DATA_DIR", "") or "./"

    if not data_dir:
        raise AssertionError("No data dir defined")

    return _Drive(name=name, data_dir=data_dir)


def Base(name: str, data_dir: str | None = None, file_name: str = "arowana.db") -> _Base:
    """
    Create or retrieve Base instance.

    Args:
        name (str): The name of the Base.
        data_dir (str): The directory where data is stored.
        file_name (str): Name of the sqlite file, has to end with the .db extension.

    Returns:
        Base: The Base instance associated with the name.
    """

    data_dir = data_dir or os.getenv("FISHWEB_DATA_DIR", "") or "./"

    if not data_dir:
        raise AssertionError("No data dir defined")

    return _Base(name=name, data_dir=data_dir, file_name=file_name)
