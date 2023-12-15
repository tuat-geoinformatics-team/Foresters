# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from Tool import Sky_Stem_Leaf
import cv2

# %%
# 「全天画像」と「幹のマスキング画像」から写真内に占める 空・幹・葉 の割合を求めるコード
df= Sky_Stem_Leaf(
        WSI_path  = './img/DSC_0599.tif',    # 全天画像のパス (二値化前でもあとでもOK)
        Stem_path = './img/stem.jpg',        # 幹をマスキングした画像 (背景を白にして、それ以外の色で塗りつぶすこと)
        WSI_threshold = 'binary',            # 全天画像の閾値 (空とそれ以外, DNで指定) 'binary'とすると，全天画像(WSI_path)に二値化画像を登録できる．
        out_csv_path = './output/天頂角別3要素.csv',  # 出力ファイル名
        circle_dir_path='.//circle//',       # 開空度の参考にする画像フォルダのパス
        plot=True,                           # 各グラフを出力する
        dpi=400                              # 出力全天画像の解像度 (フリーズするなら400くらいにした方がいい)
    )

