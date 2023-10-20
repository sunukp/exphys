import sys
import os
import time
import glob
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

sys.path.append(os.path.abspath('..'))
import src.utils.garmin_utils as garmin_utils
from src.utils.matfcns import *
from src.utils.garmin_activity_impute import *


def read_config_file(config_file):
    vars = {}
    is_file_list = False
    file_list = []

    with open(config_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            if not is_file_list:
                name, val = line.partition('=')[::2]
                vars[name.strip()] = val.strip()
                if 'input_files' == name.strip():
                    is_file_list = True
            else:
                file_list.append(line.strip())
        
        vars['input_files'] = file_list

    return vars


if __name__ == '__main__':
    config = read_config_file(sys.argv[1])
    input_dir = config['input_dir']
    input_files = config['input_files']
    output_dir = config['output_dir']
    output_file = config['output_file']
    win_size = int(config['win_size'])
    tol_secs = int(config['time_tolerance'])

    
    output_file = f'{output_dir}/{output_file}' # XXX

    for k in range(len(input_files)):
        print(f'{input_files[k]}...')

        df = pd.read_csv(input_dir + '/' + input_files[k])
        df = df.replace('None', np.nan) # heart_rate has this

        df['heart_rate'] = pd.to_numeric(df['heart_rate'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.drop_duplicates(subset=['timestamp'], ignore_index=True)
        df = df.drop(['fractional_cadence'], axis=1)
        df = df.dropna(subset=['power'])

        ##################################################################
        # new: impute
        df = df.reset_index(drop=True)
        
        # cadence
        df.loc[np.logical_and(df['power'] == 0, df['cadence'].isna()), 'cadence'] = 0
        first_na_locs, last_na_locs = get_first_last_na_idx(df['cadence'])
        if len(first_na_locs)>0:
            df['cadence'] = interpolate_vals(df, 'cadence', first_na_locs, last_na_locs, tol_secs=tol_secs)
    
        # position_lat/long
        first_na_locs, last_na_locs = get_first_last_na_idx(df['position_lat'])
        df['position_lat'] = interpolate_vals(df, 'position_lat', first_na_locs, last_na_locs, tol_secs=tol_secs)
        df['position_long'] = interpolate_vals(df, 'position_long', first_na_locs, last_na_locs, tol_secs=tol_secs)

        # distance
        first_na_locs, last_na_locs = get_first_last_na_idx(df['distance'])
        df['distance'] = interpolate_vals(df, 'distance', first_na_locs, last_na_locs, tol_secs=tol_secs)
        del_locs = np.array(last_na_locs)+1
        df = df.drop(del_locs) # delete row after null distances as that row will see distance jumped
        df = df.reset_index(drop=True)

        # enhanced_speed
        mask = np.logical_and(np.isnan(df['enhanced_speed']), df['cadence'] == 0)
        df.loc[mask, 'enhanced_speed'] = 0
        first_na_locs, last_na_locs = get_first_last_na_idx(df['enhanced_speed'])
        df['enhanced_speed'] = interpolate_vals(df, 'enhanced_speed', first_na_locs, last_na_locs, tol_secs=tol_secs)

        # enhanced_altitude
        first_na_locs, last_na_locs = get_first_last_na_idx(df['enhanced_altitude'])
        df['enhanced_altitude'] = interpolate_vals(df, 'enhanced_altitude', first_na_locs, last_na_locs, tol_secs=tol_secs)

        # heart_rate
        first_na_locs, last_na_locs = get_first_last_na_idx(df['heart_rate'])
        df['heart_rate'] = interpolate_vals(df, 'heart_rate', first_na_locs, last_na_locs, tol_secs=tol_secs)

        # temperature
        first_na_locs, last_na_locs = get_first_last_na_idx(df['temperature'])
        df['temperature'] = interpolate_vals(df, 'temperature', first_na_locs, last_na_locs, tol_secs=tol_secs)

        # drop all remaining na:
        df = df.dropna()
        df = df.reset_index(drop=True)


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
        df = df.drop(['d_timestamp'], axis=1)

        ##################################################################
        # 7 grade
        df['grade'] = gradePrcnt(df['d_enhanced_altitude'].values, df['d_distance'].values)

        if k == 0:
            df.to_csv(output_file, index=False)
        else:
            df.to_csv(output_file, mode='a', index=False, header=False)

    print(f'Printed to...{output_file}')
