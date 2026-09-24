with gauge_filter AS (
    select *
    from {{ ref('stg_raw_readings') }}
    where parameter_code = '00065'
)

select
    *,
    case 
        when extract(month from time) between 6 and 11 then true
        else false
    end as is_hurricane_season
from gauge_filter