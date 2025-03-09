from __future__ import annotations

import os
from .drive import _Drive
from .base import _Base


class Arowana:
    def __init__(self, data_dir: str | None = None) -> None:
        """
        Initialize an Arowana instance.

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


def Drive(name: str) -> _Drive:
    """
    Create or retrieve Drive instance.

    Args:
        name (str): The name of the Drive.

    Returns:
        Drive: The Drive instance associated with the name.
    """
    data_dir = os.getenv("FISHWEB_DATA_DIR", "") or "data"
    return _Drive(name=name, data_dir=data_dir)


def Base(name: str) -> _Base:
    """
    Create or retrieve Base instance.

    Args:
        name (str): The name of the Base.

    Returns:
        Base: The Base instance associated with the name.
    """
    data_dir = os.getenv("FISHWEB_DATA_DIR", "") or "data"
    return _Base(name=name, data_dir=data_dir)
