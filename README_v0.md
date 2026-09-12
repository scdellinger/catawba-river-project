# The Catawba River in My Lifetime

 ---

 ## Introduction

- Core Question: How does water level and temperature change throughout the year on the Catawba River?

 This project will look at any trends or interesting information gleaned from the monitoring station on the Catawba River to answer the core question. This monitoring station is located in McDowell County NC, just west of the town of Marion. This project will cover three parameters: discharge, gauge, and temperature. Because of the availability of data, these parameters will be starting at three different dates, listed below. With this "rolling start" of data, we will be able to start with any hypotheses, and test their validity as more information is brought in. The data for this project is being pulled from the USGS API.

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


## Data Cleaning

- Discharge (1987-2025): 0 date gaps across the entire record.
- Gauge height (2001-2025): 78 missing dates, mostly explained below.
- Temperature (2013-2025): 6 missing dates.
- 199 discharge records carry an "Estimated" qualifier — see Columns Kept above for what this means. These dates are scattered across 1988-2025 rather than clustered, consistent with sporadic short-term disruptions (ice, equipment, or rating-curve instability) rather than one sustained outage.
- Cross-referencing gap dates against estimated-discharge dates shows 99% of gauge-height gaps and 50% of temperature gaps occurred on the same days discharge required estimation — strong evidence of a shared disruption (most likely ice or equipment) affecting multiple sensors at the gauge simultaneously. No single date shows all three issues at once, though this isn't surprising given how rare gauge and temperature gaps are individually.
- Full year-by-month gap breakdown and supporting detail are in `findings.md`.