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
    """大気上端PPFDを計算する関数

    Args:
        date_csv_path (str, path): 求める日時が記入されたcsvファイルのパス. 列に(date, time)か(datetime)が含まれる必要がある.
        lat (float): 求める地点の緯度. Defaults to 35.639525095721694.
        lon (float): 求める地点の経度. Defaults to 139.37906584098394.
        out_csv_path (str, path): 出力csvファイルのパス. Defaults to './TOA_out.csv'.

    Returns:
        pd.DataFrame: 結果データフレーム 
    """


    date_df = pd.read_csv(date_csv_path, index_col=None)
    if 'datetime' in date_df.columns:
        date_time = pd.to_datetime((date_df['datetime']))
        out_csv = pd.DataFrame({
            'datetime': date_df['datetime'].values,
            'PPFD_toa': DaylightOutsideTheAtmosphere(date_time, lat, lon, mode='ppfd'),
        })
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
    val = ppfd_toa_csv('..//sample/toa_date.csv')
    print(val)

# %%
