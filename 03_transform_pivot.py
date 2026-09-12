import pandas as pd

# Read in parquets
discharge = pd.read_parquet('data/discharge_clean.parquet')
gauge = pd.read_parquet('data/gauge_clean.parquet')
temp = pd.read_parquet('data/temperature_clean.parquet')

# Merge parameter DataFrames and rename columns
wide_df = discharge.merge(gauge, on='time', how='outer').merge(temp, on='time', how='outer')
wide_df = wide_df.rename(columns={
        'time': 'date',
        'value_x': 'discharge_value',
        'unit_of_measure_x': 'discharge_units',
        'qualifier_x': 'discharge_qualifier',
        'value_y': 'gauge_value',
        'unit_of_measure_y': 'gauge_units',
        'qualifier_y': 'gauge_qualifier',
        'value': 'temp_value',
        'unit_of_measure': 'temp_units',
        'qualifier': 'temp_qualifier',
        'temperature_is_outlier': 'temp_is_outlier'
        }   
)
wide_df = wide_df[['date', 
                   'discharge_value', 'discharge_units', 'discharge_qualifier', 'discharge_is_outlier', 
                   'gauge_value', 'gauge_units', 'gauge_qualifier', 'gauge_is_outlier', 
                   'temp_value', 'temp_units', 'temp_qualifier', 'temp_is_outlier'
]]

   # file transformation. parquet for exploratory work, csv for tableau
wide_df.to_parquet('data/wide_df_clean.parquet')
wide_df.to_csv('data/catawba_wide.csv', index=False)
