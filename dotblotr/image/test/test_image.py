import os

import numpy as np
import pandas as pd

from dotblotr.image import quantify_blot_array


def test_quantify_blot():
    dir_name = os.path.dirname(os.path.realpath(__file__))
    im_path = os.path.join(dir_name, 'simulated_strip.tif')
    blot_config_path = os.path.join(dir_name, '384_tiny_config.json')
    assay_config_path = os.path.join(dir_name, 'assay_config.csv')

    assay_results = quantify_blot_array(
        im_path=im_path,
        strip_id='test_blot',
        array_config_path=blot_config_path,
        assay_config_path=assay_config_path
    )
    exp_res_path = os.path.join(dir_name, 'expected_results_table.csv')
    results_table = pd.read_csv(exp_res_path)
    np.all(results_table['norm_probe_intensity'] == assay_results['norm_probe_intensity'])
