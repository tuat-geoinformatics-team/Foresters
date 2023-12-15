# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

if __name__=='__main__':
    from Radiation import DaylightOutsideTheAtmosphere
else:
    from .Radiation import DaylightOutsideTheAtmosphere

# %%
def ppfd_toa_csv(date_csv_path, lat=35.639525095721694, lon=139.37906584098394, out_csv_path='./TOA_out.csv'):
    """
    Args:
        date_csv_path (_type_): _description_
        lat (float, optional): _description_. Defaults to 139.38.
        lon (float, optional): _description_. Defaults to 35.64.
    """


    date_df = pd.read_csv(date_csv_path, index_col=None)
    if 'datetime' in date_df.columns:
        date_time = pd.to_datetime((date_df['datetime']))
    elif ('date' in date_df.columns) & ('time' in date_df.columns):
        date_time = pd.to_datetime((date_df['date'] +' ' + date_df['time']).values)
    out_csv = pd.DataFrame({
        'date': date_df['date'].values,
        'time': date_df['time'].values,
        'PPFD_toa': DaylightOutsideTheAtmosphere(date_time, lat, lon, mode='ppfd'),
    })
    out_csv.to_csv(out_csv_path, index=None)

    return out_csv


# %%
if __name__ == '__main__':
    val = ppfd_toa_csv('../toa_date.csv')
    print(val)
