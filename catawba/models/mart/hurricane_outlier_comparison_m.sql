with
percentiles as (
    select
      quantile_cont(total_discharge, 0.25) as q1,
      quantile_cont(total_discharge, 0.75) as q3,
      quantile_cont(total_discharge, 0.75) - quantile_cont(total_discharge, 0.25) as iqr
    from {{ ref('monthly_discharge') }}
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
  count(case when md.hurricane_season = true then 1 end) as in_hurricane_season,
  count(case when md.hurricane_season = false then 1 end) as not_in_hurricane_season
from {{ ref('monthly_discharge') }} md
cross join upper_fence uf
where md.total_discharge >= uf.upper_fence