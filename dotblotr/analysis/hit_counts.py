from typing import List, Union

import pandas as pd


SPOT_DATA_COLS = [
    'dot_name',
    'assay_id',
    'source_plate_id',
    'source_plate_row',
    'source_plate_column',
    'exp_group',
    'row',
    'col'
]

def calc_hit_counts(results_table:pd.DataFrame, aux_columns:Union[None, List[str]] = None):
    assays = results_table.assay_id.unique()

    hit_dfs = []
    for assay in assays:
        # get the positive results for the assay
        assay_results = results_table.loc[results_table['assay_id'] == assay]
        pos_hits = assay_results.loc[assay_results['pos_hit']]
        hit_counts = pos_hits['dot_name'].value_counts()
        hit_counts_df = pd.DataFrame({'dot_name': hit_counts.index.values, 'n_hits': hit_counts.values})

        # add the dots with 0 hits
        neg_dots = assay_results.loc[assay_results['pos_hit'] == False]
        no_hit_dot_names = neg_dots[~neg_dots.dot_name.isin(pos_hits.dot_name)]['dot_name'].unique()
        neg_dots_df = pd.DataFrame({'dot_name': no_hit_dot_names, 'n_hits': 0})
        hit_counts_df = pd.concat([hit_counts_df, neg_dots_df], ignore_index=True)

        # get data about the positive spots
        if aux_columns is not None:
            cols_to_transfer = SPOT_DATA_COLS + aux_columns
        else:
            cols_to_transfer = SPOT_DATA_COLS
        hit_spot_data = assay_results[cols_to_transfer].drop_duplicates()

        result = hit_spot_data.join(hit_counts_df.set_index('dot_name'), on='dot_name')
        hit_dfs.append(result)

        return hit_dfs
