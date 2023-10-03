"""Utilities for solution of the optimization task."""
from datetime import datetime, time
import fnmatch
import math
import os

import pandas as pd


def get_prices(req_date, data_dir='data/', zone='N.Y.C.', resolution=0.5,
               exp_date_format='%Y%m%d', date_col='Time Stamp',
               zone_col='Name', cost_col='LBMP'):
    """The function identifies appropriate file with cost-relevant data, loads
    it, filters appropriate zone and resamples the data to required resolution

    Parameters
    ----------
    req_date : datetime
        date of required costs
    data_dir : str
        path to dir with NYISO data sets
    zone : str
        name of the NYISO zone of interest
    resolution : float
        resolution of the required sampling in hours
    exp_date_format : str
        date format that is expected to appear as substring in the file name
    date_col : str
        name of the date column in the data file
    zone_col : str
        name of the column with zones in the data file
    cost_col : name of the column with costs/LBMP in the file

    Returns
    -------
    pd.Series
        pandas series with corresponding cost data, indexed on datetime and
        sampled in the required frequency

    Raises
    ------
    Exception
        If there is no dataset corresponding to the req_date.
        If identifiers for zone_col and cost_col are not correct or unique.
        If zone identifier does not produce any results.
    TypeError
        If req_date is not datetime.
    ValueError
        If provided resolution is > 1 or < original dataset resolution.
    """
    if resolution > 1:
        raise ValueError('Argument resolution should be <= 1.')
    if not isinstance(req_date, datetime):
        raise TypeError('Argument req_date should be datetime.')
    file = None
    str_date = req_date.strftime(exp_date_format)
    for i in os.scandir(data_dir):
        if fnmatch.fnmatch(i, '*{}*'.format(str_date)):
            file = i
            break
    if file is None:
        raise Exception('No data for {} in {}.'.format(req_date, data_dir))
    price_df = pd.read_csv('{}/{}'.format(data_dir, file.name),
                           index_col=date_col, parse_dates=[date_col]
                           ).filter(regex='{}|{}'.format(zone_col, cost_col))
    n_cols = len(price_df.columns)
    if n_cols != 2:
        raise Exception('Expected 2 columns corresponding to zone_col and cost'
                        'col, got {}.'.format(n_cols))
    price_ser = price_df.loc[price_df[zone_col] == zone].filter(regex=cost_col
                                                                ).iloc[:, 0]
    n_rows = len(price_ser)
    if n_rows == 0:
        raise Exception('No data found for zone {}.'.format(zone))
    price_ser = price_ser.resample('{}H'.format(resolution), closed='right',
                                   label='right').mean()
    nan_rows = price_ser.isnull().sum()
    if nan_rows > 0:
        raise ValueError('Provided resolution {} is lower than resolution of'
                         'original dataset.'.format(resolution))
    return price_ser


def sample_to_time(time_sample, resolution, label='right'):
    """Translates the sample number to HH:MM:SS time for given resolution

    Parameters
    ----------
    time_sample : int
        time sample to be translated to time
    resolution : float
        resolution of the model in hours
    label : str
        whether label should correspond to right or left side of the bin

    Returns
    -------
    datetime.time
        time corresponding to the provided label

    Raises
    ------
    ValueError
        If the label name is incorrect.
    """
    if label == 'right':
        label_const = 1
    elif label == 'left':
        label_const = 0
    else:
        raise ValueError('Label should be either right or left.')
    hours_in_day, mins_in_hour = 24, 60
    hours_right = (time_sample + label_const) * resolution
    hh = math.floor(hours_right) % hours_in_day
    mm = int(hours_right % 1 * mins_in_hour)
    return time(hh, mm)
