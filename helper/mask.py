import cv2
import numpy as np


def masking(
    gray: np.ndarray, erode_val: tuple[int, int], close_val: tuple[int, int]
) -> np.ndarray:
    """Create a mask from the grayscale image using thresholding and morphological transformations."""

    _, binary_image = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    mask_image = erode_close(binary_image, erode_val, close_val)

    return mask_image


def erode_close(
    binary_image: np.ndarray, erode_val: tuple[int, int], close_val: tuple[int, int]
) -> np.ndarray:
    """Apply morphological transformations: erosion and closing."""

    kernel_erode = np.ones(erode_val, np.uint8)
    kernel_close = np.ones(close_val, np.uint8)

    # Erode to prevent merging between batches
    eroded_image = cv2.morphologyEx(binary_image, cv2.MORPH_ERODE, kernel_erode)
    # Close to merge neighboring chips into a single blob mask
    closed_image = cv2.morphologyEx(eroded_image, cv2.MORPH_CLOSE, kernel_close)

    return closed_image
