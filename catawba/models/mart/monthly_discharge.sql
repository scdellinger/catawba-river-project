select
    time_bucket(interval '1 month', time)::date as month_year,
    sum(value)::numeric(15,2) as total_discharge,
    case
      when extract(month from any_value(time)) in (6, 7, 8, 9, 10, 11)
      then true
      else false
    end as hurricane_season
from {{ ref('int_discharge_readings') }}
where statistic_id = '00003'
group by 1
order by 1