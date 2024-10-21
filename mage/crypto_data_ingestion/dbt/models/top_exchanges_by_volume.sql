{{
    config(
        materialized='table'
    )
}}

select 
    m.exchangeId,
    e.name,
    e.rank,
    cast(m.volumeUsd24Hr as float64) as volume_usd_24hr,  
    m.percentExchangeVolume
from {{ source('staging', 'market') }} m
join {{ source('staging', 'exchanges') }} e on m.exchangeId = e.exchangeId
where m.volumeUsd24Hr is not null  
order by volume_usd_24hr desc
