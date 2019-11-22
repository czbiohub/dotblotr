from typing import List, Union

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from dotblotr import BlotData

GRID_SPACING = 10


def plot_zscore(
        blot_df: pd.DataFrame,
        col_labels: Union[None, List[str]]=None,
        row_labels: Union[None, List[str]]=None
):
    """
    Plot the z score of each spot in a scatter plot.

    Paramters:
    ----------
    blot_df : pd.DataFrame
        A dataframe containing the blot coordinates and intensities
    col_labels : List[str]
        A list containing the label for each column.
    row_labels : List[str]
        A list containing the label for each row.

    Returns:
    --------
    f : fig handle
        The matplotlib figure handle
    ax : axis handle
        The matplotlib axis handle
    cb : colorbar handle
        The matplotlib colorbar handle

    """
    # Get the coordinates for the blots
    x = blot_df.col.values
    y = blot_df.row.values

    # Calculate the z score
    mean_intensity = blot_df.mean_intensity.values
    z_score = (mean_intensity - np.mean(mean_intensity)) / np.std(mean_intensity)

    # Plot
    f, ax = plt.subplots(figsize=(8, 5))
    ax.invert_yaxis()
    sct = ax.scatter(x, y, c=z_score)
    cb = f.colorbar(sct)
    cb.set_label('Z score', rotation=270)

    ax.set_ylabel('Row')
    ax.set_xlabel('Column')

    return f, ax, cb
