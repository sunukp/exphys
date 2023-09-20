
import sys
import os
import time
import glob
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

sys.path.append(os.path.abspath('..'))
import src.utils.garmin_utils as garmin_utils
from src.utils.matfcns import *

win_size = int(sys.argv[1])
input_dir = '../data/garmin/raw'
input_files = [
    '11775496032_ACTIVITY.csv', 
    'garmin-connect-3452356474__1692836018.csv', 
    'garmin-connect-3452356474__1692985475.csv', 
    'garmin-connect-3452356474__1693067992.csv', 
    '12030209819_ACTIVITY.csv'
    ]
# input_files = ['12030209819_ACTIVITY.csv']
output_dir = '../data/garmin/processed'
output_file = 'raw'

for k in range(len(input_files)):
    output_file = f'{output_dir}/eda__raw_all_winsize_{win_size}.csv'
    # output_file = f'{output_dir}/eda__{input_files[k]}.csv' # XXX
    print(f'{input_files[k]}...')

    df = pd.read_csv(input_dir + '/' + input_files[k])
    df = df.replace('None', np.nan) # heart_rate has this

    df['heart_rate'] = pd.to_numeric(df['heart_rate'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index(df['timestamp'], inplace=True)
    df = df.drop_duplicates(subset=['timestamp'], ignore_index=True)
    df = df.drop(['fractional_cadence'], axis=1)
    df = df.dropna(subset=['power'])
  

    ##################################################################
    # 5 movmean
    df['power'] = movmean(df['power'], win_size)
    df['enhanced_altitude'] = movmean(df['enhanced_altitude'], win_size)
    df['enhanced_speed'] = movmean(df['enhanced_speed'], win_size)
    df['cadence'] = movmean(df['cadence'], win_size)
    df['distance'] = movmean(df['distance'], win_size)

    # XXX new:
    df['heart_rate'] = movmean(df['heart_rate'], win_size) 
    df['temperature'] = movmean(df['temperature'], win_size)

    ##################################################################
    # 6 derivatives
    for col in ['timestamp', 'enhanced_altitude', 'enhanced_speed', 'cadence', 'distance']:
        dcol = 'd_' + col
        df[dcol] = df[col].diff()

    df = df[df['d_timestamp'] == timedelta(seconds=1)]

    ##################################################################
    # 7 grade
    df['grade'] = gradePrcnt(df['d_enhanced_altitude'].values, df['d_distance'].values)
    print(f'Printing to...{output_file}')
    if k == 0:
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, mode='a', index=False, header=False)

