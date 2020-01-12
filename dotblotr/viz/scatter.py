from typing import List, Union

from matplotlib import pyplot as plt
import pandas as pd


def plot_counts(hit_table:pd.DataFrame, sort_by:Union[str, List[str]]='n_hits'):
    hit_table.sort_values(by=sort_by, axis=0, inplace=True)




