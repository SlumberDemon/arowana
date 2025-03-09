from __future__ import annotations

import os
from io import BufferedIOBase, RawIOBase, TextIOBase
from pathlib import Path


class _Drive:
    def __init__(self, name: str, data_dir: str) -> None:
        self.drive_path = Path(data_dir, name)

    def put(
        self,
        name: str,
        data: str | bytes | TextIOBase | BufferedIOBase | RawIOBase | None = None,
        path: str | Path | None = None,
    ) -> str:
        """
        Put file

        Args:
            name: Name and path of the file
            data: Data content of file
            path: Path of file to get content from

        Returns:
            str: Name of the file
        """
        if not (path or data):
            raise ValueError("Missing data or path")
        if path and data:
            raise ValueError("Both path and data given")

        file = Path(self.drive_path, name)
        file.parent.mkdir(parents=True, exist_ok=True)

        if path:
            with Path.open(Path(path), "rb") as f:
                content = f.read()

            with Path.open(file, "wb") as f:
                f.write(content)
        else:
            with Path.open(file, "wb") as f:
                if isinstance(data, str):
                    data = data.encode("utf-8")
                f.write(data)

        return name

    def get(self, name: str) -> bytes | None:
        """
        Get file content

        Args:
            name: Name and path of the file

        Returns:
            bytes: File bytes
        """
        file = Path(self.drive_path, name)

        if file.exists():
            return file.read_bytes()
        return None

    def list(self, prefix: str | None = None) -> list:
        """
        List all files

        Args:
            prefix: Prefix that file names start with

        Returns:
            list: List of file names
        """

        files = []

        for path in self.drive_path.rglob("*"):
            if path.is_file():
                rel_path = str(path.relative_to(self.drive_path)).replace("\\", "/")
                if prefix is None or rel_path.startswith(prefix):
                    files.append(rel_path)

        return files

    def delete(self, name: str) -> str:
        """
        Delete file

        Args:
            name: Name and path of the file

        Returns:
            str: Name of the deleted file
        """
        file = Path(self.drive_path, name)

        if file.exists() and not file.is_dir():
            file.unlink()
            if file.parent != self.drive_path and len(os.listdir(file.parent)) == 0:
                file.parent.rmdir()

        return name
