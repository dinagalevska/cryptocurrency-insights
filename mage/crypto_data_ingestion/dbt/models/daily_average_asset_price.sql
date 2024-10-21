-- daily_average_asset_price.sql
{{
    config(
        materialized='table'
    )
}}

with daily_asset_prices as (
    select 
        id,
        cast(priceUsd as float64) as price_usd,
        date(timestamp) as date  -- Extracting date for daily aggregation
    from {{ source('staging', 'historical_assets') }}  
)

select 
    id, 
    date, 
    avg(price_usd) as avg_daily_price
from daily_asset_prices
group by 
    id, 
    date
order by 
    id asc, 
    date asc
