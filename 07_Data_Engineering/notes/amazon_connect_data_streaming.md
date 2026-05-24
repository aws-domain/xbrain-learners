# Amazon Connect Data Streaming - Core Knowledge Summary

## Module 1: Introduction to Amazon Connect Data Streaming

### Amazon Connect Overview

Amazon Connect là cloud-based **contact center service** cho phép:
- Xử lý voice calls, chat, email, tasks
- Routing contacts tới agents thông minh
- Real-time và historical metrics/reporting
- Tích hợp với AWS services ecosystem

### Data Streaming trong Amazon Connect

Amazon Connect sinh ra **3 loại data streams chính**:

```
┌──────────────────────────────────────────────────────────────────┐
│                      Amazon Connect Instance                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │ Contact Records │  │  Agent Events    │  │ Contact Events │  │
│  │ (CTRs)          │  │                  │  │                │  │
│  └───────┬─────────┘  └────────┬─────────┘  └───────┬────────┘  │
│          │                     │                     │           │
└──────────┼─────────────────────┼─────────────────────┼───────────┘
           │                     │                     │
           ↓                     ↓                     ↓
  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
  │ Kinesis Data    │  │ Kinesis Data    │  │ Amazon EventBridge  │
  │ Streams/Firehose│  │ Streams         │  │ (default event bus) │
  └─────────────────┘  └─────────────────┘  └─────────────────────┘
```

### 3 Data Stream Types

| Stream Type | Nội dung | Destination | Timing |
|-------------|----------|-------------|--------|
| **Contact Records (CTRs)** | Chi tiết về mỗi contact (duration, queue, agent, attributes) | Kinesis Data Streams hoặc Kinesis Firehose | Sau khi contact kết thúc (ACW complete) |
| **Agent Event Streams** | Agent activity (login, logout, status changes, contact states) | Kinesis Data Streams | Near real-time |
| **Contact Events** | Contact lifecycle events (initiated, queued, connected, disconnected) | Amazon EventBridge | Real-time |

### Bổ sung: Media Streams

| Stream Type | Nội dung | Destination |
|-------------|----------|-------------|
| **Live Media Streaming** | Customer audio (voice) real-time | Kinesis Video Streams |
| **Chat Message Streaming** | Real-time chat messages | Amazon SNS |

---

## Module 2: Data Streaming Design Considerations

### 2.1 Contact Records (CTRs)

#### Cấu trúc CTR

Mỗi CTR chứa thông tin chi tiết về một contact segment:

```json
{
    "AWSAccountId": "123456789012",
    "ContactId": "497f04ca-6de1-408f-9b8a-ec57bcc99b31",
    "InitialContactId": null,
    "PreviousContactId": null,
    "NextContactId": "6aa058d3-e771-4544-8e93-f5ce9c9003b3",
    "Channel": "VOICE",
    "InitiationMethod": "INBOUND",
    "Agent": {
        "ARN": "arn:aws:connect:...",
        "Username": "Agent1",
        "AfterContactWorkStartTimestamp": "2024-08-02T17:50:53Z",
        "ConnectedToAgentTimestamp": "2024-08-02T17:45:21Z"
    },
    "Queue": {
        "ARN": "arn:aws:connect:.../queue/...",
        "Name": "BasicQueue",
        "EnqueueTimestamp": "2024-08-02T17:44:10Z",
        "DequeueTimestamp": "2024-08-02T17:45:21Z"
    },
    "Attributes": {
        "customAttribute1": "value1"
    }
}
```

#### Key CTR Fields

| Field | Mô tả |
|-------|--------|
| **ContactId** | Unique ID cho contact segment này |
| **InitialContactId** | ID của contact đầu tiên trong chain (null nếu là first) |
| **PreviousContactId** | ID của contact trước đó (cho transfers) |
| **NextContactId** | ID của contact tiếp theo (cho transfers) |
| **Channel** | VOICE, CHAT, TASK, EMAIL |
| **InitiationMethod** | INBOUND, OUTBOUND, TRANSFER, CALLBACK, API, QUEUE_TRANSFER |
| **Agent** | Thông tin agent handle contact |
| **Queue** | Queue mà contact đi qua |
| **Attributes** | User-defined + system attributes |
| **DisconnectTimestamp** | Thời điểm disconnect |
| **ConnectedToSystemTimestamp** | Thời điểm connect vào hệ thống |

#### Contact Chains và Linking

```
Customer calls → Agent1 → Transfer → Agent2 → Transfer → Agent3

Contact Record 1 (Agent1):
  ContactId: "AAA"
  InitialContactId: null
  NextContactId: "BBB"

Contact Record 2 (Agent2):
  ContactId: "BBB"
  InitialContactId: "AAA"
  PreviousContactId: "AAA"
  NextContactId: "CCC"

Contact Record 3 (Agent3):
  ContactId: "CCC"
  InitialContactId: "AAA"
  PreviousContactId: "BBB"
  NextContactId: null
```

#### Xác định loại cuộc gọi từ CTR

| Loại | Logic xác định |
|------|---------------|
| **Simple call** | NextContactId = null, no consult leg |
| **Consult** | Consulted agent ACW starts AFTER initiating agent ACW |
| **Transfer** | Initiating agent ACW starts BEFORE consulted agent ACW |
| **Conference** | Consulted agent connected to customer (3-way) |

#### CTR Retention
- Có sẵn trong instance: **24 tháng**
- Dùng streaming để lưu trữ lâu dài hơn và advanced analytics

### 2.2 Agent Event Streams

#### Events captured:

| Event | Mô tả |
|-------|--------|
| **Agent Login** | Agent đăng nhập CCP |
| **Agent Logout** | Agent đăng xuất |
| **Status Change** | Chuyển trạng thái (Available, Break, Training, Offline, custom) |
| **Contact Connected** | Agent nhận contact |
| **Contact State Change** | Contact state thay đổi |

#### Contact States trong Agent Event Stream:

| State | Mô tả |
|-------|--------|
| `INCOMING` | Callback đang được offer |
| `PENDING` | Callback pending |
| `CONNECTING` | Inbound contact đang ringing cho agent |
| `CONNECTED` | Agent đã accept, đang conversation |
| `CONNECTED_ONHOLD` | Customer đang on hold |
| `PAUSED` | Task contact bị pause |
| `MISSED` | Agent missed contact |
| `ERROR` | Lỗi (ví dụ: customer abandon during whisper) |
| `ENDED` | Conversation kết thúc, agent bắt đầu ACW |
| `REJECTED` | Agent reject hoặc customer abandon khi connecting |

#### Sample Agent Event Stream:

```json
{
    "AgentARN": "arn:aws:connect:us-east-1:012345678901:instance/.../agent/...",
    "CurrentAgentSnapshot": {
        "AgentStatus": {
            "Name": "Available",
            "Type": "ROUTABLE"
        },
        "Contacts": [
            {
                "Channel": "VOICE",
                "ContactId": "ContactId-1",
                "InitiationMethod": "OUTBOUND",
                "State": "CONNECTED",
                "StateStartTimestamp": "2019-05-25T18:55:21.011Z",
                "ConnectedToAgentTimestamp": "2019-05-25T18:55:21.011Z",
                "Queue": {
                    "ARN": "arn:aws:connect:.../queue/..."
                }
            }
        ]
    },
    "EventTimestamp": "2019-05-25T18:55:21.011Z",
    "EventType": "STATE_CHANGE"
}
```

### 2.3 Contact Events (EventBridge)

Amazon Connect phát events tới EventBridge default event bus:

| Event Type | Mô tả |
|-----------|--------|
| **Contact events** | Voice, chat, task lifecycle events |
| **Rule events** | Contact Lens rules triggered |
| **Performance evaluation events** | Automated evaluation status |
| **Screen recording events** | Agent screen recording status |
| **Voice ID events** | Enrollment, authentication, fraud detection |

### 2.4 Design Considerations

#### Chọn Kinesis Data Streams vs Kinesis Firehose

| Tiêu chí | Kinesis Data Streams | Kinesis Firehose |
|----------|---------------------|-----------------|
| **Use case** | Real-time processing, custom consumers | Simple delivery to S3/Redshift/OpenSearch |
| **Latency** | ~200ms (real-time) | 60s-900s buffer interval |
| **Processing** | Custom (Lambda, KCL app) | Built-in transformation |
| **Scaling** | Manual (shard management) | Auto-scaling |
| **Cost model** | Per shard hour + per PUT | Per GB processed |
| **Retention** | 24h - 365 days | No retention (delivery only) |

**Recommendations:**
- **Contact Records → Kinesis Firehose** nếu chỉ cần lưu trữ và analytics (S3 → Athena/Redshift)
- **Contact Records → Kinesis Data Streams** nếu cần real-time processing
- **Agent Events → Kinesis Data Streams** (luôn yêu cầu KDS, không hỗ trợ Firehose trực tiếp)

#### Encryption Considerations

- Hỗ trợ **server-side encryption** với customer managed KMS key
- Service-linked role cần quyền `kms:GenerateDataKey`
- Cần update KMS key policy TRƯỚC khi enable streaming (tránh data loss)

```json
{
    "Sid": "Allow Amazon Connect streaming",
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT:role/aws-service-role/connect.amazonaws.com/..."
    },
    "Action": "kms:GenerateDataKey",
    "Resource": "*"
}
```

#### Capacity Planning

| Metric | Guideline |
|--------|-----------|
| **CTR size** | ~4-10 KB per record (varies with attributes) |
| **Agent events** | ~2-5 KB per event |
| **Shard capacity** | 1 MB/s write, 2 MB/s read per shard |
| **Estimation** | (contacts/hour × avg_size) / 3600 / 1MB = min shards |

---

## Module 3: Processing Amazon Connect Data Streams

### 3.1 Architecture Patterns

#### Pattern 1: CTRs → S3 → Analytics (Simple)

```
Amazon Connect → Kinesis Firehose → S3 → Athena/QuickSight
```

**Use case:** Historical analytics, compliance storage, BI dashboards

#### Pattern 2: Real-time Processing (Lambda)

```
Amazon Connect → Kinesis Data Streams → Lambda → DynamoDB/SNS/Custom
```

**Use case:** Real-time alerts, live dashboards, CRM integration

#### Pattern 3: Complex Analytics Pipeline

```
Amazon Connect → Kinesis Data Streams → Kinesis Firehose → S3
                                      ↓
                               Lambda (transform)
                                      ↓
                            OpenSearch / Redshift
```

**Use case:** Full-text search, complex aggregations, ML

#### Pattern 4: Agent Monitoring Dashboard

```
Agent Events → Kinesis Data Streams → Lambda → DynamoDB (state table)
                                              → CloudWatch (metrics)
                                              → SNS (alerts)
```

**Use case:** Real-time agent monitoring, WFM integration, ACW tracking

#### Pattern 5: EventBridge Rules

```
Contact Events → EventBridge → Rule (filter) → Lambda/SNS/SQS/Step Functions
```

**Use case:** Contact lifecycle automation, notification triggers

### 3.2 Processing với Lambda

```python
import json
import base64

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis records are base64 encoded
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        
        # Process CTR
        if 'ContactId' in data:
            contact_id = data['ContactId']
            channel = data.get('Channel')
            agent = data.get('Agent', {}).get('Username')
            queue_time = calculate_queue_time(data)
            # Store, alert, or forward...
        
        # Process Agent Event
        if 'EventType' in data:
            agent_arn = data['AgentARN']
            event_type = data['EventType']
            status = data['CurrentAgentSnapshot']['AgentStatus']['Name']
            # Update dashboard, trigger alerts...
```

### 3.3 Tính ACW (After Contact Work) Time

Từ Agent Event Stream, tính ACW time:

```
ACW Duration = Agent Status Change Timestamp (to Available/next status)
             - Contact ENDED StateStartTimestamp
```

Hoặc từ CTR:
```
ACW Duration = AfterContactWorkEndTimestamp - AfterContactWorkStartTimestamp
```

### 3.4 Processing với Kinesis Data Analytics (Real-time SQL)

```sql
-- Real-time average queue wait time
CREATE OR REPLACE STREAM "QUEUE_METRICS" (
    queue_name VARCHAR(256),
    avg_wait_time DOUBLE,
    contact_count INTEGER
);

CREATE OR REPLACE PUMP "QUEUE_PUMP" AS
INSERT INTO "QUEUE_METRICS"
SELECT STREAM
    queue_name,
    AVG(DATEDIFF(second, enqueue_time, dequeue_time)) as avg_wait_time,
    COUNT(*) as contact_count
FROM "SOURCE_STREAM"
GROUP BY queue_name, STEP("SOURCE_STREAM".ROWTIME BY INTERVAL '1' MINUTE);
```

### 3.5 Storing và Querying với Athena

```sql
-- Create table cho CTRs stored in S3
CREATE EXTERNAL TABLE connect_ctrs (
    ContactId string,
    Channel string,
    InitiationMethod string,
    AgentUsername string,
    QueueName string,
    ConnectedToSystemTimestamp string,
    DisconnectTimestamp string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://my-bucket/connect-ctrs/';

-- Query: Average handle time by queue
SELECT 
    QueueName,
    AVG(date_diff('second', 
        from_iso8601_timestamp(ConnectedToSystemTimestamp),
        from_iso8601_timestamp(DisconnectTimestamp)
    )) as avg_handle_time_sec
FROM connect_ctrs
WHERE Channel = 'VOICE'
GROUP BY QueueName;
```

### 3.6 EventBridge Rule Examples

```json
{
    "source": ["aws.connect"],
    "detail-type": ["Amazon Connect Contact Event"],
    "detail": {
        "eventType": ["DISCONNECTED"],
        "channel": ["VOICE"]
    }
}
```

---

## 4. Use Cases cho Data Streaming

| Use Case | Data Source | Processing | Output |
|----------|-----------|-----------|--------|
| **Real-time agent dashboard** | Agent Events | Lambda → DynamoDB | Web dashboard |
| **Abandoned call alerts** | Contact Events (EventBridge) | EventBridge Rule → SNS | Email/SMS alert |
| **Long queue wait notification** | Contact Events | Lambda (check threshold) | SNS notification |
| **Historical reporting** | CTRs | Firehose → S3 → Athena | QuickSight dashboard |
| **CRM integration** | CTRs | Lambda → API call | Salesforce/custom CRM |
| **WFM integration** | Agent Events | KCL consumer | WFM system update |
| **Compliance archival** | CTRs | Firehose → S3 (Glacier) | Long-term storage |
| **Sentiment analysis** | CTRs + Contact Lens | Lambda → Comprehend | Analytics dashboard |
| **Callback tracking** | CTRs (InitiationMethod=CALLBACK) | Lambda | Callback metrics |

---

## 5. Enable Data Streaming (Steps)

### Qua Console:
1. Amazon Connect Console → chọn instance
2. Navigation: **Data streaming**
3. Enable data streaming
4. **Contact records**: chọn Kinesis Firehose hoặc Kinesis Stream
5. **Agent events**: chọn Kinesis Stream
6. Save

### Prerequisites:
- Kinesis stream/Firehose delivery stream phải tồn tại sẵn
- Cùng AWS Region với Connect instance
- KMS key policy (nếu dùng encryption)
- Service-linked role permissions

---

## 6. Best Practices

1. **Dùng Firehose cho CTRs** khi chỉ cần batch analytics → đơn giản, auto-scaling, tự delivery S3
2. **Dùng KDS cho Agent Events** khi cần near real-time processing
3. **Monitor shard utilization** — scale up khi > 70% capacity
4. **Idempotent processing** — Kinesis có thể deliver duplicate records
5. **Error handling** — DLQ (Dead Letter Queue) cho failed processing
6. **Partition key** — Amazon Connect dùng ContactId làm partition key
7. **Data retention** — Set Kinesis retention phù hợp (default 24h, max 365 days)
8. **Compress data** trong Firehose (GZIP/Snappy) để giảm storage cost
9. **Use EventBridge** cho event-driven workflows (không cần poll)
10. **Encrypt at rest và in transit** — Enable KMS encryption cho streams

---

## Quick Reference

```
Contact Center Event Flow:
                                                    
Customer Call → IVR/Flow → Queue → Agent → ACW → Complete
     │              │        │       │      │        │
     └──Contact─────┼────────┼───────┼──────┼────────┘
        Event       │        │       │      │    Contact Record
     (EventBridge)  │        │       │      │    (CTR → Kinesis)
                    │        │       │      │
                    └── Agent Event Stream ──┘
                        (Kinesis Data Streams)
                    Login/Logout/Status/ContactState
```

---

*Sources: [Amazon Connect Administrator Guide](https://docs.aws.amazon.com/connect/latest/adminguide/), [Amazon Connect API Reference](https://docs.aws.amazon.com/connect/latest/APIReference/)*
