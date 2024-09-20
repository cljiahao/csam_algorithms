import cv2
import numpy as np

import core.constants as core_consts
from core.directory import directory
from helper.image_calc import denoise_mask_image
from helper.image_utils import create_border_image
from helper.mask import masking


def initialize_cleaner(
    image: np.ndarray,
    pad: list[int] = core_consts.BORDER_PADDING,
    erode: list[int] = None,
    close: list[int] = None,
) -> tuple[np.ndarray, list[dict]]:
    """Initialize the cleaner for an image."""

    border_image, border_gray = create_border_image(image, pad)
    mask_image = masking(border_gray, erode, close)
    clean_contours = denoise_mask_image(mask_image)

    return border_image, clean_contours


def defects_extract(path: str, erode: list[int], close: list[int]) -> list[dict]:
    """Extract defects from images in the specified path."""

    defects_list = []
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

        size_ratio = np.sum(hsv_mask) / (2.55 * largest_contour["area"])
        size = "small" if size_ratio < 4 else "big" if size_ratio > 95 else "medium"

        defects_list.append(
            {
                "image": border_image,
                "mask": hsv_mask,
                "size": size,
            }
        )

    return defects_list
