import json

import cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from skimage import io

IM_WIDTH = 1500
IM_HEIGHT = 1000
DOT_SIZE = 20
CONTROL_INTENSITY = 50

ROW_PITCH = 50
ROW_OFFSET = 50
COL_PITCH = 50
COL_OFFSET = 50


def _make_intensity(row):
    if row['exp_group'] == 'neg':
        dot_intensity = np.random.randint(20, 30)
    elif row['exp_group'] == 'empty':
        dot_intensity = 0
    else:
        dot_intensity = np.random.randint(90, 110)

    return dot_intensity


def make_simulated_df(im_name: str = 'simulated_strip.tif'):
    """ Make a simulated image of a strip. The control image is in
    channel 1 and the probe images is in channel 2.

    Parameters:
    -----------
    im_name : str
        the file name of the simulated image
    """
    # load assay config
    with open('384_tiny_config.json') as json_file:
        assay_config = json.load(json_file)

    n_rows = assay_config['n_rows']
    n_cols = assay_config['n_cols']
    row_labels = assay_config['row_labels']
    col_labels = assay_config['col_labels']

    dot_names = {}
    n_dots = n_rows * n_cols
    nominal_dot_coords = np.zeros((n_dots, 2))
    i = 0
    for r in range(n_rows):
        for c in range(n_cols):
            x_coord = COL_OFFSET + (COL_PITCH * c)
            y_coord = ROW_OFFSET + (ROW_PITCH * r)
            nominal_dot_coords[i, :] = [x_coord, y_coord]

            dot_name = row_labels[r] + col_labels[c]
            dot_names[dot_name] = i
            i += 1

    nominal_dot_coords = np.array(nominal_dot_coords)

    # load the assay config
    assay_config = pd.read_csv('assay_config.csv')

    # make intensities for each dot
    np.random.seed(0)
    assay_config['dot_intensity'] = assay_config.apply(_make_intensity, axis=1)

    # get the coordinates of the dots in the assay
    assay_dot_names = assay_config['dot_name'].values
    assay_coords = np.array([nominal_dot_coords[dot_names[n]] for n in assay_dot_names])

    intensities = assay_config['dot_intensity'].astype('uint8').values

    # make the probe dots for the simulated image
    probe_im = np.zeros((IM_HEIGHT, IM_WIDTH, 3), dtype='uint8')
    for intensity, coord in zip(intensities, assay_coords):
        dot_intensity = tuple([int(0), int(intensity), int(0)])
        cv2.circle(probe_im, (int(coord[0]), int(coord[1])), int(DOT_SIZE), dot_intensity, cv2.FILLED)

    control_im = np.zeros((IM_HEIGHT, IM_WIDTH, 3), dtype='uint8')
    for coord in assay_coords:
        dot_intensity = tuple([int(CONTROL_INTENSITY), int(0), int(0)])
        cv2.circle(control_im, (int(coord[0]), int(coord[1])), int(DOT_SIZE), dot_intensity, cv2.FILLED)

    simulated_strip = control_im + probe_im

    io.imsave(im_name, simulated_strip)
