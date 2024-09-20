import cv2
import numpy as np
from pathlib import Path
from typing import Any

import core.constants as core_consts
from core.directory import directory
from helper.base import defects_extract, initialize_cleaner
from helper.debug import cvWin
from helper.random import get_random_size


def color_impose(
    ng_dir: str,
    g_dir: str,
    erode: list[int],
    close: list[int],
    csam_colors: dict[str, Any],
    save_path: str = "",
    debug: bool = False,
) -> None:
    """Superimposes defects from NG images onto G images."""
    if not (ng_dir and g_dir):
        return

    defects_list = defects_extract(ng_dir, erode, close)
    sizes_list = list(set(defect["size"] for defect in defects_list))

    len_of_files = len(list((directory.images_dir / g_dir).rglob("*.png")))
    balanced_len = len_of_files / len(csam_colors)
    colors_count = {color["name"]: 0 for color in csam_colors}

    path_list = (directory.images_dir / g_dir).rglob("*.png")
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

        color_prob = [
            round((balanced_len - colors_count[color["name"]]) / len_of_files, 3)
            for color in csam_colors[:-1]
        ]
        color_prob.append(round(1 - sum(color_prob), 3))
        selected_color = np.random.choice(csam_colors, 1, color_prob)[0]
        colors_count[selected_color["name"]] += 1

        selected_size = get_random_size(sizes_list)

        impose_image = defects_impose(
            border_image, single_chip_mask, defects_list, selected_size, selected_color
        )
        original_size_image = impose_image[pad[0] : img_shape[0], pad[1] : img_shape[1]]

        if debug:
            cvWin(original_size_image)

        if save_path:
            save_dir = Path(save_path)
            save_dir.mkdir(parents=True, exist_ok=True)
            file_name = image_path.name
            cv2.imwrite(str(save_dir / f"aug_{file_name}"), original_size_image)


def defects_impose(
    image: np.ndarray,
    single_chip_mask: np.ndarray,
    defects_list: list[dict[str, Any]],
    selected_size: str,
    selected_color: dict[str, Any],
) -> np.ndarray:
    """Imposes a defect on the image using the selected color and size."""
    selected_defects_list = [
        defect for defect in defects_list if defect["size"] in selected_size
    ]
    selected_defect = np.random.choice(selected_defects_list, 1)[0]

    pre_defect_mask = cv2.bitwise_and(single_chip_mask, selected_defect["mask"])
    image[pre_defect_mask > 0] = selected_color["hex"]

    return image
