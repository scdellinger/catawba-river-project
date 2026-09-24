select
    extract(month from time) as month,
    sum(value)::numeric(15,2) as total_discharge
from {{ ref('int_discharge_readings') }}
where statistic_id = '00003'
group by 1
order by 1