import glob
from typing import List
from os import path

from dotblotr.image import quantify_blot_array
import pandas as pd


def process_im_list(
        im_paths: List[str],
        strip_ids: List[str],
        blot_config_path: str,
        assay_config_path: str
) -> pd.DataFrame:
    assay_results = []

    # Run through each blot
    for im_path, strip_id in zip(im_paths, strip_ids):
        result = quantify_blot_array(
            im_path=im_path,
            strip_id=strip_id,
            array_config_path=blot_config_path,
            assay_config_path=assay_config_path
        )

        assay_results.append(result)

    results_table = pd.concat(assay_results, axis=0, ignore_index=True)

    return results_table


def process_dir(
        dir_path:str,
        blot_config_path:str,
        assay_config_path:str,
        filename_pattern: str = '*.tif'
) -> pd.DataFrame:

    img_pattern = path.join(dir_path, filename_pattern)
    im_paths = glob.glob(img_pattern)

    strip_ids = [im.split('/')[-1].split('.')[0] for im in im_paths]
    results_table = process_im_list(im_paths, strip_ids, blot_config_path, assay_config_path)

    return results_table
