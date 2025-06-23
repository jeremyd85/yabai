import subprocess
from . import Direction, WindowSelect, Frame
import json
from dataclasses import dataclass
import typing
if typing.TYPE_CHECKING:
    from . import Space

@dataclass
class Window:
    id: int = 0
    pid: int = 0
    app: str = ""
    title: str = ""
    frame: Frame | None = None
    role: str = ""
    subrole: str = ""
    display: int = 0
    space: int = 0
    level: int = 0
    layer: str = ""
    opacity: float = 0.0
    split_type: str = ""
    split_child: str = ""
    stack_index: int = 0
    can_move: bool = False
    can_resize: bool = False
    has_focus: bool = False
    has_shadow: bool = False
    has_parent_zoom: bool = False
    has_fullscreen_zoom: bool = False
    is_native_fullscreen: bool = False
    is_visible: bool = False
    is_minimized: bool = False
    is_hidden: bool = False
    is_floating: bool = False
    is_sticky: bool = False
    is_grabbed: bool = False

    @staticmethod
    def from_dict(d: dict) -> "Window":
        window = Window()
        for k, v in d.items():
            if k == "frame":
                setattr(window, k, Frame.from_dict(v))
            else:
                k.replace("-", "_")
                setattr(window, k, v)
        return window
    
    def to_dict(self) -> dict[str, str | bool | dict | float | int]:
        data = vars(self)
        data["frame"] = self.frame.to_dict()
        return data

    def focus(self) -> bool:
        return focus(WindowSelect.from_window(self))
    
    def switch_space(self, space_index: int = -1) -> bool:
        return space(WindowSelect.from_window(self), space_index)
    
    def update_frame(self, frame: Frame) -> bool:
        process = subprocess.run(["yabai", "-m", "window", str(self.id), "--move", f"{frame.x}:{frame.y}", "--resize", f"{frame.width}:{frame.height}"])
        return process.returncode == 0

def swap(window: WindowSelect | None, direction: Direction) -> bool:
    cmd = ["yabai", "-m", "window"]
    if window is not None:
        cmd.append(str(window))
    cmd.extend(["--swap", direction.value])
    return subprocess.run(cmd).returncode == 0

def focus(window: WindowSelect | None) -> bool:
    cmd = ["yabai", "-m", "window"]
    if window is not None:
        cmd.append(str(window))
    cmd.append("--focus")
    return subprocess.run(cmd).returncode == 0

def space(window: WindowSelect | None, space_index: int = -1) -> bool:
    if space_index == -1:
        return False
    cmd = ["yabai", "-m", "window"]
    if window is not None:
        cmd.append(str(window))
    cmd.extend(["--space", str(space_index)])
    return subprocess.run(cmd).returncode == 0

def toggle_float(window: WindowSelect | None) -> bool:
    cmd = ["yabai", "-m", "window"]
    if window is not None:
        cmd.append(str(window))
    cmd.extend(["--toggle", "float"])
    return subprocess.run(cmd).returncode == 0