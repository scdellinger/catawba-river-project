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
