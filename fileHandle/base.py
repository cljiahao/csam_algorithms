import json
from pathlib import Path


def read_json(file_path: str) -> dict:
    """Reads a JSON file and returns its content as a dictionary."""

    file_path = Path(file_path)
    if not file_path.exists():
        data = {}
        write_json(file_path, data)
    else:
        with open(file_path, "r") as f:
            data = json.load(f)

    return data


def write_json(file_path: str, data: dict) -> None:
    """Writes a dictionary to a JSON file."""

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def read_txt(file_path: str) -> list:
    """Reads a text file and returns its lines as a list of strings."""

    file_path = Path(file_path)
    if not file_path.exists():
        data = []
        write_txt(file_path, data)
    else:
        with open(file_path, "r") as f:
            data = f.readlines()

    return data


def write_txt(file_path: str, data: str) -> None:
    """Writes a string to a text file."""

    with open(file_path, "w") as f:
        f.write(data)
