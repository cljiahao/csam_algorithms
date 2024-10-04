import cv2
from pathlib import Path

import core.constants as core_consts
from core.directory import directory
from helper.base import initialize_cleaner
from helper.debug import cvWin
from helper.image_calc import get_median_area
from helper.image_utils import check_single


def chip_dotter(
    path: str,
    erode: list[int],
    close: list[int],
    save_path: str = "",
    debug: bool = False,
) -> None:
    """Detects chip locations on an image and marks them with dots."""

    file_path = directory.images_dir / path
    if not path or not file_path.exists():
        return

    image = cv2.imread(str(file_path))
    border_image, clean_contours = initialize_cleaner(image, erode=erode, close=close)

    avg_chip_area = get_median_area(clean_contours)
    thres_range = {k: v * avg_chip_area for k, v in core_consts.THRESH_RANGE.items()}

    padx, pady = core_consts.BORDER_PADDING
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
                ((xc, yc), _, _) = contour["rect"]
                cv2.circle(
                    image,
                    (int(xc - padx), int(yc - pady)),
                    10,
                    core_consts.COLOR_WHITE,
                    -1,
                )
                no_of_chips += 1

    print(no_of_chips)

    if debug:
        cvWin(image)

    if save_path:
        save_path = Path(save_path)
        if save_path.exists():
            file_name = Path(path).name
            cv2.imwrite(str(save_path / f"dotter_{file_name}"), image)
