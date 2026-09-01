# Catawba River Discharge/Gauge/Temp Analysis
 ---

 ## Introduction

 This project will look at any trends or interesting information gleaned from the USGS-02137727 monitoring station on the Catawba River. This monitoring station is located in McDowell County NC, just west of the town of Marion. This project will cover three parameters: discharge, gauge, and temperature. Because of the availability of data, these parameters will be starting at three different dates, listed below. With this "rolling start" of data, we will be able to start with any hypotheses, and test their validity as more information is brought in. The data for this project is being pulled from the USGS API.
## Clarifications

#### Parameter codes and date ranges

- Discharge(00060) data is from 11-11-1987 to 12-31-2025
- Gauge(00065) data is from 10-01-2001 to 12-31-2025
- Temperature(00010) data is from 04-25-2013 to 12-31-2025

#### Statistic ids

- Max (00001), min (00002), and mean (00003) are the statistical ids recorded. Each were consistent with the date range covered, but the number of rows under statistical ID 00003 far outnumbered the others. This has lead me to only explore mean initially. Max and min may be brought in at a later time for more analysis. All mentions of 'data' are in reference to this scope, and will be addressed once max and min are brought in.

#### Columns Kept

- Monitoring Station Id: This one could technically be dropped, and may be eventually.
- Statistic ID: This is the ID code for the mean value for the day
- Parameter Code: This identifies the parameter. Code reference is above.
- Time: Initial investigation shows that this is a date and not an actual time. I may change this column header in the future.
- Value: This gives the value of the parameter being measured
- Unit of Measure: What units the value is portrayed in.
- Approval Status: Can be provisional or approved. Provisional are unverified records, approved have undergone QA, review, and any necessary recalibration.
- Qualifier: For record of anomalies, data limitations, or the status of the recorded value. "Estimated" values occur when a direct measurement wasn't available for that day (commonly due to ice, equipment issues, or channel/rating-curve instability).

---

## Data Cleaning

- 199 rows of the date show a qualifier of 'ESTIMATED'.
- There are zero gaps in the discharge data in respect to time.
- There are 78 missing days of gauge data within its timeframe.
- there are 6 missing days of temperature data within its timeframe.