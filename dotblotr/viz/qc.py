from os import path
from typing import Tuple

import cv2
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
from skimage import io


def plot_detected_dots(
        results_table:pd.DataFrame,
        strip_id:str,
        image_directory:str,
        image_extension:str = '.tif',
        font_scale:float = 1,
        font_color: Tuple[int, int, int] = (255, 255, 255),
        line_thickness:int = 2

) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
    """ plot the detected spot labels overlaid on the strip image.

    Parameters
    ----------
    results_table : pd.DataFrame
        the table that is the output of dotblotr.process.process_dir()
    strip_id : str
        the identifier for the strip to be plotted. This is the value from
        the strip_id column of the results_table. strip_id should be passed as a string.
    image_directory : str
        the path to the directory containing the strip images.
        This is the same as used in process_dir() to generate the results_table
    image_extension : str
        The image extension for the strip image. Default value is '.tif'
    font_scale : float
        The multiplier for setting the font size.
    font_color : Tuple[int, int, int]
        RGB tuple for the font color. Default value is (255, 255, 255).
    line_thickness : int
        The line thickness is pixels. Default value is 2.

    Returns
    -------
    f : matplotlib.figure.Figure
        matplotlib figure handle for the resulting plot
    ax : matplotlib.axes._subplots.AxesSubplot
        matplot axis handle for the resulting plot

    """

    im_name = strip_id + image_extension
    image_path = path.join(image_directory, im_name)
    im = io.imread(image_path)

    strip_results = results_table.loc[results_table['strip_id'] == strip_id]

    font = cv2.FONT_HERSHEY_SIMPLEX
    line_type = cv2.LINE_AA

    for i, row in strip_results.iterrows():
        well_name = row['dot_name']
        x = row['x']
        y = row['y']
        text_size, baseline = cv2.getTextSize(
            text=well_name,
            fontFace=font,
            fontScale=font_scale,
            thickness=line_thickness
        )

        x_centered = int(x - (text_size[0] / 2))
        y_centered = int(y + (text_size[1] / 2))

        cv2.putText(
            img=im,
            text=well_name,
            org=(x_centered, y_centered),
            fontFace=font,
            fontScale=font_scale,
            color=font_color,
            lineType=line_type,
            thickness=line_thickness
        )

    f, ax = plt.subplots(figsize=(15, 12))
    ax.imshow(im)

    return f, ax
