SELECT
    r.time_series_id,
    r.monitoring_location_id,
    m.monitoring_location AS location_description,
    r.parameter_code,
    p.parameter_description,
    r.statistic_id,
    s.statistical_description,
    r.time,
    r.value,
    r.unit_of_measure,
    r.approval_status,
    r.qualifier,
    r.last_modified::timestamp AS last_modified,
    r.longitude,
    r.latitude,
    r.feature_id
FROM {{ source('raw', 'raw_readings') }} r
LEFT JOIN {{ ref('parameter_codes') }} p
ON r.parameter_code = p.parameter_code
LEFT JOIN {{ ref('statistical_ids') }} s
ON r.statistic_id = s.statistic_id
LEFT JOIN {{ ref('monitoring_station_ids') }} m
ON r.monitoring_location_id = m.monitoring_location_id