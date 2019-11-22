from typing import Dict, Union

import numpy as np
import pandas as pd

from dotblotr import BlotConfig


class BlotData:
    def __init__(
            self, blob_df: pd.DataFrame, label_im: np.ndarray,
            blot_config: BlotConfig, im_path: str, label_mapping: Dict,
            grid_coords: np.ndarray, mask_source: Union[None, str]=None
    ):
        self.df = blob_df
        self.label_im = label_im
        self.blot_config = blot_config
        self.im_path = im_path
        self.label_mapping = label_mapping
        self.grid_coords = grid_coords
        self.mask_source = mask_source
