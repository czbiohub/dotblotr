from typing import Dict, Union

import numpy as np
import pandas as pd

from dotblotr import BlotConfig


class BlotData:
    def __init__(
            self, blob_df: pd.DataFrame, label_im: np.ndarray,
            blot_config: BlotConfig, raw_im: np.ndarray, label_mapping: Dict,
            grid_coords: np.ndarray, mask_raw_im: Union[None, np.ndarray]=None
    ):
        self.df = blob_df
        self.label_im = label_im
        self.blot_config = blot_config
        self.raw_im = raw_im
        self.label_mapping = label_mapping
        self.grid_coords = grid_coords
        self.mask_raw_im = mask_raw_im
