#!/usr/bin/enb python3
# -*- coding: utf-8 -*-
# Zenith.py: 天頂角を検討するためのコード
# %%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import cv2
from tqdm import tqdm
import warnings;warnings.simplefilter('ignore')

# %%

def Sky_Stem_Leaf(WSI_path=None, Stem_path=None, out_csv_path='./output_ssl.csv', WSI_threshold=100, circle_dir_path='./circle', plot=False, dpi=400):
    """マスキング済み全天画像から各開空度における、空・幹・葉の割合を求める

    Args:
        WSI_path (path, str): 全天カメラ画像のパス (元画像・二値化画像のどちらでも可)
        Stem_path (path, str):  マスキング済み3バンド画像のパス (背景を白で作成すること)
        out_csv_path (path, str):出力csvファイルパス Defaults to './output_ssl.csv'.
        WSI_threshold (float): 全天画像の閾値 Defaults to 100. 'binary'と入力すると，全天画像に二値化画像を登録できる．
        circle_dir_path (str, optional): 各開空度の見本画像 (背景を白で作成すること). Defaults to './circle'.
        plot(bool): 画像を出力するかどうか
        dpi (int): 画像解像度 (400くらいが妥当)

    Returns:
        Pandas.DataFrame: 各開空度における空隙率
    """

    wsi_img  = cv2.imread(WSI_path )  # 全天画像
    wsi_img  = np.nanmean(wsi_img, axis=2) if wsi_img.ndim==3 else wsi_img
    
    stem_img = cv2.imread(Stem_path)  # 幹のマスキング画像
    stem_img = np.nanmean(stem_img, axis=2)

    out_df = pd.DataFrame()
    for angle in tqdm(range(10, 180+1, 10)):
        circle_img  = np.nanmean(cv2.imread(f'{circle_dir_path}/{angle}.jpg'), axis=2)
        circle_area = np.nansum(np.where(circle_img!=255, 1, np.nan))

        stem_target_img = np.where(
            (circle_img!=255)&(stem_img!=255),
            1, np.nan
        )
        if WSI_threshold=='binary':
            wsi_target_img = np.where(
                (circle_area!=255) & (wsi_img==255),
                1, np.nan
            )
        else:
            wsi_target_img = np.where(
                (circle_img!=255)&(wsi_img>=WSI_threshold),
                1, np.nan
            )
        out_df.loc[angle, 'sky']  = np.nansum(wsi_target_img) / circle_area
        out_df.loc[angle, 'stem'] = np.nansum(stem_target_img) / circle_area
    out_df['leaf'] = 1 - (out_df['stem'] + out_df['sky'])
    out_df.index.name = 'Zenith'
    out_df.to_csv(out_csv_path)

    if plot:

        # 二値化済み全天画像の表示 (右は閾値によるマスキング表示あり)
        bin_circlie_img = np.where(circle_img!=255, wsi_img, np.nan)
        fig, ax = plt.subplots(1,2, figsize=(12, 6), dpi=dpi)
        image = ax[0].imshow(bin_circlie_img, cmap='rainbow', vmin=0, vmax=255, interpolation='nearest')
        cbar = fig.colorbar(image, orientation='horizontal')
        cbar.set_ticks(range(0, 255, 25))
        ax[0].set_title('check masking circle')

        image = ax[1].imshow(bin_circlie_img, cmap='gray', vmin=0, vmax=255)
        ax[1].imshow(wsi_target_img, cmap='Reds', vmin=0, vmax=1.25, interpolation='nearest')
        ax[1].set_title(f'WSI image (threshold={WSI_threshold})')
        cbar = fig.colorbar(image, orientation='horizontal')


        # 二値化済み全天画像のヒストグラム
        plt.figure(figsize=(8,3))
        plt.hist(bin_circlie_img.flatten(), range=(0, 255), bins=256)
        plt.xlabel('DN')
        plt.ylabel('cnt')
        plt.grid()
        plt.title('WSI image histogram')
        fig.show()

        # 天頂角別の各要素の割合
        plt.figure(figsize=(8, 3))
        plt.plot(out_df, marker='o', markersize=4, label=out_df.columns)
        plt.grid()
        plt.xticks(range(0, 181, 10))
        plt.xlabel('Zenith [deg]')
        plt.ylabel('rate', loc='top')
        plt.legend()
        plt.title(f'Zenith dynamics (threshold={WSI_threshold})')
        plt.ylim(0, 1)
        plt.show()


    return out_df

if __name__=='__main__':
    df= Sky_Stem_Leaf(
        WSI_path  = '../DSC_0008.jpg',  # 全天画像のパス (二値化前でもあとでもOK)
        Stem_path = '../stem.jpg',     # 幹をマスキングした画像 (背景を白にして、それ以外の色で塗りつぶすこと)
        WSI_threshold = 100,             # 全天画像の閾値 (空とそれ以外)
        out_csv_path = '../天頂角別3要素.csv',  # 出力ファイル名
        circle_dir_path='../circle/',     # 開空度の参考にする画像フォルダのパス
        plot=True                       # 各種確認用画像を出力する
        )

