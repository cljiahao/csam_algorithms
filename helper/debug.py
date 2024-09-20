import cv2
import numpy as np


def cvWin(image: np.ndarray, name: str = "image") -> None:
    """Display an image using OpenCV for debugging purposes.

    Args:
        image (np.ndarray): The image to be displayed.
        name (str): The name of the window. Defaults to "image".
    """

    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
