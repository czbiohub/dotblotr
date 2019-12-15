from typing import List, Union

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from dotblotr import BlotData

GRID_SPACING = 10


def _make_blot_plot(x, y, c):
    f, ax = plt.subplots(figsize=(8, 5))
    ax.invert_yaxis()
    sct = ax.scatter(x, y, c=c)
    cb = f.colorbar(sct)
    cb.set_label('Z score', rotation=270)

    ax.set_ylabel('Row')
    ax.set_xlabel('Column')

    return f, ax, cb


def plot_zscore(
        blot_df: pd.DataFrame,
        col_label: str = 'mean_intensity',
):
    """
    Plot the z score of each spot in a scatter plot.

    Paramters:
    ----------
    blot_df : pd.DataFrame
        A dataframe containing the blot coordinates and intensities
    col_label :  str
        Label of the column to plot

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
    data = blot_df[col_label].values
    z_score = (data - np.mean(data)) / np.std(data)

    # Plot
    f, ax, cb = _make_blot_plot(x, y, z_score)

    return f, ax, cb


def plot_value(blot_df: pd.DataFrame, col_label: str):

    # Get the coordinates for the blots
    x = blot_df.col.values
    y = blot_df.row.values

    # Calculate the z score
    data = blot_df[col_label].values

    # Plot
    f, ax, cb = _make_blot_plot(x, y, data)

    return f, ax, cb
