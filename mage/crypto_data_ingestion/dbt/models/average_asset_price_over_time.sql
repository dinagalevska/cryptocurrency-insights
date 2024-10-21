-- average_asset_price_over_time.sql
{{
    config(
        materialized='table'
    )
}}

with asset_prices as (
    select 
        id,
        cast(priceUsd as float64) as price_usd,
        timestamp
    from {{ source('staging', 'historical_assets') }}  
)

select 
    id, 
    timestamp, 
    avg(price_usd) as avg_price
from asset_prices
group by 
    id, 
    timestamp
order by 
    id asc, 
    timestamp asc
