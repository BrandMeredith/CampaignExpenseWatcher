import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
from sklearn.cluster import DBSCAN

PRES_CMTES = ['BENNET FOR AMERICA','BIDEN FOR PRESIDENT','BULLOCK FOR PRESIDENT','PETE FOR AMERICA, INC.','KAMALA HARRIS FOR THE PEOPLE','AMY KLOBUCHAR VICTORY COMMITTEE','WAYNE MESSAM FOR AMERICA, INC.','TIM RYAN FOR AMERICA','WARREN FOR PRESIDENT, INC.','MARIANNE WILLIAMSON FOR PRESIDENT','FRIENDS OF ANDREW YANG','CORY 2020','JULIAN FOR THE FUTURE','FRIENDS OF JOHN DELANEY','TULSI NOW','BETO FOR AMERICA','BERNIE 2020','JOE SESTAK FOR PRESIDENT','TOM STEYER 2020']
CORE_COLUMNS = ['CMTE_NM','RPT_TP','NAME','CITY','STATE','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','PURPOSE','CATEGORY']


def dbscan_model():
    # Read in data
    df_header = pd.read_csv("./static/data/oppexp_header_file.csv")
    df = pd.read_csv("./static/data/oppexp.txt", delimiter="|", low_memory=False, names=df_header.columns, index_col=False)
    cmte_header = pd.read_csv("./static/data/cm_header_file.csv") # pull in header for committee names file
    cmte_names = pd.read_csv("./static/data/cm.txt", delimiter="|", names=cmte_header.columns) # pull in committee names file

    # Clean data
    df = ( df.set_index('CMTE_ID') ).join(cmte_names.set_index('CMTE_ID'))
    df = df.reset_index()
    df['TRANSACTION_DT']=pd.to_datetime(df['TRANSACTION_DT'],errors = 'coerce')
    df = df[df['TRANSACTION_AMT']>0]
    df = df[df.apply(lambda x: x.CMTE_NM in PRES_CMTES, axis=1)]

    # Find Outliers
    clustering = DBSCAN(eps=30, min_samples=100).fit_predict(df[['TRANSACTION_AMT']])
    outliers = df[clustering==-1]
    outliers = outliers.sort_values('TRANSACTION_DT',ascending=False)

    # Save the outliers in a csv
    outliers.to_csv('./flaskexample/static/data/AWS_outliers2020.csv')

def choose_campaign(cmte_nm):
    outliers = pd.read_csv("./flaskexample/static/data/outliers2020.csv", index_col=0)
    # Restrict to one campaign
    return outliers.loc[outliers['CMTE_NM']==cmte_nm,CORE_COLUMNS]
