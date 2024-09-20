from fileHandle.base import read_json, write_json
import core.constants as core_consts
from core.directory import directory

SETTINGS_JSON_PATH = directory.json_dir / core_consts.SETTINGS_FILENAME


def validate_settings_format(settings: dict[str, dict[str, list[int]]]) -> str | None:
    """Validate the format of the settings data."""

    for key in core_consts.DEFAULT_SETTINGS:
        if key not in settings:
            return f"missing key: {key}."

        missing_sub_keys = [
            k for k in core_consts.DEFAULT_SETTINGS[key] if k not in settings[key]
        ]
        if missing_sub_keys:
            return f"missing sub-keys: {', '.join(missing_sub_keys)} in key: {key}."

        invalid_lists = [
            k
            for k, value in settings[key].items()
            if not (
                isinstance(value, list)
                and len(value) == 2
                and all(isinstance(v, int) for v in value)
            )
        ]
        if invalid_lists:
            return f"invalid lists for keys: {', '.join(invalid_lists)} in key: {key}."

    return None


def read_settings_json() -> list[dict[str, str | dict[str, list[int]]]] | list:
    """Retrieve the settings from the settings JSON file."""
    return read_json(SETTINGS_JSON_PATH).get("settingsGroup", [])


def get_settings_json(item: str) -> dict[str, dict[str, list[int]]]:
    """Retrieve and validate settings for a specific item from the settings JSON file."""

    settings_group = read_settings_json()
    settings = next(
        (
            item_data["settings"]
            for item_data in settings_group
            if item_data["item"] == item
        ),
        None,
    )

    if not settings:
        print(f"Item: {item} not found in settings file.")
        settings = core_consts.DEFAULT_SETTINGS

    std_out = validate_settings_format(settings)
    if std_out:
        print(f"Item: {item} {std_out}")

    return settings


def write_settings_json(
    item: str,
    settings_data: dict[str, dict[str, list[int]]] = core_consts.DEFAULT_SETTINGS,
) -> None:
    """Write settings data for a specific item to the settings JSON file."""

    settings_group = read_settings_json()

    std_out = validate_settings_format(settings_data)
    if std_out:
        print(f"Item: {item} {std_out}")

    # Update or append the settings
    for item_data in settings_group:
        if item_data["item"] == item:
            item_data["settings"] = settings_data
            break
    else:
        settings_group.append({"item": item, "settings": settings_data})

    write_json(SETTINGS_JSON_PATH, {"settingsGroup": settings_group})
