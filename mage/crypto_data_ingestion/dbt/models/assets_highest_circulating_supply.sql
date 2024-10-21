{{
    config(
        materialized='table'
    )
}}

select 
    id,
    cast(circulatingSupply as float64) as circulating_supply,
    timestamp
from {{ source('staging', 'historical_assets') }}
where circulatingSupply is not null
order by circulating_supply desc

--koj kriptovaluti se najdostapni u vreme
