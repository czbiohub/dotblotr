from typing import List, Union

from matplotlib.colors import Normalize
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def plot_hit_grid(
        hit_table: pd.DataFrame, results_table: pd.DataFrame,
        sort_by:Union[str, List[str]] = 'n_hits', x_label: str = 'dot_name',
        cmap:str = 'inferno',
):
    """ Plot the hits

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
    cmap : str
        Name of the colormap to be used for the number of hits.
        The default value is 'inferno'
        See the matplotlib documation for details:
        https://matplotlib.org/3.1.1/tutorials/colors/colormaps.html
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
                #names.append(dot_row[x_label])
                names.append(dot_row['dot_name'])
                strip_id_indices.append(dot_row['strip_id'])
                counts.append(count)

    f, ax = plt.subplots(figsize=(50, 2))
    sc = ax.scatter(names, strip_id_indices, c=counts, cmap=cmap);

    ax.tick_params(axis='x', labelsize=5, rotation=90)
    ax.set_xlabel('spot name')
    ax.set_ylabel('strip id')

    plt.draw()

    norm = Normalize(vmin=1, vmax=hit_table['n_hits'].max())
    # for t in ax.get_xticklabels():
    #     tick_name = t.get_text()
    #     dot_name = results_table.loc[results_table[x_label] == tick_name].dot_name.values[0]
    #     n_hits = hit_table.loc[hit_table['dot_name'] == dot_name].n_hits.values[0]
    #     c = sc.cmap(norm(n_hits))
    #     t.set_color(c)
    label_names = []
    for t in ax.get_xticklabels():
        dot_name = t.get_text()
        label_names.append(dot_name)
        n_hits = hit_table.loc[hit_table['dot_name'] == dot_name].n_hits.values[0]
        c = sc.cmap(norm(n_hits))
        t.set_color(c)

    new_labels = [
        results_table.loc[results_table['dot_name'] == n][x_label].values[0] for n in label_names
    ]
    ax.set_xticklabels(new_labels)
    plt.draw()

    return f, ax


def plot_cplot(
        results_table: pd.DataFrame,
        vertical_var:str = 'top_hit',
        vert_sort_order:str = 'descending',
        horizontal_var:str = 'strip_id',
        color_var:str = 'top_hit_pct',
        cmap:str = 'inferno',
        cbar_label:str = 'Purity'
):
    """ Plot the consolidated hits

    Parameters:
    ------------
    results_table : pd.DataFrame
        The results table output from process_dir() from which to get the strip info
    vertical_var : str
        The column name in results_table to use for the vertical axis variable
        The default value is 'top_hit'
    vert_sort_order : str
        The order the vertical axis should be sorted by.
        Can be 'ascending' (lowest value by the horizontal axis)
        or 'descending' (highest value by the horizontal axis.
        The default value is 'descending'.
    horizontal_var : str
        The column name in results_table to use for the horizontal axis varible.
        The default value is 'strip_id'
    color_var : str
        The column name in results_table to use to color to points.
        The default value is 'top_hit_pct'
    cmap : str
        The name of the colormap for coloring the points. The default value is 'inferno'.
        See: https://matplotlib.org/3.1.1/tutorials/colors/colormaps.html
    cbar_label : str
        The value for the colorbar label. The default value is 'Purity'

    Returns:
    --------
    f
        matplotlib figure object
    ax
        matplotlib axis object
    """
    # Get a list of unique genes in the results_table
    unique_vertical_var = results_table[vertical_var].unique()

    # sort the vertical variable by the number of instances
    n_vert_var = [
        len(
            np.unique(
                results_table.loc[
                    (results_table[vertical_var] == v) & results_table['pos_hit']
                ][horizontal_var]
            )
        )
        for v in unique_vertical_var
    ]

    # optionally put the highest values closest to the horizontal axis
    if vert_sort_order == 'descending':
        vert_var_order = np.argsort(n_vert_var)[::-1]
    unique_vertical_var = unique_vertical_var[vert_var_order]

    # Get a list of the unique h_vars
    unique_horizontal_variable = results_table[horizontal_var].unique()

    # make an empty lists for the plot values for the dotplot
    h_vars = []
    v_vars = []
    n_hits = []
    color_property = []

    for h in unique_horizontal_variable:
        for v in unique_vertical_var:
            # Get the rows where the strip_id and top_hit match the strip_id and
            strip_gene_df = results_table[(results_table[horizontal_var] == h) & (results_table[vertical_var] == v)]

            # If there are any matches, add the values to plot
            if len(strip_gene_df) > 0:
                # add the gene/strip pair to the coords
                h_vars.append(h)
                v_vars.append(v)

                # each row of the df is a hit, so the number of rows is the number of hits
                pos_rows = strip_gene_df.loc[strip_gene_df.pos_hit]
                n_hits.append(len(pos_rows))

                # I wasn't sure how you wanted to calculate the color_property,
                # so I took the mean of the hits for the gene/strip pair
                color_property.append(strip_gene_df[color_var].mean())

    # make the figure and axes
    f, ax = plt.subplots(figsize=(10, 15))

    # make the scatter plot (https://matplotlib.org/3.1.3/api/_as_gen/matplotlib.pyplot.scatter.html)
    # x = h_vars
    # y = gene names
    # s: set the size by the number of hits
    # c: set the color by the color_property
    # cmap: use the 'magma' colormap (https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html)
    s_plot = ax.scatter(x=h_vars, y=v_vars, s=n_hits, c=color_property, cmap=cmap)

    # rotate the xticks 90 degress
    plt.xticks(rotation=90);

    # add the colorbar
    cbar = plt.colorbar(s_plot)
    cbar.set_label(cbar_label, rotation=270, labelpad=20, fontsize=16)

    # add the sizes legend
    plt.legend(
        *s_plot.legend_elements("sizes", num=4),
        bbox_to_anchor=(0., 1.02, 1., .102),
        loc='lower left',
        ncol=5,
        mode="expand",
        borderaxespad=0.);

    return f, ax
