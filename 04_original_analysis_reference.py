import pandas as pd
import matplotlib.pyplot as plt

# Allow all columns to be displayed instead of the middle columns being abbreviated to '...'.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# -------------------------------|
# Yearly discharge investigation |
# -------------------------------|
""" Look at the data through a year by year lense, finding any outliers and any additional insights. """

   # Bring in the discharge parquet and tailor the dataset for yearly analysis. Grain of dataframe is one row equals one unique year.
df = pd.read_parquet('data/discharge_clean.parquet')
df = df.rename(columns={'time': 'date'})[['date', 'value']]  # Renamed 'time' column to 'date'. The data deals with the mean, so this should have addressed in the cleaning phase
df['year'] = df['date'].dt.to_period('Y')   # Create a 'year' column to work by year.
df = df[df['date'] > '1987-12-31']   # Cut off 1987 since only 50 days of that year are included.
yearly_discharge = df.groupby('year')['value'].sum().reset_index(name='value')   # Aggregate over year
yearly_discharge = yearly_discharge.sort_values(by='year')   # Sort results by year

   # Look at .kurt() and .describe()
# print(yearly_discharge['value'].kurt())   
# print(yearly_discharge['value'].describe())

q1 = 71409.05
q3 = 114062.65
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)
l_tightened_fence = q1 - (iqr * 1)
u_tightened_fence = q3 + (iqr * 1)

   # Find outlier years
outliers = yearly_discharge[yearly_discharge['value'] > u_tightened_fence]   # Produces two high outlier years with a tightened fence

# --------------------------------|
# Monthly discharge investigation |
# --------------------------------|
""" Look at the data through a month by month lense, looking for monthly outliers and the years they fall into"""


   # Bring in the discharge parquet and tailor for monthly investigation. Grain of dataframe is one row equals one unique month.
df = pd.read_parquet('data/discharge_clean.parquet')
df = df.rename(columns={'time': 'date'})[['date', 'value']]   #  Change 'time' column header to 'date'
df['year_month'] = df['date'].dt.to_period('M')   # Add a 'year_month' column to aggregate over.
df = df[df['year_month'] > '1987-11']   # Exclude November 1987 since it is a partial year. 
monthly_discharge = df.groupby('year_month')['value'].sum().reset_index(name='value')   # Aggregate over year.
monthly_discharge = monthly_discharge.sort_values(by='value', ascending=False)   # Sort by unique months
#print(monthly_discharge.head(10))

   # Look at .kurt() and .describe()
#print(monthly_discharge['value'].kurt())
#print(monthly_discharge['value'].describe())

q1 = 4084.25
q3 = 9669.25
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)
high_upper = q3 + (iqr * 3)

   # Finding year_month of medium and high outliers, also see count by year.
med_outliers = df[(df['value'] >= upper_fence) & (df['value'] < high_upper)]
hi_outliers = df[df['value'] >= high_upper]
med_outliers['year'] = med_outliers['year_month'].dt.year   # Add a year column to see if years hold multiple outliers
hi_outliers['year'] = hi_outliers['year_month'].dt.year   # Add a year column to see if years hold multiple outliers

   # Looking at month of the year data for any additional insights
by_month = df
by_month['month'] = df['date'].dt.month
by_month = by_month.groupby('month')['value'].sum().reset_index(name='value')

   # Look at .kurt() and .describe()
#print(by_month['value'].kurt())
#print(by_month['value'].describe())
q1 = 244715.15
q3 = 333523.65
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)

   # Look at non hurricane months to see if the statistics change.
hurricane_months = pd.PeriodIndex(['2004-09', '2018-05', '2018-10', '2024-09'], freq=('M'))   # List of months with confirmed hurricane remnant activity
non_hurricane = df[~df['year_month'].isin(hurricane_months)]  
non_hurricane = non_hurricane.groupby('year_month')['value'].sum().reset_index(name='value')

   # .kurt() and .describe() 
#print(non_hurricane['value'].kurt())
#print(non_hurricane.describe())

   # look at the highest day from each month compared to the months total. How much of the month's mean is concentrated in one day?
concentration = df.groupby('year_month')['value'].max() / df.groupby('year_month')['value'].sum()
#print(concentration.sort_values(ascending=False).head(10))

   # Compare hurricane season (June 01 - November 30) to months outside of hurricane season, and how many are in each.
monthly_discharge['month'] = monthly_discharge['year_month'].dt.month
hurricane_months = [6, 7, 8, 9, 10, 11]
hurricane_season = monthly_discharge[monthly_discharge['month'].isin(hurricane_months)]
not_hurricane_season = monthly_discharge[~monthly_discharge['month'].isin(hurricane_months)]

   # compare the number of months in and out of hurricane season and how many outliers are in each
#print(len(hurricane_season))
#print(len(not_hurricane_season))
#print(len(hurricane_season[hurricane_season['value'] > 18046.75]))
#print(len(not_hurricane_season[not_hurricane_season['value'] > 18046.75]))


# ------------------------------|
# Daily Discharge Investigation |
# ------------------------------|

   # Look at daily discharge and see any trends
daily_discharge = pd.read_parquet('data/discharge_clean.parquet')
daily_discharge = daily_discharge.rename(columns={'time': 'date'})[['date', 'value']]

   # Add columns for different sorting uses
daily_discharge['year_month'] = daily_discharge['date'].dt.to_period('M')
daily_discharge['year'] = daily_discharge['date'].dt.year
daily_discharge['month'] = daily_discharge['date'].dt.month
hurricane_months = [6, 7, 8, 9, 10, 11]

   # compare number of days in and out of hurricane season and how many outliers are in each
hurricane_season = daily_discharge[daily_discharge['month'].isin(hurricane_months)]
not_hurricane_season = daily_discharge[~daily_discharge['month'].isin(hurricane_months)]
#print(daily_discharge.sort_values(by='value', ascending=False).head(50))

   # .kurt() and .describe()
#print(daily_discharge['value'].kurt())
#print(daily_discharge['value'].describe())      

print(len(hurricane_season[hurricane_season['value'] >= 525]))
print(len(not_hurricane_season[not_hurricane_season['value'] >= 525]))


#-----------------------------|
# Yearly Gauge Investigation  |
#-----------------------------|

df = pd.read_parquet('data/gauge_clean.parquet')
df = df.rename(columns={'time': 'date'})[['date', 'value', 'gauge_is_outlier']]

   # Add year, year_month, month columns for deeper analysis
df['year'] = df['date'].dt.year
df['year_month'] = df['date'].dt.to_period('M')
df['month'] = df['date'].dt.month
#print(df.head(10))

   # .kurt() and .describe()
#print(df['value'].kurt())
#print(df['value'].describe())

q1 = 1.59
q3 = 2.2
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)
extreme_fence = q3 + (iqr * 3)

#print('Outliers below lower fence:', len(df[df['value'] <= lower_fence]))
#print('1st quartile:', len(df[df['value'] < 1.59]))
#print('2nd quartile:', len(df[(df['value'] >= 1.59) & (df['value'] < 1.88)]))
#print('3rd quartile:', len(df[(df['value'] >= 1.88) & (df['value'] < 2.2)]))
#print('4th quartile:', len(df[df['value'] >= 2.2]))
#print('Outliers above 75% and below upper fence:', len(df[(df['value'] >= 2.2) & (df['value'] < upper_fence)]))
#print('Outliers above upper fence and below extreme fence:', len(df[(df['value'] >= upper_fence) & (df['value'] < extreme_fence)]))
#print('Outliers above extreme fence:', len(df[df['value'] >= extreme_fence]))

   # Find what percentage of gauge readings are at different levels of outliers
med_outlier_perc = (247 / 8780) * 100
extreme_outlier_perc = (151 / 8780) * 100
#print(f"Medium outlier percentage of total gauge readings: {med_outlier_perc:.2f}%")
#print(f"Extreme outlier percentage of total gauge readings: {extreme_outlier_perc:.2f}%")

   # Create gauge outlier dataframe
gauge_outliers = df[df['gauge_is_outlier'] == True]
#print(gauge_outliers.head(10))

   # Calculate outlier count by year
outlier_by_year = gauge_outliers.groupby('year')['value'].count().reset_index(name='outlier_count')
#print(outlier_by_year.sort_values(by='outlier_count'))
#print(outlier_by_year['outlier_count'].dtype)

   # Calculate outlier count by month of year
outlier_by_month = gauge_outliers.groupby('month')['value'].count().reset_index(name='outlier_count')
#print(outlier_by_month.sort_values(by='outlier_count'))

   # Helene gauge and discharge comparison analysis
helene_date_range = pd.date_range(start='2024-09-20', end='2024-10-31')
helene_data = pd.read_parquet('data/discharge_clean.parquet').merge(pd.read_parquet('data/gauge_clean.parquet'), on='time')
helene_data = helene_data[helene_data['time'].isin(helene_date_range)][['time', 'value_x', 'value_y']]
helene_data = helene_data.sort_values(by='time')
helene_data['discharge_change'] = (helene_data['value_x']) - (helene_data['value_x'].shift(1))
helene_data['gauge_change'] = (helene_data['value_y']) - (helene_data['value_y'].shift(1))
ax = helene_data.plot(x='time', y='discharge_change', kind='line', color='red')
helene_data.plot(x='time', y='gauge_change', color='blue', secondary_y=True, ax=ax)
#plt.show()

   # Fresh data pull to look at non hurricane september and october temps to compare to 2024 september and october temps
helene_data = helene_data.merge(pd.read_parquet('data/temperature_clean.parquet'), on='time', how='left')[['time', 'value_x', 'value_y', 'value', 'discharge_change', 'gauge_change']]
helene_data['temp_change'] = (helene_data['value']) - (helene_data['value'].shift(1))
#print(helene_data)

temp = pd.read_parquet('data/temperature_clean.parquet')
temp['month'] = temp['time'].dt.month
sep_temp = temp[temp['month'].isin([9])]
oct_temp = temp[temp['month'].isin([10])]
sep_temp = sep_temp.sort_values(by='time')[['time', 'value']]
oct_temp = oct_temp.sort_values(by='time')[['time', 'value']]
#print(sep_temp.iloc[30:60])
#print(oct_temp.iloc[31:61])

temp = pd.read_parquet('data/temperature_clean.parquet')
#print(temp['value'].kurt())

wide = pd.read_parquet('data/wide_df_clean.parquet')
print(wide['temp_value'].dtype)