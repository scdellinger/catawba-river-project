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

   # Show a bar graph with quartiles and outlier thresholds. 
ax = yearly_discharge.plot(x='year', y='value', kind='bar')
ax.axhline(y=l_tightened_fence, color='red', linestyle='--', linewidth=1.5, label='Outlier Threshold')
ax.axhline(y=u_tightened_fence, color='red', linestyle='--', linewidth=1.5)
ax.axhline(y=71409.05, color='purple', linestyle='--', linewidth=1.5, label='25th percentile')
ax.axhline(y=88760.00, color='green', linestyle='--', linewidth=1.5, label='50th percentile')
ax.axhline(y=114062.65, color='orange', linestyle='--', linewidth=1.5, label='75th percentile')
ax.legend()
#plt.show()   

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
print(upper_fence)

   # Show a bar chart with quartiles and outlier thresholds.
ax = monthly_discharge.plot(x='year_month', y='value', kind='bar')
ax.axhline(y=upper_fence, color='red', linestyle='--', linewidth=1.5, label='Medium outliers')
ax.axhline(y=high_upper, color='red', linestyle='--', linewidth=1.5, label='Extreme outliers')
ax.axhline(y=4084.25, color='purple', linestyle='--', linewidth=1.5, label='25th percentile')
ax.axhline(y=6334, color='green', linestyle='--', linewidth=1.5, label='50th percentile')
ax.axhline(y=9669.25, color='orange', linestyle='--', linewidth=1.5, label='75th percentile')
ax.legend()
#plt.show()

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

   # Show a bar chart with quartiles and outlier thresholds.
ax = by_month.plot(x='month', y='value', kind='bar')
ax.axhline(y=244715.15, color='purple', linestyle='--', linewidth=1.5, label='25th percentile')
ax.axhline(y=292839.9, color='green', linestyle='--', linewidth=1.5, label='50th percentile')
ax.axhline(y=333623.65, color='orange', linestyle='--', linewidth=1.5, label='75th percentile')
ax.axhline(y=lower_fence, color='red', linestyle='--', linewidth=1.5, label='Low Outliers')
ax.axhline(y=upper_fence, color='red', linestyle='--', linewidth=1.5, label='High Outliers')
ax.legend()
#plt.show()


   # Look at non hurricane months to see if the statistics change.
hurricane_months = pd.PeriodIndex(['2004-09', '2018-05', '2018-10', '2024-09'], freq=('M'))   # List of months with confirmed hurricane remnant activity
non_hurricane = df[~df['year_month'].isin(hurricane_months)]  
non_hurricane = non_hurricane.groupby('year_month')['value'].sum().reset_index(name='value')

   # .kurt() and .describe() 
#print(non_hurricane['value'].kurt())
#print(non_hurricane.describe())


concentration = df.groupby('year_month')['value'].max() / df.groupby('year_month')['value'].sum()
#print(concentration.sort_values(ascending=False).head(10))


monthly_discharge['month'] = monthly_discharge['year_month'].dt.month
hurricane_months = [6, 7, 8, 9, 10, 11]
hurricane_season = monthly_discharge[monthly_discharge['month'].isin(hurricane_months)]
not_hurricane_season = monthly_discharge[~monthly_discharge['month'].isin(hurricane_months)]
print(len(hurricane_season))
print(len(not_hurricane_season))
print(len(hurricane_season[hurricane_season['value'] > 18046.75]))
print(len(not_hurricane_season[not_hurricane_season['value'] > 18046.75]))


# ------------------------------|
# Daily Discharge Investigation |
# ------------------------------|

   # Look at daily discharge and see any trends
daily_discharge = pd.read_parquet('data/discharge_clean.parquet')
daily_discharge = daily_discharge.rename(columns={'time': 'date'})[['date', 'value']]
daily_discharge['year_month'] = daily_discharge['date'].dt.to_period('M')
daily_discharge['year'] = daily_discharge['date'].dt.year
daily_discharge['month'] = daily_discharge['date'].dt.month
hurricane_months = [6, 7, 8, 9, 10, 11]
hurricane_season = daily_discharge[daily_discharge['month'].isin(hurricane_months)]
not_hurricane_season = daily_discharge[~daily_discharge['month'].isin(hurricane_season)]
#print(daily_discharge.sort_values(by='value', ascending=False).head(50))

   # .kurt() and .describe()
#print(daily_discharge['value'].kurt())
#print(daily_discharge['value'].describe())      

#print(len(hurricane_season[hurricane_season['value'] > 771]))
#print(len(not_hurricane_season[not_hurricane_season['value'] > 771]))
