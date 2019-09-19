import pandas as pd
import numpy as np
from scipy import stats

def my_model(cmte_name  = 'Default'):
    # Read in data
    df = pd.read_csv("~/Documents/Insight/Data - Insight/oppexp20/oppexp.csv", low_memory=False)
    cmte_header = pd.read_csv(
        "~/Documents/Insight/Data - Insight/cm20/cm_header_file.csv")  # pull in header for committee names file
    cmte_names = pd.read_csv("~/Documents/Insight/Data - Insight/cm20/cm.txt", delimiter="|",
                             names=cmte_header.columns)  # pull in committee names file

    # Clean data
    df = (df.set_index('CMTE_ID')).join(cmte_names.set_index('CMTE_ID'))

    # Get committee id from committee name
    #cmte_name = #"GILLIBRAND 2020" #INPUT
    cmte_data = cmte_names[cmte_names['CMTE_NM'] == cmte_name].copy()
    cmte_id = cmte_data['CMTE_ID'].values[0]

    # Committee-level data
    cmte = df[df.index == cmte_id].copy()
    pos_cmte = cmte[cmte['TRANSACTION_AMT'] > 0]
    gpd_pos_cmte = pos_cmte.groupby('PURPOSE')
    cats_paid = gpd_pos_cmte['TRANSACTION_AMT'].sum().sort_values(ascending=False)
    top_cats = cats_paid.index[:3]

    # Detect outliers
    outliers = pd.DataFrame()
    for cat in top_cats:
        cmte_cat = cmte[cmte['PURPOSE'] == cat].copy()
        outliers = outliers.append(cmte_cat[np.abs(stats.zscore(cmte_cat['TRANSACTION_AMT'])) > 3])

    return outliers