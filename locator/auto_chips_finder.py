import cv2
import numpy as np

import core.constants as core_consts
from core.directory import directory
from fileHandle.json import get_settings_json, write_settings_json
from helper.image_utils import check_single, create_border_image
from helper.image_calc import denoise_mask_image, get_median_area
from helper.mask import erode_close
from locator.chip_dotter import chip_dotter


def auto_chips_finder(
    path: str, no_of_chips: int, item: str | bool = False, debug: bool = False
) -> None:
    """Finds optimal chip parameters and optionally updates settings."""

    file_path = directory.images_dir / path
    if not path or not file_path.exists():
        return

    image = cv2.imread(str(file_path))
    _, border_gray = create_border_image(image)
    _, binary_image = cv2.threshold(border_gray, 250, 255, cv2.THRESH_BINARY_INV)

    for erode in range(2, 20):
        for close in range(2, 20):
            count_diff = evaluation(binary_image, no_of_chips, erode, close)
            if count_diff == 0:
                best_params = {"erode": [erode, erode], "close": [close, close]}
                print(best_params)
                if debug:
                    chip_dotter(
                        path, erode=[erode, erode], close=[close, close], debug=debug
                    )
                if item:
                    settings = get_settings_json(item)
                    settings["chip"] = best_params
                    write_settings_json(item, settings)
                return
            if int(no_of_chips * 0.1) < count_diff:
                break


def evaluation(
    binary_image: np.ndarray, no_of_chips: int, erode: int, close: int
) -> int:
    """Evaluates the difference between detected chips and the target chip count."""

    mask_img = erode_close(binary_image, (erode, erode), (close, close))
    contours = denoise_mask_image(mask_img)

    avg_chip_area = get_median_area(contours)
    thres_range = {k: v * avg_chip_area for k, v in core_consts.THRESH_RANGE.items()}
    large_chip_area = [
        cont for cont in contours if thres_range["upp_chip_area"] < cont["area"]
    ]

    current_count = len(contours)
    if large_chip_area:
        current_count -= len(large_chip_area)
        for c in large_chip_area:
            split_contours = check_single(binary_image, c, thres_range["upp_def_area"])
            current_count += len(split_contours)

    return abs(no_of_chips - current_count)
