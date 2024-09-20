# JSON File Names
SETTINGS_FILENAME: str = "settings.json"
COLOR_GROUP_FILENAME: str = "colors.json"

# Image Processing
BORDER_PADDING: list[int] = [54, 54]  # Must be even numbers
DENOISE_THRESHOLD: int = 10
BG_THRESHOLD: int = 130
THRESH_RANGE: dict[str, float] = {
    "low_chip_area": 0.15,
    "upp_chip_area": 3,
    "low_def_area": 0.75,
    "upp_def_area": 1.5,
}
DEFAULT_SETTINGS = {
    "batch": {"erode": [1, 1], "close": [1, 1]},
    "chip": {"erode": [1, 1], "close": [1, 1]},
}
DEFAULT_COLORS = {"NG": "#ffff00", "Others": "#00ffff"}

# Types / Modes
G_TYPES: list[str] = ["G", "Good", "g", "good"]
DEFECT_SIZES: dict[str, float] = {"small": 0.7, "medium": 0.2, "big": 0.1}

# COLORS
COLOR_BACKGROUND: list[int, int, int] = [192, 192, 192]
COLOR_WHITE: list[int, int, int] = [255, 255, 255]
COLOR_BLACK: list[int, int, int] = [0, 0, 0]
COLOR_BLUE: list[int, int, int] = [255, 0, 0]
COLOR_GREEN: list[int, int, int] = [0, 255, 0]
COLOR_RED: list[int, int, int] = [0, 0, 255]
COLOR_YELLOW: list[int, int, int] = [0, 255, 255]
COLOR_CYAN: list[int, int, int] = [255, 255, 0]
COLOR_ORANGE: list[int, int, int] = [0, 191, 255]
COLOR_LIME: list[int, int, int] = [255, 192, 0]
