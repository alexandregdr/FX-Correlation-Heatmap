#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 08:10:50 2025

@author: alexandregindre
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

eurusd=pd.read_csv("/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/EUR_USD Historical Data.csv")
usdjpy=pd.read_csv("/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/USD_JPY Historical Data.csv")
audusd=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/AUD_USD Historical Data.csv')
gbpusd=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/GBP_USD Historical Data.csv')
usdcad=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/USD_CAD Historical Data.csv')
usdchf=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/USD_CHF Historical Data.csv')
usdcny=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/USD_CNY Historical Data.csv')
usdhkd=pd.read_csv('/Users/alexandregindre/Downloads/Projet FX Correl - Python/DATA/USD_HKD Historical Data.csv')


def clean_fx_df(df):
    df = df.copy()
    
    # Suppression colonnes inutiles
    df = df.drop(columns=["Vol.", "Change %"], errors="ignore")
    
    # Conversion Date
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Conversion Price en float -> gestion des virgules
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    
    # Trier par date croissante
    df = df.sort_values("Date")
    
    df = df.reset_index(drop=True)
    
    return df

# Recalcul des returns pour pouvoir calculer les correls
def compute_returns(df):
    df = df.copy()
    df["Return_pct"] = df["Price"].pct_change() * 100
    return df


fx_dfs = {
    "EURUSD": eurusd,
    "USDJPY": usdjpy,
    "AUDUSD": audusd,
    "GBPUSD": gbpusd,
    "USDCAD": usdcad,
    "USDCHF": usdchf,
    "USDCNY": usdcny,
    "USDHKD": usdhkd
}


for pair in fx_dfs:
    fx_dfs[pair] = clean_fx_df(fx_dfs[pair])
    fx_dfs[pair] = compute_returns(fx_dfs[pair])


returns_df = None

for pair, df in fx_dfs.items():
    temp = df[["Date", "Return_pct"]].rename(
        columns={"Return_pct": pair}
    )
    
    if returns_df is None:
        returns_df = temp
    else:
        returns_df = pd.merge(
            returns_df,
            temp,
            on="Date",
            how="inner"
        )


returns_df = returns_df.dropna()
returns_df = returns_df.set_index("Date")


corr_matrix = returns_df.corr()


plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f",
)

plt.title("FX Daily Returns Correlation Heatmap")
plt.tight_layout()
plt.show()

