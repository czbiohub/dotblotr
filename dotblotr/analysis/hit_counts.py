import pandas as pd


SPOT_DATA_COLS = [
    'blot_label',
    'assay_id',
    'source_plate_id',
    'source_plate_row',
    'source_plate_column',
    'exp_group',
    'row',
    'col'
]

def calc_hit_counts(results_table):
    assays = results_table.assay_id.unique()

    pos_hit_dfs = []
    for assay in assays:
        # get the positive results for the assay
        assay_results = results_table.loc[results_table['assay_id'] == assay]
        pos_hits = assay_results.loc[assay_results['pos_hit']]
        hit_counts = pos_hits['blot_label'].value_counts()
        hit_counts_df = pd.DataFrame({'blot_label': hit_counts.index.values, 'n_hits': hit_counts.values})

        # get data about the positive spots
        hit_spot_data = pos_hits[SPOT_DATA_COLS].drop_duplicates()

        result = hit_spot_data.join(hit_counts_df.set_index('blot_label'), on='blot_label')
        pos_hit_dfs.append(result)

        return pos_hit_dfs
