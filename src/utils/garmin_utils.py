
import fitdecode as fitd
import datetime
import numpy as np

ACTIVITY_FEATURE_NAMES = ['timestamp',
    'position_lat',
    'position_long',
    'distance',
    'enhanced_speed',
    'enhanced_altitude',
    'power',
    'heart_rate',
    'cadence',
    'temperature',
    'fractional_cadence']


def garlatlon2deg(lat_or_lon):
    '''
    Garmin lat/lon conversion
    '''
    return lat_or_lon/((2**32)/360)


def read_fit_acvitity(fit_fn):
    '''
    Reads *_ACTIVITY.fit files, parses 'record' frames into a list and returns it.

    Args:
        fit_fn: the full path of the '*_ACTIVITY.fit' file to parse.
    Returns:
        a list of comma-separated values.
    '''
    csv_lines = []

    with fitd.FitReader(fit_fn) as fit:
        for frame in fit:
            if frame.frame_type == fitd.FIT_FRAME_DATAMESG:
                
                if frame.name == 'record':
                    row = []

                    obj = frame.get_value('timestamp', fallback='')
                    if isinstance(obj, datetime.datetime):
                        row.append(obj.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        row.append('')
                    
                    obj = frame.get_value('position_lat', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('position_long', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    row.append(str(frame.get_value('distance', fallback='')))
                    row.append(str(frame.get_value('enhanced_speed', fallback='')))
                    row.append(str(frame.get_value('enhanced_altitude', fallback='')))
                    row.append(str(frame.get_value('power', fallback='')))
                    
                    obj = frame.get_value('heart_rate', fallback='')
                    if obj is None:
                        row.append('NaN')
                    else:
                        row.append(str(obj))

                    row.append(str(frame.get_value('cadence', fallback='')))
                    row.append(str(frame.get_value('temperature', fallback='')))
                    row.append(str(frame.get_value('fractional_cadence', fallback='')))

                    csv_lines.append(','.join(row))
    return csv_lines
