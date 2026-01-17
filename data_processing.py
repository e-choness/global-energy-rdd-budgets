import pandas as pd
import streamlit as st

DATA_PATH = "data/Energy-Technology-RD&D-Budgets-Filtered.csv"

@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    # prefer uppercase TIME_PERIOD and OBS_VALUE which hold values
    if 'TIME_PERIOD' in df.columns:
        df['Year'] = pd.to_numeric(
            df['TIME_PERIOD'], errors='coerce').astype(pd.Int64Dtype())
    elif 'Time Period' in df.columns:
        df['Year'] = pd.to_numeric(
            df['Time Period'], errors='coerce').astype(pd.Int64Dtype())
    else:
        df['Year'] = pd.NA

    if 'OBS_VALUE' in df.columns:
        df['Value'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
    elif 'Observation value' in df.columns:
        df['Value'] = pd.to_numeric(df['Observation value'], errors='coerce')
    else:
        df['Value'] = pd.NA

    # friendly names
    if 'Country/Region' in df.columns:
        df['Country'] = df['Country/Region']
    elif 'COUNTRY' in df.columns:
        df['Country'] = df['COUNTRY']

    if 'Technology' in df.columns:
        df['Technology'] = df['Technology']
    elif 'RDD_TECH' in df.columns:
        df['Technology'] = df['RDD_TECH']

    if 'Sector' in df.columns:
        df['Sector'] = df['Sector']

    # drop rows missing values
    df = df.dropna(subset=['Year', 'Value', 'Country'])

    return df