import subprocess
import json
from dataclasses import dataclass, field
from . import Window, Space

def windows(has_focus: bool | None = None, ) -> list["Window"]:
    proc = subprocess.run(["yabai", "-m", "query", "--windows"], capture_output=True)
    if proc.returncode != 0:
        return []
    windows = json.loads(proc.stdout)
    filtered_windows = []
    for window_dict in windows:
        window = Window.from_dict(window_dict)
        if has_focus is not None and window.has_focus != has_focus:
            continue
        filtered_windows.append(window)
    return [Window.from_dict(window) for window in windows]

def spaces(has_focus: bool | None = None) -> list["Space"]:
    proc = subprocess.run(["yabai", "-m", "query", "--spaces"], capture_output=True)
    if proc.returncode != 0:
        return []
    spaces = json.loads(proc.stdout)
    filtered_spaces = []
    for space_dict in spaces:
        space = Space.from_dict(space_dict)
        if has_focus is not None and space.has_focus != has_focus:
            continue
        filtered_spaces.append(space)
    return [Space.from_dict(space) for space in spaces]
