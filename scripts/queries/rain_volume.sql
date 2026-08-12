-- Rain (rain.trade) 30d traded volume, from on-chain order-book fills.
--
-- DefiLlama cannot supply this: its adapter discovers pools from two retired
-- factories and sums an AMM-era EnterOption event, while the live deployment uses a
-- third factory whose pools are order books emitting ExecuteBuy/SellOrder.
--
-- Two event variants are live (192-byte and 160-byte payloads); baseAmount is the
-- 4th non-indexed word, shifted one slot in the variant carrying an extra uint8.
-- maker and taker are indexed, so topic1 = topic2 identifies a self-trade — one
-- address accounts for roughly half of Rain's all-time volume that way.
-- Pools are joined to their collateral token so RAIN-denominated pools (18 dec)
-- cannot corrupt a sum scaled for USDT0 (6 dec).
WITH sig AS (
  SELECT keccak(to_utf8('ExecuteBuyOrder(uint256,uint8,uint256,uint256,uint256,uint256,address,address)')) AS ebo8,
         keccak(to_utf8('ExecuteSellOrder(uint256,uint8,uint256,uint256,uint256,uint256,address,address)')) AS eso8,
         keccak(to_utf8('ExecuteBuyOrder(uint256,uint256,uint256,uint256,uint256,address,address)')) AS ebo7,
         keccak(to_utf8('ExecuteSellOrder(uint256,uint256,uint256,uint256,uint256,address,address)')) AS eso7,
         keccak(to_utf8('PoolTokenSet(address,address,uint256,string,string)')) AS pts
),
pool_token AS (
  SELECT DISTINCT bytearray_substring(l.topic1,13,20) AS pool,
                  bytearray_substring(l.topic2,13,20) AS token
  FROM arbitrum.logs l, sig WHERE l.topic0 = sig.pts
),
fills AS (
  SELECT l.contract_address,
         (l.topic1 = l.topic2) AS self_trade,
         CASE WHEN length(l.data) = 192
              THEN bytearray_to_uint256(bytearray_substring(l.data,129,32))
              ELSE bytearray_to_uint256(bytearray_substring(l.data, 97,32)) END AS base_amount
  FROM arbitrum.logs l, sig
  WHERE l.topic0 IN (sig.ebo8, sig.eso8, sig.ebo7, sig.eso7)
    AND l.block_time >= now() - interval '30' day
)
SELECT sum(CASE WHEN NOT f.self_trade THEN f.base_amount ELSE 0 END)/1e6 AS volume_usd,
       count_if(NOT f.self_trade) AS fills
FROM fills f
JOIN pool_token p ON f.contract_address = p.pool
WHERE p.token = 0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9
