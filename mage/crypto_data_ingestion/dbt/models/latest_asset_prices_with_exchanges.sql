{{
    config(
        materialized='table'
    )
}}

with latest_assets as (
    select 
        id,
        max(timestamp) as latest_timestamp
    from {{ source('staging', 'historical_assets') }}
    group by id
),

asset_prices as (
    select 
        ha.id,
        ha.priceUsd,
        ha.circulatingSupply,
        ha.timestamp
    from {{ source('staging', 'historical_assets') }} ha
    join latest_assets la on ha.id = la.id and ha.timestamp = la.latest_timestamp
)

select 
    ap.id,
    cast(ap.priceUsd as float64) as latest_price_usd,
    ap.circulatingSupply,
    m.exchangeId,
    e.name as exchange_name,
    cast(m.volumeUsd24Hr as float64) as volume_usd_24hr,
    cast(m.percentExchangeVolume as float64) as percent_exchange_volume
from asset_prices ap
join {{ source('staging', 'market') }} m on ap.id = m.baseId
join {{ source('staging', 'exchanges') }} e on m.exchangeId = e.exchangeId  
order by ap.id asc
