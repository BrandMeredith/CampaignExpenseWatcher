import pandas as pd

def read_data():
    df = pd.read_csv("~/Documents/Insight/Data - Insight/oppexp20/oppexp.csv", low_memory=False)
    cmte_header = pd.read_csv("~/Documents/Insight/Data - Insight/cm20/cm_header_file.csv") # pull in header for committee names file
    cmte_names = pd.read_csv("~/Documents/Insight/Data - Insight/cm20/cm.txt", delimiter="|", names=cmte_header.columns) # pull in committee names file
    return df, cmte_names

def clean_data(df, cmte_names):
    # Add committee names to the dataframe
    return ( df.set_index('CMTE_ID') ).join(cmte_names.set_index('CMTE_ID'))