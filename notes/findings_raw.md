## Phase 2 (Clean and Explore)

#### Estimated

Some questions that come up with this are:
- Do any of these dates coincide with the gaps in discharge, gauge, or temperature?


- There are 199 instances in the data of qualifier being ESTIMATED.
- First date: 1988-01-07
- Last date: 2025-01-24
- 2009 has the most estimated days: 32
- 77/78 (99%) missing dates for gauge values coincide with an estimated discharge date.
- 3/6 (50%) missing dates for temperature values coincide with an estimated discharge date.
- A 3-way intersection of the estimated discharge dates, missing gauge dates, AND missing temperature dates does not exist. There is not a single day where all three occur on the same date.

#### Discharge (ft $^3$/s)

- Covers dates from 11-11-1987 to 12-13-2025
- Full date summary stats:
    - Mean: 251.325834
    - Median: 180
    - Mode: 111 (75 occurrences)
    - Std Dev: 380.389378
    - Range: 12 $\to$ 19600
    - Count: 13931
    - Max: 19,600
        - Every 4.5 seconds, enough water passed through this location to fill and olympic sized pool.
        - That is a 1ft x 1ft column of water 3.71 miles high.

- Distribution shape: Leptokurtic (724)

- Outlier Detection:
    - Q1: 115
    - Q3: 279
    - Q1 - Q3: 164
    - Lower Fence: -131
    - Upper Fence: 525
    - High Upper Fence (Q3 + (3 * IQR)): 771
    - 935/13931 (6.7%) of discharge above upper fence (flood state)
    - 510 medium outliers (between 525 and 771)
    - 425 high outliers (above 771)

- Quality Checks:
    - No missing dates in the data. 199 dates have a qualifier of ESTIMATED.
    - 10/199 (5%) of estimated days were also outliers. This points towards a narrow range of reasons for discharge being estimated, with seemingly flood lever flow not falling within the range of reasons.

- Relationships:

- Trend/Pattern:

- Inferential/Hypothesis: 

#### Gauge Height (ft)

- Covers dates from 10-01-2001 to 12-31-2025

- Full date summary stats:
    - Mean: 1.984065
    - Median: 1.88
    - Mode: 1.88 (118 occurrences)
    - Std Dev: 0.704675
    - Range: 0.68 $\to$ 15.78
    - Count: 8780

- Distribution Shape: Leptokurtic (~46.59)

- Outlier Detection:
    - Q1: 1.59
    - Q3: 2.2
    - Q3 - Q1: 0.61
    - Lower Fence: 0.675
    - Upper Fence (Q3 + (1.5 * IQR)): 3.115
    - High Upper Fence (Q3 + (3 * IQR)): 4.03
    - 398/8780 (~4.5%) of gauge readings above upper fence (flood state)
    - 249 medium outliers (between 3.115 and 4.01)
    - 149 high outliers (above 4.01)

- Quality Checks:
    - There are 78 date gaps in gauge data.
    - These gaps are spread out over 7 different years, from 2002 to 2020. 
    - 77/78 (99%) of missing dates also fall within the set of dates where discharge is estimated. This points to whatever the reasoning are for an estimated discharge also affects the ability of receiving gauge readings.

Years/months with gaps and the amount:
- 2020: 27
    -   May: 4
    - June: 23
- 2009: 23
    - January: 7
    - February: 15
    - September: 1
- 2003: 15
    - May: 15
- 2006: 8
    - January: 4
    - February: 4
- 2004: 2
    - November: 2
- 2002: 2
    - December: 2
- 2005: 1
    - December: 1

If sorted by month:
- June: 23
- February: 19
- May: 19
- January: 11
- December: 3
- November: 2
- September: 1

- Relationships

- Trend/Pattern

- Inferential/Hypothesis

#### Temperature (Deg C)

- Covers dates from 04-25-2013 $\to$ 12-31-2025

- Full data summary stats:
    - Mean: 14.624611
    - Median: 15
    - Mode: 
    - Std Dev: 6.242122
    - Range: 0.2 $\to$ 26.6
    - Count: 4628

- Distribution Shape: platykurtid (~ -1.14)

- Outlier Detection:
    - Q1: 9.2
    - Q3: 20.125
    - IQR (Q3 - Q1): 10.925
    - Lower Fence: -7.1875
    - Upper Fence: 36.5125
    - All temperature readings fall within the lower and upper fences as expected with a platykurtic distribution.
    - The platykurtic nature of the distribution show that temperature changes are seasonal driven.

- Quality Checks
    - There are 6 date gaps in temperature data from 2013-4-25 to 2025-12-31.

Years/months with gaps and the amounts:
- 2025
    - January: 3
- 2014
    - June: 2
- 2016
    - October: 1

- Relationships:

- Trend/Patterns:

- Inferential/Hypothesis:

#### Hurricane Helene — Discharge Event (September-October 2024)
- Pre-storm baseline: Still being computed. There are a couple spikes before Helene that need to be investigated. Initial assumption is either storm or dam water release.
- Peak reading of discharge is 19,600(!) ft $^3$/s on 2024-09-27


#### Outlier Column Added, DataFrames Parquet 

- Boolean mask column added to each parameter dataframe that records whether or not the value falls below the lower fence or above the upper fence.
- Data folder created and parquet applied to each dataframe for preservation and stored in the data folder.

---

## Phase 3 (Transform and Pivot)

- Dataframes merged into one wide_df dataframe, merged on time.
- Column names updated 
- Monitoring location id and statistical id are consistent for each row (USGA-02137727 and 00003, respectively) so they were dropped from the data frame.
- 'time' was renamed to 'date' to better reflect that the data shown is the mean for a day, with no timestamp applied.
- 13,931 rows confirmed. All dates from 1987-11-11 to 2025-12-31 present.
- Columns reordered so that date appears first (grain of dataframe is one row = one day) and remaining columns are grouped by parameter [discharge, gauge, temp].

---

## Phase 4 (Exploratory Analysis)

- Look at yearly discharge rates and pinpoint outliers.
    - Yearly kurtosis has a value of 0.9356, a near normal distribution.
    
    - .describe() results:
        - count: 38
        - mean: 91889.66
        - std: 36068.50
        - min: 38308.20
        - 25%: 71409.05
        - 50%: 88760.00
        - 75%: 114062.65
        - max: 200507.00
    
    - Further investigation shows that 2018 is an outlier year for discharge at monitoring location USGS-2137727.
        - Initial investigation show that there were several tropical storms and hurricanes that pushed inland and stalled over the NC mountains region. 2018 needs deeper investigation by month.
        - Hurricanes Florence and Michael are major contributors
    
    - Tighten outlier threshold to see if other hurricane years can be identified.
        - Tightening the upper fence produced 2020 as another outlier year.
        - 8 different hurricanes contributed to immense rainfall in the western NC mountains.

- Look at monthly discharge rates and pinpoint outliers.
    - Month by month kurtosis has a value of 7.5554, leptokurtic with non-normal distribution.
    - .describe() results:
        - count: 
        - mean: 
        - std: 
        - min: 
        - 25%: 
        - 50%: 
        - 75%: 
        - max: 

    - Specifically hone in on 2018 and 2020, as they were outlier years
    
    - There are 11 medium outliers (>= Q3 + (IQR * 1.5) and < high) and 5 high outliers (>= Q3 + (IQR * 3)). 
        - Two of the high outlier months fall inside 2018, the months of May and December. November of 2018 is also a medium outlier. 
        - September of 2004 (42,548) is the highest month within the dataset, 5.57x the mean (7644.59).
        - Outliers:
            - 03-1990, Not hurricane, intense rainfall from storm
            - 06-1992, Not hurricane, rainfall from several storms
            - 03-1993, Not hurricane, 'Storm of the Century' blizzard, 18-24 in of snow in 1-2 days, temperatures started warming up a few days later
            - 01-1995, Not hurricane, snow and rain
            - 01-1998, Not hurricane, plenty of rain, el nino
            - 02-1998, not hurricane, plenty of rain, el nino
            - * 09-2004, Hurricane remnants from Frances, Ivan, and Jeanne
            - 05-2013, Not hurricane, consistent storms
            - 07-2013, Not hurricane, consistent storms
            - 12-2015, Not hurricane, storms, el nino
            - * 05-2018, 'hurricane', tropical weather and subtropical storm alberto
            - * 10-2018, Hurricane Michael. Florence came through in september and did drop a ton of rain, but most of that went to filling aquifers and then when michael came there was no where else for that water to go
            - 12-2018, Not hurricane, winter storm diego
            - 01-2019, Not hurricane, heavy rainfall
            - 05-2020, Not hurricane, heavy rain
            - * 09-2024, Hurricane Helene
        - Only 4 of the 16 outlier months were impacted by hurricane
        
        - Outlier count by year:
            - 1: [1990, 1992, 1993, 1995, 2004, 2015, 2019, 2020, 2024]
            - 2: [1998, 2013]
            - 3: 2018
        
        - There is still presence of outliers in the '90s, but we see years in the 2010s where there are multiple months of outliers. 
        - The data hints that outliers in the late summer to fall months can be contributed to hurricanes, while the prevalent case of winter/spring outliers come from storm systems that originate from warm air pouring in from the gulf of mexico. May 2020 is special because it is from subtropical storm Alberto that formed outside of the hurricane season, but had the same makings of a hurricane.
        - The kurtosis of month by month discharge values drops from 7.5554 to 2.4518 when removing months that have known hurricane remnant activity. 
        - This appears to signal that even though these weather events can prove catastrophic, there are still non hurricane months that bring exceptionally high discharge amounts. This area is no stranger to the risk of flash floods. Where the hurricane months stand out is that they fall in a season with low discharge levels naturally, and there are large amounts of water that are dumped on the mountainside in a short period of time, and that was has to go somewhere.
        - I also looked at each month to figure out how much the top day in each month contributed to the overall total per month (max discharge of month / total discharge of month). Two outlier months (2024-09 and 2004-09) were in the top 10, with concentrations of 53.5138% and 35.4893% respectively. The other 8 top concentrations were all between August and December, and further research shows that there were still hurricanes present in these high concentrations, but the amount of discharge for the month did not qualify as an outlier. 
        - Further more, if you were to split the year_months into hurricane season and not hurricane season groups, only 5 of the year_month outliers are within hurricane season, and 11 of the outliers are outside of the hurricane season.
    
    - Looking at the data by month of the year, December thru May have higher than median discharge totals, with June thru November showing below median levels.
        - June, July, August, and November fall below the 25th percentile (244715.2), and January, March, and April falling above the 75th percentile (333623.7). May is just below at 330743.9
        - Initial assumption is that the high winter months see elevated discharge from snow melt, and the reduced summer and fall months are due to drier seasons. 

- Take another look at daily discharge rates and further investigate the extreme outliers to see how many coincide with atlantic hurricanes impacting the southern appalachian mountains.
    - Only two of the top days ranked by discharge were not related to a tropical, subtropical, or hurricane
    - 188 of the 603 extreme outlier days happened within the hurricane season
