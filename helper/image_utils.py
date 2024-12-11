import cv2
import numpy as np
from typing import Any, List

import core.constants as core_consts


def create_border_image(
    image: np.ndarray, pad: List[int] = core_consts.BORDER_PADDING
) -> tuple[np.ndarray, np.ndarray]:
    """Return border-extended image in both BGR and grayscale."""

    padx, pady = pad
    border_image = cv2.copyMakeBorder(
        image,
        pady,
        pady,
        padx,
        padx,
        cv2.BORDER_CONSTANT,
        value=core_consts.COLOR_BACKGROUND,
    )

    img = border_image.copy()
    background = np.all(img >= core_consts.BG_THRESHOLD, axis=-1)
    img[background] = core_consts.COLOR_WHITE
    border_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return border_image, border_gray


def check_single(
    border_image: np.ndarray,
    contour: dict[str, Any],
    upp_chip_area: float,
) -> List[dict[str, Any]]:
    """Return contours broken into smaller chips if possible."""

    if upp_chip_area < contour["area"]:
        blank = np.zeros(border_image.shape[:2], np.uint8)
        cv2.drawContours(blank, [contour["contour"]], -1, core_consts.COLOR_WHITE, -1)

        x, y = np.intp(cv2.minAreaRect(contour["contour"])[0])
        x_crop, y_crop = core_consts.BORDER_PADDING
        crop = blank[
            y - y_crop // 2 : y + y_crop // 2, x - x_crop // 2 : x + x_crop // 2
        ]

        # Erode the image to detect smaller chips
        for i in range(1, 15):
            for j in range(1, 15):
                crop[:] = cv2.erode(crop, np.ones((i, j), np.uint8))
                new_cnts, _ = cv2.findContours(
                    blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                if len(new_cnts) == 0:
                    break
                elif len(new_cnts) > 1:
                    contour_arr = []
                    for cnt in new_cnts:
                        area = cv2.contourArea(cnt)
                        rect = cv2.minAreaRect(cnt)
                        width, height = rect[1]
                        contour_arr.append(
                            {
                                "contour": cnt,
                                "area": area,
                                "length": min(width, height),
                                "rect": rect,
                            }
                        )
                    return contour_arr

    return [contour]
