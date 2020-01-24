from typing import List, Union

from matplotlib.colors import Normalize
from matplotlib import pyplot as plt
import pandas as pd


def plot_hit_grid(
        hit_table: pd.DataFrame, results_table: pd.DataFrame,
        sort_by:Union[str, List[str]]='n_hits', x_label: str ='dot_name'
):
    """
    Plot the hits

    Parameters:
    ------------
    hit_table : pd.DataFrame
        the hit table output from calc_hit_counts().
        Note that `calc_hit_counts()` returns an list of hit tables,
        so index to the hit table you wish to plot.
    results_table : pd.DataFrame
        the results table output from process_dir() from which to get the strip info
    sort_by : list[str]
        a list of hit_table columns to sort the dots (x axis) by.
        ['n_hits', 'dot_name'] sorts by number of hits and then the dot name
    x_label : str
        the results table column to use for the name of the dot on the x_label
        (e.g., dot_name for the name of the dot)
    """

    hit_table.sort_values(by=sort_by, axis=0, inplace=True, ascending=False)

    unique_strip_ids = results_table.strip_id.unique()
    strip_ids = {strip_id: i for i, strip_id in enumerate(unique_strip_ids)}

    names = []
    strip_id_indices = []
    counts = []

    for i, row in hit_table.iterrows():
        name = row['dot_name']
        count = row['n_hits']
        dot_table = results_table.loc[results_table['dot_name'] == name]

        for j, dot_row in dot_table.iterrows():
            if dot_row['pos_hit']:
                names.append(dot_row[x_label])
                strip_id_indices.append(dot_row['strip_id'])
                counts.append(count)

    f, ax = plt.subplots(figsize=(50, 2))
    sc = ax.scatter(names, strip_id_indices, c=counts, cmap='hsv');

    ax.tick_params(axis='x', labelsize=5, rotation=90)
    ax.set_xlabel('spot name')
    ax.set_ylabel('strip id')

    plt.draw()

    norm = Normalize(vmin=1, vmax=5)
    for t in ax.get_xticklabels():
        tick_name = t.get_text()
        dot_name = results_table.loc[results_table[x_label] == tick_name].dot_name.values[0]
        n_hits = hit_table.loc[hit_table['dot_name'] == dot_name].n_hits.values[0]
        c = sc.cmap(norm(n_hits))
        t.set_color(c)

    plt.draw()

    return f, ax


