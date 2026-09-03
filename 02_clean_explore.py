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

# Separate mean_df into dataframe per parameter code.
m_dis = mean_df[mean_df['parameter_code'] == '00060']
m_gau = mean_df[mean_df['parameter_code'] == '00065']
m_temp = mean_df[mean_df['parameter_code'] == '00010']

# Setting up the date spine for finding gaps in the data
dis_dates = pd.date_range(start=m_dis['time'].min(), end=m_dis['time'].max(), freq='D')
gau_dates = pd.date_range(start=m_gau['time'].min(), end=m_gau['time'].max(), freq='D')
temp_dates = pd.date_range(start=m_temp['time'].min(), end=m_temp['time'].max(), freq='D')

# Creating a list of missing dates for each parameter, and some combinations.
miss_date_dis = set(dis_dates) - set(m_dis['time'])
miss_date_gau = set(gau_dates) - set(m_gau['time'])
miss_date_temp = set(temp_dates) - set(m_temp['time'])
gau_without_temp = miss_date_gau - miss_date_temp

# Discharge stats (Leptokurtic: kurtosis = 724)
q1 = 115
q3 = 279
iqr = q3 -q1
lower_fence = q1 - (1.5 * iqr)
upper_fence = q3 + (1.5*iqr)
high_upper = q3 + (3 * iqr)
normal_discharge = m_dis[ m_dis['value'] <= upper_fence]
outlier_discharge = m_dis[m_dis['value'] > upper_fence]
med_high_discharge = m_dis[(m_dis['value'] > upper_fence) & (m_dis['value'] <= high_upper)]
high_high_discharge = m_dis[m_dis['value'] > high_upper]

# Gauge stats (Leptokurtic: kurtosis = ~ 46.59)
q1 = 1.59
q3 = 2.2
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)
high_upper = q3 + (iqr * 3)
normal_gauge = m_gau[m_gau['value'] <= upper_fence]
outlier_gauge = m_gau[m_gau['value'] > upper_fence]
med_high_gauge = m_gau[(m_gau['value'] > upper_fence) & (m_gau['value'] <= high_upper)]
high_high_gauge = m_gau[m_gau['value'] > high_upper]

# Temp stats (platykurtic: kurtosis = -1.14)
q1 = 9.2
q3 = 20.125
iqr = q3 - q1
lower_fence = q1 - (iqr*1.5)
upper_fence = q3 + (1.5*iqr)

# Discharge value-outlier/qualifier-estimated overlap
df = m_dis[(m_dis['value'] > 525) & (m_dis['qualifier'].notna())]
df = df.sort_values(by='time')


# Outlier boolean columns added
m_dis['discharge_is_outlier'] = m_dis[(m_dis['value'] < -131) & (m_dis['value'] >= 525)]
m_gau['gauge_is_outlier'] = m_gau[(m_gau['value'] < 0.675) & (m_gau['value'] >= 3.115)]
m_temp['temperature_is_outlier'] = m_temp[(m_temp['value'] < -7.1875) & (m_temp['value'] >= 36.5125)]

discharge = m_dis
gauge = m_gau
temperature = m_temp