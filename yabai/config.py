from . import Layout
import subprocess

def layout(layout: Layout) -> bool:
    return subprocess.run(["yabai", "-m", "config", "layout", layout.value]).returncode == 0

def active_window_border_color(color: str) -> bool:
    return subprocess.run(["yabai", "-m", "config", "active_window_border_color", color]).returncode == 0