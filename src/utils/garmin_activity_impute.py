from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def get_first_last_na_idx(sers):
    '''
    Function to return the first and last indices of nan values in the Series sers.
    The returned indices are designed to be used to interpolate missing values in between.
    As such, the # of first indices and last indices should always match.
    Also sers starting with a nan doesn't get counted, nor does one ending with a nan
    (again, because we want to interpolate)
    '''
    isna_loc = np.argwhere(sers.isna()).ravel()
    sers_val = sers.values

    first_na_locs = []
    last_na_locs = []

    for k in isna_loc:
        if k >= 1:
            if not np.isnan(sers_val[k-1]):
                first_na_locs.append(k)
            if k < sers.shape[0]-1:
                if not np.isnan(sers_val[k+1]) and len(first_na_locs) > 0:
                    last_na_locs.append(k)


    if np.isnan(sers_val[-1]):
        first_na_locs = first_na_locs[:-1]

    return first_na_locs, last_na_locs


def interpolate_vals(df, col, first_na_locs, last_na_locs, tol_secs=10):
    '''
    Call as df[col] = interpolate_vals(df, col, ...)
    '''
    sers_val = df[col].values

    for k in range(len(first_na_locs)):
        
        tdelta = df.loc[last_na_locs[k], 'timestamp'] - df.loc[first_na_locs[k], 'timestamp']

        if tdelta <= timedelta(seconds=tol_secs-1):
            nobs = last_na_locs[k] - first_na_locs[k] + 1
            val_prev = sers_val[first_na_locs[k]-1]
            val_next = sers_val[last_na_locs[k]+1]

            rang = np.linspace(val_prev, val_next, nobs+2)
            rang = rang[1:-1]

            col_idx = df.columns.get_loc(col)
            for i, j in enumerate(range(first_na_locs[k], last_na_locs[k]+1)):
                df.iloc[j, col_idx] = rang[i]

    # return df[col]