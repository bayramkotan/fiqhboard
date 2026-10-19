"""Settings, without Qt (the window and the command line share them).

Kept as settings.json in the data folder; only values that differ from the
default are written.

Data folder: FIQHBOARD_DATA_DIR if set, otherwise
  Linux    ~/.local/share/fiqhboard   (XDG_DATA_HOME)
  Windows  %LOCALAPPDATA%\\fiqhboard
  macOS    ~/Library/Application Support/fiqhboard
"""

import json
import os
import sys
from pathlib import Path

THEMES = ("system", "light", "dark", "paper", "slate", "emerald", "midnight", "contrast")
CONTENT_LANGUAGES = ("en", "tr", "ar")

DEFAULTS = {
    "view.theme": "system",
    "view.text_scale": 1.0,
    "content.language": "en",
}


class ConfigError(ValueError):
    pass


def data_dir() -> Path:
    env = os.environ.get("FIQHBOARD_DATA_DIR")
    if env:
        path = Path(env).expanduser()
    elif sys.platform == "win32":
        path = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "fiqhboard"
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / "fiqhboard"
    else:
        path = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "fiqhboard"
    return path


def settings_path() -> Path:
    return data_dir() / "settings.json"


def _read() -> dict:
    try:
        data = json.loads(settings_path().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _write(data: dict) -> None:
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def validate(key: str, value):
    if key not in DEFAULTS:
        raise ConfigError(f"unknown setting: {key}")
    if key == "view.theme":
        if value not in THEMES:
            raise ConfigError(f"{key} must be one of: {', '.join(THEMES)}")
        return value
    if key == "view.text_scale":
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ConfigError(f"{key} must be a number") from None
        if not 0.8 <= number <= 1.6:
            raise ConfigError(f"{key} must be between 0.8 and 1.6")
        return round(number, 2)
    if key == "content.language":
        if value not in CONTENT_LANGUAGES:
            raise ConfigError(f"{key} must be one of: {', '.join(CONTENT_LANGUAGES)}")
        return value
    return value


def get(key: str):
    if key not in DEFAULTS:
        raise ConfigError(f"unknown setting: {key}")
    value = _read().get(key)
    if value is None:
        return DEFAULTS[key]
    try:
        return validate(key, value)
    except ConfigError:
        return DEFAULTS[key]


def set(key: str, value) -> None:    # noqa: A001 — the natural name for a settings module
    value = validate(key, value)
    data = _read()
    if value == DEFAULTS[key]:
        data.pop(key, None)
    else:
        data[key] = value
    _write(data)
