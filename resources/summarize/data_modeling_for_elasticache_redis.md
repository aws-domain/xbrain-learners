# Data Modeling for Amazon ElastiCache for Redis - Core Knowledge Summary

## Module 1: Fundamental Concepts

### Introduction

Amazon ElastiCache for Redis là dịch vụ in-memory data store fully managed, cung cấp:
- **Sub-millisecond latency** cho read/write operations
- Hỗ trợ engines: **Valkey**, **Redis OSS**, **Memcached**
- Deployment modes: **Serverless** hoặc **Node-based clusters**
- High availability: replication, automatic failover, backup/restore

**Khi nào dùng Redis/Valkey thay vì Memcached:**
- Cần data structures phức tạp (không chỉ simple strings)
- Cần persistence, replication, high availability
- Cần Pub/Sub, Sorted Sets, Geospatial, Streams
- Cần backup/restore

---

### Keys

Keys là identifiers duy nhất cho mỗi value trong Redis. Best practices:

| Quy tắc | Giải thích |
|---------|-----------|
| **Naming convention** | Dùng hierarchical structure với colon separator: `APPNAME:CONTEXT:ID` |
| **Ví dụ** | `order-app:customer:123`, `session:user:456` |
| **Max size** | 512 MB (nhưng nên giữ ngắn) |
| **Readable keys** | `user:1001:profile` tốt hơn `u1001p` |
| **Tránh trùng lặp** | Naming convention giúp giảm unintentional overwriting |

**Key expiration (TTL):**
- `EXPIRE key seconds` — Set thời gian sống cho key
- `TTL key` — Kiểm tra thời gian còn lại
- `PERSIST key` — Xóa expiration
- Khi key expire, Redis tự động xóa → giải phóng memory

**Key commands quan trọng:**
```
SET key value          — Tạo/ghi đè key
GET key                — Lấy value
DEL key                — Xóa key
EXISTS key             — Kiểm tra key tồn tại
KEYS pattern           — Tìm keys theo pattern (⚠️ blocking, dùng SCAN thay thế)
SCAN cursor [MATCH pattern] — Non-blocking iteration qua keys
```

---

### Data Types

Redis hỗ trợ nhiều data types phong phú:

#### 1. Strings
- Kiểu cơ bản nhất, lưu text, numbers, serialized objects, binary data
- Max size: 512 MB
- Commands: `SET`, `GET`, `INCR`, `DECR`, `APPEND`, `MGET`, `MSET`

```
SET user:name "Alice"
INCR page:views          → atomic counter
SETEX session:abc 3600 "data"  → set with TTL
```

#### 2. Hashes
- Collection of field-value pairs (giống object/dictionary)
- Phù hợp lưu objects với nhiều attributes
- Commands: `HSET`, `HGET`, `HMSET`, `HMGET`, `HGETALL`, `HDEL`, `HINCRBY`

```
HSET user:1001 name "Alice" age 30 city "Hanoi"
HGET user:1001 name        → "Alice"
HINCRBY user:1001 age 1    → 31
```

**Best practice:** Tránh hash quá lớn (multi-GB). Dùng `HGET`/`HMGET` thay vì `HGETALL` cho large hashes.

#### 3. Lists
- Ordered collection of strings (linked list)
- Hỗ trợ push/pop từ cả hai đầu → dùng làm queue hoặc stack
- Commands: `LPUSH`, `RPUSH`, `LPOP`, `RPOP`, `LRANGE`, `LLEN`, `LINDEX`

```
LPUSH notifications:user1 "New message"
RPUSH queue:tasks "task_1"
LRANGE notifications:user1 0 9   → 10 items gần nhất
```

#### 4. Sets
- Unordered collection of unique strings
- Hỗ trợ set operations: union, intersection, difference
- Commands: `SADD`, `SREM`, `SMEMBERS`, `SISMEMBER`, `SUNION`, `SINTER`, `SDIFF`

```
SADD tags:post:1 "redis" "aws" "cache"
SISMEMBER tags:post:1 "redis"     → 1 (true)
SINTER tags:post:1 tags:post:2    → common tags
```

#### 5. Sorted Sets (ZSets)
- Set + score cho mỗi member → tự động sắp xếp theo score
- Dùng cho leaderboards, rankings, time-series, priority queues
- Commands: `ZADD`, `ZRANGE`, `ZREVRANGE`, `ZRANK`, `ZREVRANK`, `ZSCORE`, `ZRANGEBYSCORE`

```
ZADD leaderboard 100 "player1" 250 "player2"
ZREVRANGE leaderboard 0 9         → Top 10 players
ZRANK leaderboard "player1"       → rank (0-based)
```

#### 6. Streams
- Append-only log structure cho event streaming
- Hỗ trợ consumer groups, acknowledgment, pending messages
- Commands: `XADD`, `XREAD`, `XRANGE`, `XLEN`, `XGROUP`, `XACK`

```
XADD mystream * sensor_id 1 temperature 25.3
XREAD COUNT 10 STREAMS mystream 0
```

#### 7. Geospatial Indexes
- Lưu trữ longitude/latitude, tính khoảng cách, tìm vị trí lân cận
- Commands: `GEOADD`, `GEODIST`, `GEORADIUS`, `GEOSEARCH`, `GEOPOS`

```
GEOADD stores 106.6297 10.8231 "store_hcm"
GEOADD stores 105.8342 21.0278 "store_hn"
GEODIST stores "store_hcm" "store_hn" km
GEOSEARCH stores FROMMEMBER "store_hcm" BYRADIUS 50 km
```

#### 8. Bitmaps & HyperLogLog
- **Bitmaps**: Thao tác bit-level trên strings → tracking, flags
- **HyperLogLog**: Probabilistic counting unique elements (error ~0.81%)

```
SETBIT user:login:20240101 1001 1   → user 1001 logged in
PFADD unique:visitors "user1" "user2"
PFCOUNT unique:visitors              → approximate count
```

#### 9. JSON (ElastiCache mở rộng)
- Lưu trữ JSON documents trực tiếp
- Max 64 MB, nesting depth 128
- JSONPath syntax cho query

---

### Time Complexity (Big O Notation)

Mỗi Redis command có time complexity xác định. Đây là yếu tố **cực kỳ quan trọng** khi thiết kế data model:

| Complexity | Ý nghĩa | Ví dụ commands |
|-----------|---------|---------------|
| **O(1)** | Constant time — không phụ thuộc data size | `GET`, `SET`, `HGET`, `HSET`, `LPUSH`, `RPUSH`, `SADD`, `ZADD` |
| **O(log N)** | Logarithmic — tăng chậm theo data size | `ZRANK`, `ZRANGE` (sorted set lookup) |
| **O(N)** | Linear — tỷ lệ thuận với data size | `KEYS *`, `HGETALL`, `SMEMBERS`, `LRANGE 0 -1` |
| **O(N*M)** | Multiply — expensive | `SUNION` (nhiều large sets) |
| **O(N+M*log(M))** | Sort operations | `SORT` |

**Nguyên tắc quan trọng:**
- Redis là **single-threaded** → 1 command blocking sẽ block tất cả clients
- **TRÁNH** commands O(N) trên large datasets trong production
- Dùng `SCAN` thay `KEYS`, `HSCAN` thay `HGETALL` cho large collections
- Dùng `HGET`/`HMGET` thay `HGETALL` khi chỉ cần vài fields
- Batch operations (`MGET`, `MSET`, pipeline) giảm round-trips nhưng vẫn O(N)

---

## Module 2: Redis Data Type Use Cases

### Use Case 1: Database Performance Enhancement (Caching)

#### Tại sao cần caching:
- Database queries (đặc biệt JOINs, aggregations) chậm và expensive
- Mỗi 100ms latency tăng → sales giảm 1% (theo Amazon)
- Redis cache: sub-millisecond access vs. database: 5-50ms+

#### Caching Strategies

##### 1. Cache-Aside (Lazy Loading) — Reactive

```
Application Request
       ↓
  ┌─ Cache Hit? ─┐
  │  YES         │  NO
  ↓              ↓
Return        Query DB
from cache       ↓
             Write to Cache
                 ↓
             Return data
```

**Ưu điểm:**
- Chỉ cache data thực sự được request → tiết kiệm memory
- Node failure không fatal (chỉ tăng latency)
- Đơn giản implement

**Nhược điểm:**
- Cache miss penalty: 3 round-trips (cache check → DB query → cache write)
- Data có thể stale (không tự update khi DB thay đổi)

##### 2. Write-Through — Proactive

```
Application Write
       ↓
  Write to DB
       ↓
  Write to Cache
       ↓
    Return
```

**Ưu điểm:**
- Cache luôn fresh (sync với DB)
- Read performance tốt hơn (ít cache miss)

**Nhược điểm:**
- Write penalty: mỗi write → 2 operations
- Cache churn: data ít dùng cũng bị cache
- New node = missing data (cần kết hợp lazy loading)

##### 3. Kết hợp + TTL (Best Practice)

```python
# Lazy loading + TTL
def get_customer(customer_id):
    data = cache.get(customer_id)
    if data is None:
        data = db.query("SELECT * FROM customers WHERE id = %s", customer_id)
        cache.set(customer_id, data, ttl=300)  # 5 phút
    return data

# Write-through + TTL
def save_customer(customer_id, values):
    db.update("UPDATE customers SET ... WHERE id = %s", customer_id, values)
    cache.set(customer_id, values, ttl=300)
```

#### Caching Techniques cho Relational Data

| Technique | Mô tả | Redis Type |
|-----------|--------|-----------|
| **Cache ResultSet** | Serialize toàn bộ query result | String (binary) |
| **Cache JSON** | Lưu selected fields dạng JSON | String |
| **Cache Hash** | Mỗi field = 1 hash field | Hash |
| **Cache Object** | Serialize application object | String (binary) |

**Key naming convention:** `object:type:id` → `customer:id:1001`

#### Chọn data nào để cache:
- Data truy cập thường xuyên (frequently accessed)
- Data ít thay đổi (relatively static)
- Query expensive (JOINs, aggregations)
- Application chấp nhận data stale trong thời gian ngắn

---

### Use Case 2: Locating Points of Interest (Geospatial)

Redis Geospatial cho phép lưu trữ và query dữ liệu vị trí:

#### Core Commands

```
# Thêm locations
GEOADD locations 106.6297 10.8231 "coffee_shop_1"
GEOADD locations 106.6350 10.8250 "coffee_shop_2"
GEOADD locations 106.7000 10.8000 "restaurant_1"

# Tính khoảng cách
GEODIST locations "coffee_shop_1" "restaurant_1" km
→ "8.5"

# Tìm trong bán kính
GEOSEARCH locations FROMMEMBER "coffee_shop_1" BYRADIUS 5 km ASC
→ 1) "coffee_shop_1"
   2) "coffee_shop_2"

# Tìm từ tọa độ cụ thể
GEOSEARCH locations FROMLONLAT 106.63 10.82 BYRADIUS 2 km COUNT 10 ASC

# Lấy tọa độ
GEOPOS locations "coffee_shop_1"
→ 1) "106.6297"  2) "10.8231"
```

#### Use Cases thực tế:
- **Ride-sharing**: Tìm tài xế gần nhất
- **Food delivery**: Tìm nhà hàng trong bán kính
- **Store locator**: Tìm chi nhánh gần nhất
- **Social**: Tìm bạn bè ở gần

#### Đặc điểm kỹ thuật:
- Stored internally dưới dạng Sorted Set (ZSET) với geohash scores
- Precision: ~0.5% error do geohash encoding
- Hỗ trợ units: m, km, mi, ft
- `BYRADIUS` (vòng tròn) và `BYBOX` (hình chữ nhật)
- Kết hợp `COUNT` và `ASC/DESC` để giới hạn và sắp xếp results

---

### Use Case 3: Real-Time Data Streaming with Analytics

Redis Streams là cấu trúc dữ liệu append-only, phù hợp cho event streaming:

#### Core Concepts

```
┌─────────────────────────────────────────────┐
│                  STREAM                      │
│  ID: timestamp-seq                          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│  │ Msg1 │→│ Msg2 │→│ Msg3 │→│ Msg4 │→...  │
│  └──────┘ └──────┘ └──────┘ └──────┘      │
└─────────────────────────────────────────────┘
        ↑                           ↑
   Consumer Group A            Consumer Group B
   ├── Consumer 1              ├── Consumer X
   └── Consumer 2              └── Consumer Y
```

#### Streams Commands

```
# Produce: thêm message vào stream
XADD sensor:data * temperature 23.5 humidity 65 device_id "sensor_01"
# * = auto-generate ID (timestamp-based)

# Consume: đọc messages
XREAD COUNT 5 BLOCK 2000 STREAMS sensor:data $
# $ = chỉ messages mới từ bây giờ

# Range query (analytics)
XRANGE sensor:data 1609459200000-0 1609545600000-0
# Query messages trong time range

# Consumer Groups (parallel processing)
XGROUP CREATE sensor:data analytics_group $ MKSTREAM
XREADGROUP GROUP analytics_group consumer1 COUNT 10 STREAMS sensor:data >
XACK sensor:data analytics_group <message_id>

# Stream info
XLEN sensor:data                    → total messages
XINFO STREAM sensor:data           → stream metadata
XINFO GROUPS sensor:data           → consumer groups info
```

#### So sánh Redis Streams vs Pub/Sub

| Feature | Streams | Pub/Sub |
|---------|---------|---------|
| Persistence | Có (dữ liệu được lưu) | Không (fire-and-forget) |
| Consumer Groups | Có | Không (trừ Sharded Pub/Sub) |
| Message replay | Có (đọc lại history) | Không |
| Acknowledgment | Có (XACK) | Không |
| Use case | Event sourcing, logging, analytics | Real-time notifications |

#### Real-Time Analytics Pattern:

```
# Producer: IoT sensors gửi data liên tục
XADD iot:readings * sensor "temp_01" value 25.3 ts 1709123456

# Analytics consumer: tính trung bình mỗi phút
XRANGE iot:readings <start> <end>
→ Process → HSET analytics:hourly:temp avg 25.1 max 26.0 min 24.5

# Dashboard consumer: đọc real-time
XREAD BLOCK 0 STREAMS iot:readings $
```

#### Pub/Sub cho Real-Time Messaging:

```
# Subscribe to channel
SUBSCRIBE news.sports.golf

# Publish message
PUBLISH news.sports.golf "Tiger Woods wins Masters"

# Pattern subscribe
PSUBSCRIBE news.sports.*
```

---

### Use Case 4: Online Gaming Leaderboards

Redis Sorted Sets là giải pháp hoàn hảo cho leaderboards:

#### Tại sao Sorted Sets:
- **Uniqueness**: Mỗi member chỉ xuất hiện 1 lần
- **Auto-sorting**: Tự động sắp xếp khi score thay đổi
- **O(log N)**: Thêm/cập nhật/rank lookup đều nhanh
- **Real-time**: Cập nhật tức thì, không cần re-sort

#### Leaderboard Commands

```
# Thêm/cập nhật scores
ZADD leaderboard 1500 "player_alice"
ZADD leaderboard 2300 "player_bob"
ZADD leaderboard 1800 "player_charlie"
ZADD leaderboard 3100 "player_dave"

# Top 10 (high to low)
ZREVRANGE leaderboard 0 9 WITHSCORES
→ 1) "player_dave"    3100
   2) "player_bob"    2300
   3) "player_charlie" 1800
   4) "player_alice"  1500

# Rank của player cụ thể (0-based, high-to-low)
ZREVRANK leaderboard "player_bob"
→ 1  (vị trí thứ 2)

# Score của player
ZSCORE leaderboard "player_alice"
→ "1500"

# Cập nhật score (thay thế hoàn toàn)
ZADD leaderboard 2000 "player_alice"

# Tăng score (increment)
ZINCRBY leaderboard 500 "player_alice"
→ "2500"

# Players trong khoảng score
ZRANGEBYSCORE leaderboard 1000 2000
→ players có score 1000-2000

# Tổng số players
ZCARD leaderboard
→ 4

# Xóa player
ZREM leaderboard "player_alice"
```

#### Advanced Leaderboard Patterns

```
# Multiple leaderboards (daily, weekly, monthly)
ZADD leaderboard:daily:20240101 score player
ZADD leaderboard:weekly:2024W01 score player
ZADD leaderboard:monthly:202401 score player

# Kết hợp nhiều leaderboards
ZUNIONSTORE leaderboard:combined 3 leaderboard:day1 leaderboard:day2 leaderboard:day3

# Leaderboard with expiration (daily reset)
ZADD leaderboard:daily score player
EXPIRE leaderboard:daily 86400  # 24 hours

# Relative ranking (nearby players)
# Tìm rank của player, rồi lấy players xung quanh
rank = ZREVRANK leaderboard "player_alice"
ZREVRANGE leaderboard (rank-5) (rank+5) WITHSCORES
```

#### Recommendations (Hashes + Counters)

```
# Like/Dislike system
INCR item:38923:likes
INCR item:38923:dislikes
HSET item:38923:ratings "Susan" 1     # liked
HSET item:38923:ratings "Tommy" -1    # disliked

# Recommendation score
ZADD recommendations:user1 0.95 "item:100" 0.87 "item:200"
```

---

## Summary: Chọn Data Type theo Use Case

| Use Case | Data Type | Commands chính |
|----------|-----------|---------------|
| **Session cache** | String (with TTL) | SET, GET, EXPIRE |
| **User profile** | Hash | HSET, HGET, HMGET |
| **Activity feed** | List | LPUSH, LRANGE |
| **Tags/categories** | Set | SADD, SINTER, SUNION |
| **Leaderboard** | Sorted Set | ZADD, ZREVRANGE, ZRANK |
| **Location search** | Geospatial | GEOADD, GEOSEARCH |
| **Event streaming** | Stream | XADD, XREAD, XREADGROUP |
| **Real-time messaging** | Pub/Sub | PUBLISH, SUBSCRIBE |
| **Unique counting** | HyperLogLog | PFADD, PFCOUNT |
| **Feature flags** | Bitmap | SETBIT, GETBIT |
| **Complex objects** | JSON | JSON.SET, JSON.GET |
| **Rate limiting** | String + INCR | INCR, EXPIRE |

---

## Performance Tips

1. **Key design**: Dùng naming convention nhất quán (`app:entity:id:field`)
2. **Avoid blocking**: Không dùng `KEYS *`, `HGETALL` trên large data → dùng `SCAN`, `HSCAN`
3. **Pipeline**: Batch multiple commands để giảm round-trips
4. **Connection pooling**: Reuse connections, tránh tạo mới mỗi request
5. **TTL strategy**: Luôn set TTL cho cache data → tránh memory exhaustion
6. **Data size**: Break large items thành smaller keys/fields
7. **Cluster mode**: Enable cho data > single node capacity
8. **Read replicas**: Distribute read load across replicas

---

*Sources: [AWS ElastiCache Documentation](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/), [Database Caching Strategies Using Redis Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/), [Valkey Commands Reference](https://valkey.io/commands/)*
