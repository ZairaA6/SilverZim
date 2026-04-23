from dataclasses import dataclass, field

@dataclass
class RaceState:
    user_angle: float = 0
    user_speed: float = 0
    user_start: bool = True
    x: float = 0 # user x and y coordinates
    y: float = 0
    lap_count: int = 1
    drs_on: bool = False
    acceleration: float = 0.15
    pitstop_screen_show: bool = False
    tyre_compound: str = "Medium"
    current_generation: int = 0
    checkpoint_flags: list = field(default_factory=list)
    sim_success: bool = True