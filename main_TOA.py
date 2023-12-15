# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from Tool.ppfd_toa_csv import ppfd_toa_csv

# %%
# 日付をまとめたcsvファイルから大気上端PPFD (TOA PPFD)を求めるコード
ppfd_toa_csv(
    date_csv_path   = './sample/toa_date.csv',  # 求めたい日付をまとめたcsvファイルのパス
    lat             = 35.639525095721694 ,      # 求めたい地点の緯度
    lon             = 139.37906584098394 ,      # 求めたい地点の経度
    out_csv_path    = './output/TOA_out.csv'    # 出力csvファイルのパス
)
