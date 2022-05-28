#!/usr/bin/env python
# coding: utf-8

from BLPlot import CuratedOverview as CO
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    #PTData = pd.read_csv("outputs/dyn-BF/dyn-BF-AUROCscores.csv", header = 0, index_col = 0)
    AUPRC = pd.read_csv("outputs/DREAM4/DREAM4-AUPRC.csv", header = 0, index_col = 0)
    AUPRC.reset_index()
    print(AUPRC)
    CO.plot(AUPRC, 
            randValues=[1,1],
            shape='text',
            palettes=sns.color_palette(), 
            text='Y',
            levels=[['AUPRC Ratio'],['mCAD', 'VSC']],
            rotation=['vertical','vertical'])
