select
    extract(year from time) as year,
    sum(value)::numeric(15,2) as total_discharge
from {{ ref('int_discharge_readings') }}
where statistic_id = '00003'
group by extract(year from time)
order by year desc
