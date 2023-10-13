
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

LAP_FEATURE_NAMES = [
    'timestamp',
    'start_time',
    'start_position_lat',
    'end_position_lat',
    'start_position_long',
    'end_position_long',
    'total_calories',
    'total_strokes',
    'total_work',
    'avg_speed',
    'max_speed',
    'avg_power',
    'max_power',
    'normalized_power',
    'avg_heart_rate',
    'max_heart_rate',
    'avg_cadence',
    'max_cadence',
    'total_ascent',
    'total_descent',
    'avg_vam',
    'lap_trigger',
    'sport',
    'sub_sport'
]

SESSION_FEATURE_NAMES = [
    'timestamp',
    'start_time',
    'start_position_lat',
    'end_position_lat',
    'start_position_long',
    'end_position_long',
    'num_laps',
    'training_stress_score',
    'intensity_factor',
    'total_training_effect',
    'total_anaerobic_training_effect',
    'total_calories',
    'total_strokes',
    'total_work',
    'avg_speed',
    'max_speed',
    'avg_power',
    'max_power',
    'normalized_power',
    'avg_heart_rate',
    'max_heart_rate',
    'avg_cadence',
    'max_cadence',
    'total_ascent',
    'total_descent',
    'avg_vam',
    'sport',
    'sub_sport'
]

def garlatlon2deg(lat_or_lon):
    '''
    Garmin lat/lon conversion
    '''
    return lat_or_lon/((2**32)/360)


def gartimestamp2datetime(gar_ts):
    '''
    Garmin timestamp conversion.
    Returns the local datetime
    '''
    return datetime.datetime.fromtimestamp(gar_ts + fitd.processors.FIT_UTC_REFERENCE)


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


def read_fit_lap(fit_fn):
    csv_lines = []

    with fitd.FitReader(fit_fn) as fit:
        for frame in fit:
            if frame.frame_type == fitd.FIT_FRAME_DATAMESG:
                
                if frame.name == 'lap':
                    row = []

                    obj = frame.get_value('timestamp', fallback='')
                    if isinstance(obj, datetime.datetime):
                        row.append(obj.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        row.append('')

                    obj = frame.get_value('start_time', fallback='')
                    if isinstance(obj, datetime.datetime):
                        row.append(obj.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        row.append('')
                    
                    obj = frame.get_value('start_position_lat', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('end_position_lat', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('start_position_long', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('end_position_long', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    row.append(str(frame.get_value('total_calories', fallback='')))
                    row.append(str(frame.get_value('total_strokes', fallback='')))
                    row.append(str(frame.get_value('total_work', fallback='')))
                    row.append(str(frame.get_value('avg_speed', fallback='')))
                    row.append(str(frame.get_value('max_speed', fallback='')))
                    row.append(str(frame.get_value('avg_power', fallback='')))
                    row.append(str(frame.get_value('max_power', fallback='')))
                    row.append(str(frame.get_value('normalized_power', fallback='')))
                    row.append(str(frame.get_value('avg_heart_rate', fallback='')))
                    row.append(str(frame.get_value('max_heart_rate', fallback='')))
                    row.append(str(frame.get_value('avg_cadence', fallback='')))
                    row.append(str(frame.get_value('max_cadence', fallback='')))
                    row.append(str(frame.get_value('total_ascent', fallback='')))
                    row.append(str(frame.get_value('total_descent', fallback='')))
                    row.append(str(frame.get_value('avg_vam', fallback='')))
                    row.append(str(frame.get_value('lap_trigger', fallback='')))
                    row.append(str(frame.get_value('sport', fallback='')))
                    row.append(str(frame.get_value('sub_sport', fallback='')))

                    csv_lines.append(','.join(row))
    return csv_lines



def read_fit_session(fit_fn):
    csv_lines = []

    with fitd.FitReader(fit_fn) as fit:
        for frame in fit:
            if frame.frame_type == fitd.FIT_FRAME_DATAMESG:
                
                if frame.name == 'session':
                    row = []

                    obj = frame.get_value('timestamp', fallback='')
                    if isinstance(obj, datetime.datetime):
                        row.append(obj.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        row.append('')
                    
                    obj = frame.get_value('start_time', fallback='')
                    if isinstance(obj, datetime.datetime):
                        row.append(obj.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        row.append('')

                    obj = frame.get_value('start_position_lat', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('end_position_lat', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('start_position_long', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    obj = frame.get_value('end_position_long', fallback='')
                    try:
                        row.append(str(garlatlon2deg(obj)))
                    except:
                        row.append('NaN') # otherwise we get 'None'

                    row.append(str(frame.get_value('num_laps', fallback='')))
                    row.append(str(frame.get_value('training_stress_score', fallback='')))
                    row.append(str(frame.get_value('intensity_factor', fallback='')))
                    row.append(str(frame.get_value('total_training_effect', fallback='')))
                    row.append(str(frame.get_value('total_anaerobic_training_effect', fallback='')))

                    row.append(str(frame.get_value('total_calories', fallback='')))
                    row.append(str(frame.get_value('total_strokes', fallback='')))
                    row.append(str(frame.get_value('total_work', fallback='')))
                    row.append(str(frame.get_value('avg_speed', fallback='')))
                    row.append(str(frame.get_value('max_speed', fallback='')))
                    row.append(str(frame.get_value('avg_power', fallback='')))
                    row.append(str(frame.get_value('max_power', fallback='')))
                    row.append(str(frame.get_value('normalized_power', fallback='')))
                    row.append(str(frame.get_value('avg_heart_rate', fallback='')))
                    row.append(str(frame.get_value('max_heart_rate', fallback='')))
                    row.append(str(frame.get_value('avg_cadence', fallback='')))
                    row.append(str(frame.get_value('max_cadence', fallback='')))
                    row.append(str(frame.get_value('total_ascent', fallback='')))
                    row.append(str(frame.get_value('total_descent', fallback='')))
                    row.append(str(frame.get_value('avg_vam', fallback='')))
                    row.append(str(frame.get_value('sport', fallback='')))
                    row.append(str(frame.get_value('sub_sport', fallback='')))

                    csv_lines.append(','.join(row))
    return csv_lines
