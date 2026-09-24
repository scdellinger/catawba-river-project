with 
helene_discharge as (
    select 
        time as date,
        value as discharge_value
    from {{ ref('int_discharge_readings') }}
    where time::date between '2024-09-20' and '2024-10-20'
),
helene_gauge as (
    select 
        time as date,
        value as gauge_value
    from {{ ref('int_gauge_readings') }}
    where time::date between '2024-09-20' and '2024-10-20'
)
select
    hd.date,
    hd.discharge_value,
    hg.gauge_value
from helene_discharge hd
join helene_gauge hg
on hd.date = hg.date
order by 1