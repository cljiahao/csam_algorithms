import os
import cv2
import numpy as np
from typing import Any, List, Dict

import core.constants as core_consts
from core.exceptions import ImageProcessError
from fileHandle.json import get_settings_json


def denoise_mask_image(mask_image: np.ndarray) -> List[Dict[str, Any]]:
    """Remove noise from mask image and return contours with their areas."""

    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    clean_contours = []
    for cnt in contours:
        chip_area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        if chip_area > core_consts.DENOISE_THRESHOLD:
            (_, (width, height), _) = rect
            clean_contours.append(
                {
                    "contour": cnt,
                    "area": chip_area,
                    "length": max(width, height),
                    "rect": rect,
                }
            )

    if not clean_contours:
        std_out = "Contour length = 0, unable to find median area."
        print(std_out)
        raise ImageProcessError(std_out)

    return clean_contours


def chunking(contours: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Divide contours into chunks based on CPU core count for multiprocessing."""

    cpu_count = os.cpu_count() or 1
    chunk_size = max(1, len(contours) // cpu_count)
    chunk_contours = [
        contours[i : i + chunk_size] for i in range(0, len(contours), chunk_size)
    ]
    print("Chunk size:", chunk_size, "based on CPU Count:", cpu_count)

    return chunk_contours


def get_median_area(contours: List[Dict[str, Any]]) -> float:
    """Calculate and return the median area of contours."""

    contour_areas = [obj["area"] for obj in contours]
    avg_chip_area = np.median(contour_areas)
    print(f"Average Chip Area is {avg_chip_area}")

    return avg_chip_area


def find_batch_no(x: float, y: float, batch_data: List[Dict[str, float]]) -> int:
    """Return the batch number corresponding to given coordinates."""

    for i, coor in enumerate(batch_data):
        if x <= coor["x2"] and x >= coor["x1"] and y <= coor["y2"] and y >= coor["y1"]:
            return i + 1

    return 0


def retrieve_erode_close(
    item: str = "",
    erode: List[int] = None,
    close: List[int] = None,
    batch: bool = False,
) -> tuple[List[int], List[int]]:
    """Retrieve erode and close values based on item type or provided values."""

    if not (erode or close):
        if not item:
            raise ValueError(
                "Missing item type. Please provide erode and close values or an item type."
            )
        settings = get_settings_json(item)
        mode = "batch" if batch else "chip"
        erode = settings[mode]["erode"]
        close = settings[mode]["close"]

    return erode, close
