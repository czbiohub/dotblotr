import json
from typing import Union, Dict


class BlotConfig:

    def __init__(self, config: Union[Dict, str]):
        if isinstance(config, str):
            with open(config, "r") as read_file:
                self.config = json.load(read_file)
        else:
            self.config = config

    @property
    def n_cols(self)->int:
        return self.config['n_cols']

    @n_cols.setter
    def n_cols(self, n_cols):
        self.config['n_cols'] = n_cols

    @property
    def n_rows(self)->int:
        return self.config['n_rows']

    @n_rows.setter
    def n_rows(self, n_rows:int):
        self.config['n_rows'] = n_cols

    def get_col_label(self, col_index:int)->str:

        col_label = self.config['col_labels'][col_index]

        return col_label

    def get_row_label(self, row_index:int)->str:

        col_label = self.config['row_labels'][row_index]

        return col_label
