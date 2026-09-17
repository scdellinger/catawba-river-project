import pandas as pd
import json

# Allow all 8 columns to be displayed instead of the middle columns being abbreviated to '...'.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Pull in the raw data from 'raw_data.json'
with open('raw_data.json', 'r') as f:
    all_features = json.load(f)

# Set up and organize the DataFrame, ensure coordinates are preserved when flattening the data.
rows = []
for f in all_features:
    row = dict(f['properties'])
    lon, lat = f['geometry']['coordinates']
    row['longitude'] = lon
    row['latitude'] = lat
    row['feature_id'] = f['id']
    rows.append(row)

df = pd.DataFrame(rows)

'''
   - Convert 'time' to datetime type, 'value' to numeric type.
   - 'qualifier' is object type. If not NaN, the value is list type. Looking at list and length of each list, there is 
      only one item in each list in this initial data pull. assert added to flag if there is ever a list with more than 
      one element.
'''
assert (df['qualifier'].dropna().apply(len) <= 1).all(), "qualifier column has a row with more than one value — unwrap logic assumes single-element lists"
df['qualifier'] = df['qualifier'].apply(lambda x: x[0] if isinstance(x, list) else x)
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['time'] = pd.to_datetime(df['time'], errors='coerce')

df.to_parquet('data/long_format.parquet', index=False)