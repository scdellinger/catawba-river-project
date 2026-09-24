with 
percentiles as (
    select
      quantile_cont(value, 0.25) as q1,
      quantile_cont(value, 0.75) as q3,
      quantile_cont(value, 0.75) - quantile_cont(value, 0.25) as iqr
    from {{ ref('int_discharge_readings') }}
    where statistic_id = '00003'
),
upper_fence as (
    select
      q1,
      q3,
      iqr,
      q3 + (iqr * 1.5) as upper_fence
    from percentiles
)

select
  count(case when is_hurricane_season = true then 1 end) as in_season_outliers,
  count(case when is_hurricane_season = false then 1 end) as not_in_season_outliers
from {{ ref('int_discharge_readings') }} dr
cross join upper_fence uf
where dr.value >= uf.upper_fence
and dr.statistic_id = '00003'