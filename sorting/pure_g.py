import cv2
import numpy as np
from pathlib import Path
from shutil import copyfile

import core.constants as core_consts
from core.directory import directory
from helper.base import initialize_cleaner
from helper.debug import cvWin


def retrieve_pure_g(
    path: str,
    erode: list[int],
    close: list[int],
    save_path: str = "",
    debug: bool = False,
) -> None:
    """Retrieve images containing pure green channel and save them if required."""

    if not path:
        return

    path_list = (directory.images_dir / path).rglob("*.png")

    for image_path in path_list:
        image = cv2.imread(str(image_path))

        if image is None:
            continue  # Skip if the image cannot be loaded

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

        if debug:
            cvWin(hsv_mask)

        if save_path and not hsv_mask.sum():  # Ensure no pure green areas
            save_dir = Path(save_path)
            save_dir.mkdir(parents=True, exist_ok=True)
            file_name = image_path.name
            copyfile(str(image_path), str(save_dir / file_name))
