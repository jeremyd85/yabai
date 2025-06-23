import subprocess
import json
from dataclasses import dataclass, field
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    from .window import Window
# import window

def restart() -> bool:
    return subprocess.run(["yabai", "--restart-service"]).returncode == 0

@dataclass
class Frame:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0

    @staticmethod
    def from_dict(d: dict) -> "Frame":
        return Frame(
            x=d["x"], y=d["y"], width=d["w"], height=d["h"]
        )

    def to_dict(self) -> dict[str, float]:
        return vars(self)


@dataclass
class Space:
    id: int = 0
    uuid: str = ""
    index: int = 0
    label: str = ""
    type: str = ""
    display: int = 0
    window_ids: list[int] = field(default_factory=list)
    first_window_id: int = 0
    last_window_id: int = 0
    has_focus: bool = False
    is_visible: bool = False
    is_native_fullscreen: bool = False

    @staticmethod
    def from_dict(d: dict) -> "Space":
        space = Space()
        for k, v in d.items():
            k.replace("-", "_")
            setattr(space, k, v)
        return space


class Layout(Enum):
    BSP = "bsp"
    FLOAT = "float"

class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

class WindowSelectType(Enum):
    PREV = "prev"
    NEXT = "next"
    FIRST = "first"
    LAST = "last"
    RECENT = "recent"
    MOUSE = "mouse"
    LARGEST = "largest"
    SMALLEST = "smallest"
    SIBLING = "sibling"
    FIRST_NEPHEW = "first_nephew"
    SECOND_NEPHEW = "second_nephew"
    UNCLE = "uncle"
    FIRST_COUSIN = "first_cousin"
    SECOND_COUSIN = "second_cousin"
    ID = "id"


@dataclass
class WindowSelect:
    select_type: WindowSelectType = WindowSelectType.RECENT
    window_id: int | None = None

    @staticmethod
    def from_id(window_id: int) -> "WindowSelect":
        return WindowSelect(select_type=WindowSelectType.ID, window_id=window_id)
    
    @staticmethod
    def from_type(select_type: WindowSelectType) -> "WindowSelect":
        return WindowSelect(select_type=select_type, window_id=None)
    
    @staticmethod
    def from_window(window: "Window") -> "WindowSelect":
        return WindowSelect.from_id(window.id)
    
    def __str__(self) -> str:
        if self.select_type == WindowSelectType.ID:
            return str(self.window_id)
        return self.select_type.value
        




    