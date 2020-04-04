from typing import Tuple

import numpy as np
from skimage import io


def open_rgb(
        file_path: str,
        control_channel: int = 0,
        probe_channel: int = 1
) -> Tuple[np.ndarray, np.ndarray]:
    """ Opens RGB images and returns the control and probe images

    Parameters
    -----------
    file_path : str
        Path to the RGB tif to open
    control_channel : int
        Index for the control channel. Default is 0.
    probe_channel : int
        Index for the probe channel. Default is 1.

    Returns
    -----------
    control_im : np.ndarray
        Single plane control image
    probe_im : np.ndarray
        Single plane probe image

    """
    im = io.imread(file_path)
    control_im = im[:, :, control_channel]
    probe_im = im[:, :, probe_channel]

    return control_im, probe_im
