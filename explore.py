import pandas as pd
import json

# Allow all 8 columns to be displayed instead of the middle columns being abbreviated to '...'.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Pull in the raw data from 'raw_data.json'
with open('raw_data.json', 'r') as f:
    all_features = json.load(f)

# Divide the features into their statistical_id codes: max - 00001, min - 00002, mean - 00003.
max_features = [f for f in all_features if f['properties']['statistic_id'] == '00001']
min_features = [f for f in all_features if f['properties']['statistic_id'] == '00002']
mean_features = [f for f in all_features if f['properties']['statistic_id'] == '00003']

# Set up and organize the DataFrame for the scope of mean - 00003.
rows = [f['properties'] for f in mean_features]
df = pd.DataFrame(rows)
mean_df = df[['monitoring_location_id', 'statistic_id', 
         'parameter_code', 'time', 'value', 
         'unit_of_measure', 'approval_status', 'qualifier']]

# Cast time and value as datetime and numeric.
mean_df['time'] = pd.to_datetime(mean_df['time'], errors='coerce')
mean_df['value'] = pd.to_numeric(mean_df['value'], errors='coerce')

# Separate mean_df into dataframe per parameter code
m_dis = mean_df[mean_df['parameter_code'] == '00060']
m_gau = mean_df[mean_df['parameter_code'] == '00065']
m_temp = mean_df[mean_df['parameter_code'] == '00010']

# Setting up the date spine for finding gaps in the data
dis_dates = pd.date_range(start=m_dis['time'].min(), end=m_dis['time'].max(), freq='D')
gau_dates = pd.date_range(start=m_gau['time'].min(), end=m_gau['time'].max(), freq='D')
temp_dates = pd.date_range(start=m_temp['time'].min(), end=m_temp['time'].max(), freq='D')


miss_date_gau = set(gau_dates) - set(m_gau['time'])
miss_date_temp = set(temp_dates) - set(m_temp['time'])

years = pd.to_datetime(list(miss_date_gau)).year
print(years.value_counts())
