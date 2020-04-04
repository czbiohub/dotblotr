from os import path

import pandas as pd

from .find_spots import get_intensities, get_intensities_from_mask
from .io import open_rgb

MERGE_ON = 'dot_name'
MERGE_COLS = [MERGE_ON, 'mean_intensity']


def quantify_blot_array(
        im_path: str,
        strip_id: str,
        array_config_path: str,
        assay_config_path: str
):
    assay_config = pd.read_csv(assay_config_path)
    control_image, probe_image = open_rgb(im_path)
    control_blot = get_intensities(im=control_image, blot_config_path=array_config_path)
    probe_blot = get_intensities_from_mask(im=probe_image, blot_data=control_blot)

    assay_results = _compare_to_control(
        control_blot=control_blot,
        probe_blot=probe_blot,
        assay_config=assay_config
    )

    assay_id = path.split(assay_config_path)[-1]
    assay_results.insert(loc=0, column='assay_id', value=assay_id)

    assay_results.insert(loc=1, column='strip_id', value=strip_id)

    return assay_results


def _compare_to_control(control_blot, probe_blot, assay_config):

    # new control column names
    control_df = control_blot.df
    probe_df = probe_blot.df[MERGE_COLS]

    # add the source plate info and drop any rows for wells not present in assay
    control_df = pd.merge(assay_config, control_df, on=MERGE_ON, how='outer', suffixes=('', ''))
    control_df = control_df.dropna(axis=0)

    # calculate the normalized intensity
    assay_df = pd.merge(control_df, probe_df, on=MERGE_ON, how='outer', suffixes=('_control', '_probe'))
    assay_df['norm_probe_intensity'] = assay_df['mean_intensity_probe'] / assay_df['mean_intensity_control']

    # calculate the positive hit thresholds
    neg_ctrls = assay_df.loc[assay_df['exp_group'] == 'neg']
    neg_mean = neg_ctrls.norm_probe_intensity.mean()
    neg_std = neg_ctrls.norm_probe_intensity.std()
    assay_df['positive_threshold'] = neg_mean + assay_df['zscore_threshold'] * neg_std

    # identify the positive hits
    assay_df['pos_hit'] = assay_df['norm_probe_intensity'] > assay_df['positive_threshold']

    return assay_df
