import pandas as pd
import numpy as np
import glob
import streamlit as st

def load_and_process_data():
    """
    Ingests raw CSVs, cleans them, aggregates to District level,
    and performs Feature Engineering for the AI models.
    """
    def load_stream(pattern):
        # Recursive search for files
        files = glob.glob(f"**/*{pattern}*.csv", recursive=True)
        df_list = []
        for f in files:
            try:
                temp = pd.read_csv(f)
                # Cleaning: Standardize headers
                temp.columns = [c.lower().strip() for c in temp.columns]
                
                # Select numeric cols + grouping keys
                num_cols = temp.select_dtypes(include=[np.number]).columns.tolist()
                if 'pincode' in num_cols: num_cols.remove('pincode')
                
                # Aggregation: Pincode -> District
                grp = temp.groupby(['date', 'state', 'district'])[num_cols].sum().reset_index()
                df_list.append(grp)
            except:
                pass
        return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

    with st.spinner('Ingesting Data Streams...'):
        df_enrol = load_stream('enrolment')
        df_bio = load_stream('biometric')
        df_demo = load_stream('demographic')

    # Mapping columns to standard names
    col_map = {
        'age_0_5': 'enrol_newborn', 'age_18_greater': 'enrol_adult',
        'bio_age_5_17': 'bio_update_child', 'bio_age_17_': 'bio_update_adult',
        'demo_age_17_': 'demo_update_adult'
    }
    for df in [df_enrol, df_bio, df_demo]:
        df.rename(columns=col_map, inplace=True)

    # Data Fusion (Merging Streams)
    keys = ['date', 'state', 'district']
    df_master = pd.merge(df_enrol, df_bio, on=keys, how='outer')
    df_master = pd.merge(df_master, df_demo, on=keys, how='outer').fillna(0)
    
    # Date Parsing
    df_master['date'] = pd.to_datetime(df_master['date'], dayfirst=True, errors='coerce')

    # Feature Engineering (The "Secret Sauce")
    df_master['total_vol'] = (df_master['enrol_newborn'] + df_master['bio_update_child'] + df_master['demo_update_adult'])
    # Migration Score: Ratio of Adult Address Changes to Total Activity
    df_master['migration_score'] = df_master['demo_update_adult'] / (df_master['total_vol'] + 1)

    return df_master