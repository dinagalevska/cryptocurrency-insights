{{
    config(
        materialized='table'
    )
}}

with exchange_volume as (
    select 
        exchangeId,
        timestamp,
        sum(cast(volumeUsd24Hr as float64)) as total_volume
    from {{ source('staging', 'market') }}
    where volumeUsd24Hr is not null
    group by exchangeId, timestamp
)

select 
    exchangeId,
    timestamp,
    total_volume,
    (total_volume / sum(total_volume) over (partition by timestamp)) * 100 as volume_contribution_percentage
from exchange_volume
order by timestamp, total_volume desc

--Ова помага да се види која берза има најголем пазарен дел и која берза има најмал обем на тргување во одреден период.