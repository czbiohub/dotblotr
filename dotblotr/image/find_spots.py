from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from skimage import io
from skimage.filters import threshold_local, median
from skimage.measure import label, regionprops
from skimage.morphology import closing, square, disk, erosion
from skimage.segmentation import clear_border
from sklearn.cluster import KMeans

from dotblotr import BlotConfig
from dotblotr import BlotData


def _load_image(im_path: str) -> np.ndarray:
    """
    Load an image from a given path

    Parameters:
    ----------
    im_path : str
        File path to an image.

    im : np.ndarray
        The image
    """

    im = io.imread(im_path)

    return im


def _calc_circularity(region):
    """
    Calculate the circularity of region.

    Parameters:
    -----------
    region :
        The region to calculate the circularity

    Returns:
    --------
    circularity : float
        The circularity
    """
    area = region.area
    perimeter = region.perimeter

    if perimeter > 0:
        circularity = 4 * area * np.pi / perimeter ** 2
    else:
        circularity = 0

    return circularity


def _find_indices(coords, n_indices):
    kmeans = KMeans(n_clusters=n_indices, random_state=0).fit(coords.reshape(-1, 1))
    labels = kmeans.labels_

    indices = np.argsort(kmeans.cluster_centers_.ravel()).argsort()

    return labels, indices


def _find_label_mapping(regions: List, blot_config: BlotConfig) -> Tuple[Dict, np.ndarray]:

    blob_labels = [r.label for r in regions]

    coords = np.array([r.centroid for r in regions])
    row_coords = coords[:, 0]
    col_coords = coords[:, 1]

    row_labels, row_indices = _find_indices(row_coords, blot_config.n_rows)
    col_labels, col_indices = _find_indices(col_coords, blot_config.n_cols)

    label_mapping = {}
    grid_coordinates = []
    for i, (row_index, col_index) in enumerate(zip(row_labels, col_labels)):
        r = row_indices[row_index]
        row_label = blot_config.get_row_label(r)

        c = col_indices[col_index]
        col_label = blot_config.get_col_label(c)

        blot_label = row_label + col_label

        label_mapping[blob_labels[i]] = blot_label

        grid_coordinates.append([r, c])

    return label_mapping, np.array(grid_coordinates)


def _make_blob_df(regions: List, label_mapping: Dict, grid_coordinates: np.ndarray) -> pd.DataFrame:

    areas = [r.area for r in regions]
    mean_intensities = [r.mean_intensity for r in regions]
    blot_labels = [label_mapping[r.label] for r in regions]
    blob_labels = [r.label for r in regions]

    rows = grid_coordinates[:, 0]
    cols = grid_coordinates[:, 1]

    coords = np.array([r.centroid for r in regions])
    y_coords = coords[:, 0]
    x_coords = coords[:, 1]

    data = {
        'blot_label': blot_labels,
        'blob_label': blob_labels,
        'row': rows,
        'col': cols,
        'x': x_coords,
        'y': y_coords,
        'mean_intensity': mean_intensities,
        'area': areas,
    }

    blob_df = pd.DataFrame(data)

    return blob_df


def find_spots(im: np.ndarray) -> Tuple[List, np.ndarray]:
    BLOCK_SIZE = 101
    CLOSING_SIZE = 3
    EROSION_SIZE = 7

    CIRC_THRESH = 0.3

    # Binarize image
    filtered = median(im, square(7))
    thresh = threshold_local(filtered, block_size=BLOCK_SIZE)
    bw = closing(filtered > thresh, square(CLOSING_SIZE))
    eroded_bw = erosion(bw, selem=disk(EROSION_SIZE))

    # Make the label_image
    cleared = clear_border(eroded_bw)
    label_image = label(cleared)
    regions = regionprops(label_image=label_image, intensity_image=im)

    # Filter regions
    size_filtered = [r for r in regions if r.area > 100]
    circularity = [_calc_circularity(r) for r in size_filtered]
    circularity_filtered = [r for c, r in zip(circularity, size_filtered) if c > CIRC_THRESH]

    # Remove filtered labels from label image
    good_labels = [r.label for r in circularity_filtered]

    unique_labels = np.unique(label_image)
    in_good_labels = np.isin(unique_labels, good_labels)
    labels_to_remove = unique_labels[np.logical_not(in_good_labels)]

    for l in labels_to_remove:
        label_image[label_image == l] = 0

    return circularity_filtered, label_image


def get_intensities(im_path: str, blot_config_path: str) -> BlotData:

    im = _load_image(im_path)
    regions, label_im = find_spots(im)
    blot_config = BlotConfig(config=blot_config_path)

    label_mapping, grid_coords = _find_label_mapping(regions, blot_config)

    blob_df = _make_blob_df(regions, label_mapping, grid_coords)

    blob_data = BlotData(
        blob_df,
        label_im=label_im,
        blot_config=blot_config,
        im_path=im_path,
        label_mapping=label_mapping,
        grid_coords=grid_coords
    )

    return blob_data


def get_intensities_from_mask(im_path: str, blot_data: BlotData) -> BlotData:

    im = _load_image(im_path)
    label_im = blot_data.label_im
    regions = regionprops(label_im, intensity_image=im)
    df = _make_blob_df(regions, blot_data.label_mapping, blot_data.grid_coords)

    new_blot_data = BlotData(
        blob_df=df,
        label_im=label_im,
        blot_config=blot_data.blot_config,
        im_path=im_path,
        label_mapping=blot_data.label_mapping,
        grid_coords=blot_data.grid_coords,
        mask_source=blot_data.im_path
    )

    return new_blot_data

