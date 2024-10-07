import cv2
import math
import numpy as np
from PIL import Image
from pathlib import Path

import core.constants as core_consts
from core.directory import directory
from helper.base import initialize_cleaner
from helper.debug import cvWin
from helper.image_calc import get_median_area
from helper.image_utils import check_single


def auto_crop_calc(
    path: str,
    erode: list[int],
    close: list[int],
    save_path: str = "",
    debug: bool = False,
) -> None:
    """Performs cropping calculations and saves rotated images if needed."""

    file_path = directory.images_dir / path
    if not path or not file_path.exists():
        return

    image = cv2.imread(str(file_path))
    border_image, clean_contours = initialize_cleaner(image, erode=erode, close=close)

    average_length = np.median([obj["length"] for obj in clean_contours])
    nearest_pad = math.ceil(average_length * 2)

    avg_chip_area = get_median_area(clean_contours)
    thres_range = {k: v * avg_chip_area for k, v in core_consts.THRESH_RANGE.items()}


    no_of_chips = 0
    for clean_cnt in clean_contours:
        split_contours = check_single(
            border_image, clean_cnt, thres_range["upp_def_area"]
        )

        for contour in split_contours:
            if (
                thres_range["low_chip_area"]
                < contour["area"]
                < thres_range["upp_chip_area"]
            ):

                rotated_crop_images = rotate_chips(border_image, clean_cnt["rect"], nearest_pad)

                if debug:
                    cvWin(rotated_crop_images)

                if save_path:
                    save_image(save_path, no_of_chips, clean_cnt["rect"], rotated_crop_images)
                    no_of_chips += 1

    print(no_of_chips)

def rotate_chips(
    border_image: np.ndarray,
    rect: cv2.RotatedRect,
    pad: list[int] | int = core_consts.BORDER_PADDING,
) -> np.ndarray:
    """Returns a rotated and cropped chip image."""

    ((x, y), (width, height), theta) = rect
    if height < width:
        theta -= 90

    if isinstance(pad, int):
        pad = [pad, pad]

    crop = border_image[
        int(y - pad[1]) : int(y + pad[1]),
        int(x - pad[0]) : int(x + pad[0]),
    ]

    pil_image = Image.fromarray(crop)
    rotated_image = np.asarray(pil_image.rotate(theta))

    return rotated_image[
        pad[1] // 2 : pad[1] * 3 // 2,
        pad[0] // 2 : pad[0] * 3 // 2,
    ]


def save_image(
    save_path: str, no_of_chips: int, rect: cv2.RotatedRect, image: np.ndarray
) -> None:
    """Saves the processed chip image to the specified path."""

    save_path = Path(save_path)
    if not save_path.exists():
        return

    pad = core_consts.BORDER_PADDING
    ((xc, yc), _, _) = rect
    file_name = f"0_batch_{no_of_chips}_{int(xc - pad[0])}_{int(yc - pad[1])}.png"
    cv2.imwrite(str(save_path / file_name), image)
