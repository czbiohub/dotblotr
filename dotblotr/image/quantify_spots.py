import pandas as pd

from .find_spots import get_intensities, get_intensities_from_mask


MERGE_ON = 'blot_label'
MERGE_COLS = [MERGE_ON, 'mean_intensity']


def quantify_blot_array(
        control_image: str,
        probe_image: str,
        array_config_path: str,
        assay_config_path: str
):
    control_blot = get_intensities(im_path=control_image, blot_config_path=array_config_path)
    probe_blot = get_intensities_from_mask(im_path=probe_image, blot_data=control_blot)

    assay_results = _compare_to_control(control_blot=control_blot, probe_blot=probe_blot)

    return assay_results


def _compare_to_control(control_blot, probe_blot):

    # new control column names
    control_df = control_blot.df
    probe_df = probe_blot.df[MERGE_COLS]

    assay_df = pd.merge(control_df, probe_df, on=MERGE_ON, how='outer', suffixes=('_control', '_probe'))

    return assay_df
