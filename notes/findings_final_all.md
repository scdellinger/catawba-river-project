## Final organized findings for discharge, gauge, and temperature

#### Discharge (measured in ft $^3$/s)
- Discharge data covers 11-11-1987 to 12-31-2025
- There are 199 dates with a qualifier of ESTIMATED
- Full date summary stats:
    - Mean: 251.325834
    - Median: 180
    - Mode: 111 (75 occurrences)
    - Std Dev: 380.389378
    - Range: 12 $\to$ 19600
    - Count: 13931
    - Max: 19,600 (occurring 09-27-2024, effects of hurricane Helene)
        - Every 4.5 seconds, enough water passed through this location to fill and olympic sized pool.
        - That is a 1ft x 1ft column of water 3.71 miles high.

- Distribution shape: Leptokurtic (724)

- Outlier Detection:
    - Q1: 115
    - Q3: 279
    - Q3 - Q1: 164
    - Lower Fence: -131
    - Upper Fence: 525
    - High Upper Fence (Q3 + (3 * IQR)): 771
    - 935/13931 (6.7%) of discharge above upper fence (flood state)
    - 510 medium outliers (between 525 and 771)
    - 425 high outliers (above 771)

- Quality Checks:
    - No missing dates in the data. 199 dates have a qualifier of ESTIMATED.
    - 10/199 (5%) of estimated days were also outliers. This points towards a narrow range of reasons for discharge being estimated, with seemingly flood level flow not falling within the range of reasons.

- Relationships:
    - Analysis shows a strong relationship between discharge and gauge values, with the helene_discharge_gauge visual showing this very well. Link to png visual in README.

- Trend/Pattern:
    - Discharge numbers grouped by the month of the year show elevated discharge sums from December to May, and lowered sums from June to November. This is shown in the month_of_year_discharge visual.
    - You see a slight bump up from the lower totals for the months of August, September, and October, which is right in the middle of hurricane season.
    - The elevated winter/spring months are also influenced by a lack of evapotranspiration, with deciduous trees stopping transpiration completely during dormancy. 
    - 2018 is an outlier year for total discharge over the course of the year. In 2018, hurricanes Florence andThere were 8 separate hurricane remnants that came up from the gulf of mexico and passed over the western nc mountains. Visual in readme for yearly discharge and outliers
    - There were 16 months over the course of the data that were outliers. 4 of the 16 outlier months had confirmed hurricane remnant activity.
    - September of 2004 (42,548) is the highest month within the dataset, 5.57x the mean (7644.59).
    - VWhen removing those 4 months from the data and recalculating kurtosis, it drops from 7.5554 to 2.4518.
    - I also looked at each month to figure out how much the top day in each month contributed to the overall total per month (max discharge of month / total discharge of month). Two outlier months (2024-09 and 2004-09) were in the top 10, with concentrations of 53.5138% and 35.4893% respectively. The other 8 top concentrations were all between August and December, and further research shows that there were still hurricanes present in these high concentrations, but the amount of discharge for the month did not qualify as an outlier. 
    - Further more, if you were to split the year_months into hurricane season and not hurricane season groups, only 5 of the year_month outliers are within hurricane season, and 11 of the outliers are outside of the hurricane season.

- Inferential/Hypothesis: 
    - My initial thought was that discharge would be greatest during the summer/fall months and least during winter and early spring. This in fact was opposite, with the winter spring months dominating discharge, summer and fall being lower. There was some rise in august through october due to tropical storm remnants moving inlands and stalling.


#### Gauge (measured in ft)

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
    - 77/78 (99%) of missing dates also fall within the set of dates where discharge is estimated. The cause for an estimated discharge reading could also be highly affecting the ability to gather a gauge reading as well.

    -  Years/months with gaps and the amount:
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

    - If sorted by month:
        - June: 23
        - February: 19
        - May: 19
        - January: 11
        - December: 3
        - November: 2
        - September: 1

- Relationships
    - As mentioned in discharge, gauge follows the rise and fall of discharge. Also evidenced in the helene_discharge_gauge visual found in the README

- Trend/Pattern
    - Gauge roughly follows the same rise and fall trends of discharge.

- Inferential/Hypothesis
    - I came into the investigation believing that the water height would be pretty consistent throughout the year, and rising and falling with damn discharge or a large summer storm. I was surprised to see how closely gauge height followed the trends of discharge. 

### Temperature (Measured in degrees C)

- Temperature readings had the shortest available date range, from 04-25-2013 to 12-31-2025.
- The kurtosis of temperature is -1.14, indicating that temperature variations are very small and contain zero outliers.
- Looking at the days before and after Helene, water temperature has a small 2-3 C dip when the hurricane reaches the nc mountains, and many "wiggles" in October.
- When looking back at other september and october temps in 2013 and 2014 to compare years without hurricane remnant activity during those months, that same "wiggle" is present in october. I contribute this to seasonal temperature fluctuations similar to the air temperature fluctuations consistent with the onset of Fall.