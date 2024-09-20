import cv2
import numpy as np

from core.directory import directory
from fileHandle.json import get_settings_json, write_settings_json
from helper.debug import cvWin
from helper.image_calc import denoise_mask_image
from helper.image_utils import create_border_image
from helper.mask import erode_close


def auto_batch_finder(
    path: str, no_of_batches: int, item: str | bool = False, debug: bool = False
) -> None:
    """Finds optimal batch parameters and optionally updates settings."""

    file_path = directory.images_dir / path
    if not path or not file_path.exists():
        return

    image = cv2.imread(str(file_path))
    border_image, border_gray = create_border_image(image)
    _, binary_image = cv2.threshold(border_gray, 250, 255, cv2.THRESH_BINARY_INV)

    for erode in range(2, 30):
        for close in range(2, 50):
            count_diff = evaluation(binary_image, no_of_batches, erode, close)
            if count_diff == 0:
                best_params = {"erode": [erode, erode], "close": [close, close]}
                print(best_params)
                if debug:
                    mask_img = erode_close(binary_image, (erode, erode), (close, close))
                    confirmed_batch = cv2.bitwise_and(
                        border_image, border_image, mask=mask_img
                    )
                    cvWin(confirmed_batch)
                if item:
                    settings = get_settings_json(item)
                    settings["batch"] = best_params
                    write_settings_json(item, settings)
                return


def evaluation(
    binary_image: np.ndarray, no_of_batches: int, erode: int, close: int
) -> int:
    """Evaluates the difference between found contours and target batch count."""

    mask_img = erode_close(binary_image, (erode, erode), (close, close))
    contours = denoise_mask_image(mask_img)

    return abs(no_of_batches - len(contours))
