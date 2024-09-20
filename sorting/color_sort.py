import cv2
import numpy as np
from typing import Any, Dict
from pathlib import Path
from shutil import copyfile

import core.constants as core_consts
from core.directory import directory
from helper.base import initialize_cleaner
from helper.debug import cvWin


def color_sort(
    path: str,
    erode: list[int],
    close: list[int],
    csam_colors: Dict[str, Any],
    save_path: str = "",
    debug: bool = False,
) -> None:
    """Sort images based on chip color detection."""

    if not path:
        return

    path_list = (directory.images_dir / path).rglob("*.png")

    for image_path in path_list:
        image = cv2.imread(str(image_path))
        img_shape = image.shape[:2]
        pad = [(x - y) // 2 for x, y in zip(core_consts.BORDER_PADDING, img_shape)]

        border_image, clean_contours = initialize_cleaner(image, pad, erode, close)
        largest_contour = max(clean_contours, key=lambda x: x["area"])

        single_chip_mask = np.zeros(border_image.shape[:2], np.uint8)
        cv2.drawContours(
            single_chip_mask,
            [largest_contour["contour"]],
            -1,
            core_consts.COLOR_WHITE,
            -1,
        )

        single_chip = cv2.bitwise_and(border_image, border_image, mask=single_chip_mask)
        hsv = cv2.cvtColor(single_chip, cv2.COLOR_BGR2HSV_FULL)
        hsv_mask = cv2.inRange(hsv, np.array([1, 0, 0]), np.array([254, 255, 255]))
        defect = cv2.bitwise_and(single_chip, single_chip, mask=hsv_mask)

        color_type = check_color(defect, csam_colors)

        if debug:
            print(color_type)
            cvWin(defect)

        if save_path and not hsv_mask.sum():
            save_dir = Path(save_path) / color_type["name"]
            save_dir.mkdir(parents=True, exist_ok=True)
            file_name = image_path.name
            copyfile(str(image_path), str(save_dir / file_name))


def check_color(
    defect: np.ndarray,
    csam_colors: Dict[str, Any],
) -> Dict[str, Any]:
    """Determine the color type of the defect."""

    color_hexes, hex_count = np.unique(
        defect.reshape(-1, defect.shape[-1]), axis=0, return_counts=True
    )

    # Remove black (background) color
    color_hexes = np.delete(color_hexes, 0, axis=0)
    hex_count = np.delete(hex_count, 0, axis=0)

    # Find the most common color in the defect
    high_count_color = color_hexes[np.argmax(hex_count)]

    # Match the high count color to the csam_colors dictionary
    color_type = next(
        (
            color
            for color in csam_colors
            if np.array_equal(color["hex"], high_count_color)
        ),
        None,
    )

    return color_type
