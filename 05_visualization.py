import pandas as pd
import matplotlib.pyplot as plt

   # Yearly discharge visual showing that the year containing the greatest daily discharge mean isn't the outlier year.
df = pd.read_parquet('data/discharge_clean.parquet')[['time', 'value']]
df = df.rename(columns={'time': 'date'})
df['year'] = df['date'].dt.year
df = df.groupby('year')['value'].sum().reset_index(name='total')

q1 = 65555.75
q3 = 113595
iqr = q3 - q1
lower_fence = q1 - (iqr * 1.5)
upper_fence = q3 + (iqr * 1.5)

ax = df.plot(y='total', x='year', kind='bar', title='Yearly Discharge With Outlier Threshold')
ax.axhline(y=upper_fence, color='red', linestyle='--', linewidth=1.5, label='Outlier Threshold')
ax.legend()
plt.savefig('visuals/yearly_discharge_outliers.png', dpi=150, bbox_inches='tight')

   # Month of year discharge showing dec-may higher discharge compared to june-november lower discharge
df = pd.read_parquet('data/discharge_clean.parquet')[['time', 'value']]
df = df.rename(columns={'time': 'date'})
df['month'] = df['date'].dt.month
df = df.groupby('month')['value'].sum().reset_index(name='total')
df['months'] = pd.to_datetime(df['month'], format='%m').dt.month_name()


ax = df.plot(y='total', x='months', kind='bar', title='Month of Year Discharge Comparison')
ax.axhline(y=292839.9, color='black', linestyle='--', linewidth=1.5, label='Median discharge value')
plt.xticks(rotation=45, ha='right')
ax.legend()
plt.savefig('visuals/month_of_year_discharge.png', dpi=150, bbox_inches='tight')
plt.show()
   # Helene discharge/gauge comparison

df = pd.read_parquet('data/discharge_clean.parquet').merge(pd.read_parquet('data/gauge_clean.parquet'), on='time')
df = df.rename(columns={'time': 'date', 'value_x': 'discharge_value', 'value_y': 'gauge_value'})[['date', 'discharge_value', 'gauge_value']]
print(df.columns)
helene_date_range = pd.date_range(start='2024-09-20', end='2024-10-20', freq='D')
df = df[df['date'].isin(helene_date_range)]
df = df.sort_values(by='date')

ax = df.plot(y='discharge_value', x='date', color='blue', title='Helene Discharge and Gauge Height Extremes')
df.plot(y='gauge_value', x='date', color='red', secondary_y=True, ax=ax)

ax.set_ylabel('Discharge (ft³/s)')
ax.right_ax.set_ylabel('Gauge Height (ft)')

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax.right_ax.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax.axvline(x=pd.Timestamp('2024-09-27'), color='gray', linestyle=':', linewidth=1)
ax.annotate('Peak: 9/27\n19,600 ft³/s, 15.75 ft', 
            xy=(pd.Timestamp('2024-09-27'), 19600),
            xytext=(10, 10), textcoords='offset points',
            fontsize=9)
plt.savefig('visuals/helene_discharge_gauge.png', dpi=150, bbox_inches='tight')

   # Hurricane and non hurricane outliers, months and days
df = pd.read_parquet('data/discharge_clean.parquet')
df = df.rename(columns={'time': 'date'})[['date', 'value']]
df['month'] = df['date'].dt.month
df['year_month'] = df['date'].dt.to_period('M')
hurricane_months = [6, 7, 8, 9, 10, 11]
df['hurricane_season'] = df['month'].isin(hurricane_months)


   # Daily outliers within each season
#print(df['value'].describe())
q1 = 115
q3 = 279
iqr = q3 - q1
upper_fence = q3 + (iqr * 1.5)

d_hurr_season = df[df['hurricane_season'] == True]
d_not_hurr_season = df[df['hurricane_season'] == False]
daily_hurr_outliers = len(d_hurr_season[d_hurr_season['value'] >= upper_fence])
daily_not_hurr_outliers = len(d_not_hurr_season[d_not_hurr_season['value'] >= upper_fence])


   # Monthly outliers within each season
monthly = df.groupby('year_month')['value'].sum().reset_index(name='total')

#print(monthly['total'].describe())
q1 = 4084.25
q3 = 9669.25
iqr = q3 - q1
upper_fence = q3 + (iqr * 1.5)

m_hurr_season = df[df['hurricane_season'] == True]
m_not_hurr_season = df[df['hurricane_season'] == False]
monthly_not = m_not_hurr_season.groupby('year_month')['value'].sum().reset_index(name='total')
monthly_yes = m_hurr_season.groupby('year_month')['value'].sum().reset_index(name='total')
monthly_hurr_outliers = len(monthly_yes[monthly_yes['total'] >= upper_fence])
monthly_hurr_not_outliers = len(monthly_not[monthly_not['total'] >= upper_fence])

fig, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(m_categories, m_values, color=['red', 'green'])
ax2.set_title('Monthly Outliers')
plt.tight_layout()
plt.savefig('visuals/monthly_outlier_hurricane_comparison', dpi=150, bbox_inches='tight')

   # Daily outliers within each season
d_values = [daily_hurr_outliers, daily_not_hurr_outliers]
m_values = [monthly_hurr_outliers, monthly_hurr_not_outliers]
d_categories = ['Daily outliers in hurricane season', 'Daily outliers not in hurricane season']
m_categories = ['Monthly outliers in hurricane season', 'Monthly outliers not in hurricane season']

fig, ax1 = plt.subplots(figsize=(10, 6)) 
ax1.bar(d_categories, d_values, color=['red', 'green'])
ax1.set_title('Daily Outliers')
plt.tight_layout()
plt.savefig('visuals/daily_outlier_hurricane_comparison', dpi=150, bbox_inches='tight')


