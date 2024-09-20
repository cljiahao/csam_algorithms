import core.constants as core_consts
from core.directory import directory
from augments.base import color_impose, super_impose
from helper.image_calc import retrieve_erode_close
from locator.base import (
    auto_batch_finder,
    auto_chips_finder,
    auto_crop_calc,
    chip_dotter,
)
from sorting.base import color_sort, retrieve_pure_g

##### Instantiate: Do not touch this #####
save_path = ""
csam_img_file_path = ""
batch_file_path = ""
crop_file_path = ""
dot_file_path = ""
ng_dir = ""
g_dir = ""
##### Instantiate: Do not touch this #####

# csam_img_file_path = "locator/test.png"
# batch_file_path = "locator/test_batch_273_cv.png"
# batch_file_path = "locator/NG_378.png"
# batch_file_path = "locator/ng_image_395.png"
# batch_file_path = "locator/6000(NG)_394.png"

# crop_file_path = "locator/test_batch_273_cv.png"

# dot_file_path = "locator/test_batch_273_cv.png"
# dot_file_path = "locator/6000(NG)_394.png"
# dot_file_path = "locator/6000(NG)_8_batches.png"
# dot_file_path = "locator/6000(NG).png"

ng_dir = "augment/NG"
# g_dir = "augment/G"

# save_path = directory.images_dir

item = "GCM32ER71E106KA59_+B55-E01GJ"
no_of_batch = None
no_of_chips = None
erode = None
close = None
color = False
sorting = True
debug = True

csam_colors = [
    {
        "name": "blue",
        "hex": core_consts.COLOR_BLUE,
        "size": core_consts.DEFECT_SIZES,
    },
    {
        "name": "cyan",
        "hex": core_consts.COLOR_CYAN,
        "size": core_consts.DEFECT_SIZES,
    },
    {
        "name": "green",
        "hex": core_consts.COLOR_GREEN,
        "size": core_consts.DEFECT_SIZES,
    },
    {
        "name": "lime",
        "hex": core_consts.COLOR_LIME,
        "size": core_consts.DEFECT_SIZES,
    },
    {
        "name": "yellow",
        "hex": core_consts.COLOR_YELLOW,
        "size": core_consts.DEFECT_SIZES,
    },
    {
        "name": "black",
        "hex": core_consts.COLOR_BLACK,
        "size": [size for size in core_consts.DEFECT_SIZES if size not in ["small"]],
    },
    {
        "name": "orange",
        "hex": core_consts.COLOR_ORANGE,
        "size": [size for size in core_consts.DEFECT_SIZES if size not in ["big"]],
    },
]

if __name__ == "__main__":

    erode, close = retrieve_erode_close(item, erode, close)

    auto_batch_finder(csam_img_file_path, no_of_batch, item, debug)

    auto_chips_finder(batch_file_path, no_of_chips, item, debug)

    auto_crop_calc(crop_file_path, erode, close, save_path, debug)

    chip_dotter(dot_file_path, erode, close, save_path, debug)

    if color:
        color_impose(ng_dir, g_dir, erode, close, csam_colors, save_path, debug)
    else:
        super_impose(ng_dir, g_dir, erode, close, save_path, debug)

    if sorting:
        color_sort(ng_dir, erode, close, csam_colors, save_path, debug)

        retrieve_pure_g(g_dir, erode, close, save_path, debug)
