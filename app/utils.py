import pandas as pd
import numpy as np
import streamlit as st # <-- FIXED: Imported Streamlit for the caching decorator

# Define the file paths and required metrics
# IMPORTANT: These paths are relative to the location where Streamlit is run (the parent folder)
BENIN_FILE = 'data/benin_clean.csv'
SL_FILE = 'data/sierraleone_clean.csv'
TOGO_FILE = 'data/togo_clean.csv'
IRRADIANCE_METRICS = ['GHI', 'DNI', 'DHI']

@st.cache_data
def load_and_combine_data():
    """Loads cleaned data from all countries and combines them into one DataFrame."""
    try:
        benin_df = pd.read_csv(BENIN_FILE)
        sl_df = pd.read_csv(SL_FILE)
        togo_df = pd.read_csv(TOGO_FILE)
        
        benin_df['Country'] = 'Benin'
        sl_df['Country'] = 'Sierra Leone'
        togo_df['Country'] = 'Togo'

        combined_df = pd.concat([benin_df, sl_df, togo_df], ignore_index=True)
        return combined_df

    except Exception as e:
        # Note: Streamlit will show this error on the page if data loading fails
        print(f"Error loading data for Streamlit: {e}")
        return None

def create_summary_table(df):
    """Generates the Summary Table (Mean, Median, Std Dev) for displayed countries."""
    
    # Define the aggregation functions
    agg_funcs = ['mean', 'median', 'std']
    
    # Calculate Mean, Median, and Std Dev using pandas groupby
    summary_table = df.groupby('Country')[IRRADIANCE_METRICS].agg(agg_funcs)
    
    # Simple Column Flattening and Renaming
    new_columns = []
    for metric in IRRADIANCE_METRICS:
        for func in agg_funcs:
            new_columns.append(f'{metric} {func.capitalize()}') 
            
    summary_table.columns = new_columns
    
    # Calculate Coefficient of Variation (CV) for GHI
    summary_table['GHI CV (%)'] = (summary_table['GHI Std'] / summary_table['GHI Mean']) * 100
    
    return summary_table.round(2)
