# W4 — Thực hành Local (Miễn phí, không cần AWS Bedrock)

> Dùng Gemini Flash (free) + ChromaDB (local) để hiểu toàn bộ concept L1→L4
> Khi làm project thật với nhóm → nhóm dùng Bedrock, bạn đã hiểu cơ chế rồi

---

## Setup môi trường (5 phút)

```bash
# Tạo folder thực hành
mkdir w4-practice && cd w4-practice

# Cài dependencies
pip install chromadb google-generativeai fastapi uvicorn

# Lấy Gemini API key miễn phí
# Vào https://aistudio.google.com → Get API key → tạo key
# Không cần credit card
```

---

## L1 — Simple RAG

**Concept cần hiểu:** query → retrieve chunks → send to LLM → get answer with source

```python
# l1_rag.py
import chromadb
import google.generativeai as genai
import os

genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- Bước 1: Tạo knowledge base (giống Bedrock KB) ---
client = chromadb.Client()
collection = client.create_collection("geekbrain")

# Dùng Conduit docs của bạn làm data thực hành
# Đọc file và index vào ChromaDB
import os
docs = []
ids = []

doc_folder = "../resources/workshops/conduit-aws-networking"
for i, filename in enumerate(os.listdir(doc_folder)):
    if filename.endswith(".md"):
        with open(f"{doc_folder}/{filename}") as f:
            content = f.read()
            docs.append(content[:2000])  # lấy 2000 ký tự đầu
            ids.append(f"doc_{i}")

collection.add(documents=docs, ids=ids)
print(f"Indexed {len(docs)} documents")

# --- Bước 2: Retrieve (giống Bedrock Retrieve API) ---
def retrieve(question: str, k: int = 3):
    results = collection.query(query_texts=[question], n_results=k)
    chunks = results["documents"][0]
    return chunks

# --- Bước 3: Generate (giống gọi Claude) ---
model = genai.GenerativeModel("gemini-1.5-flash")

def ask(question: str):
    chunks = retrieve(question)
    context = "\n\n".join(chunks)

    prompt = f"""Answer the question using ONLY the provided context.
Always cite which document the answer came from.
If the context does not contain the answer, say 'I don't have enough information.'

Context:
{context}

Question: {question}"""

    response = model.generate_content(prompt)
    return response.text

# Test L1
print(ask("What port does the backend use?"))
print(ask("Why is the database in an isolated subnet?"))
```

**Chạy thử:**
```bash
python l1_rag.py
```

---

## L2 — Multi-Source + Conflict Resolution

**Concept cần hiểu:** retrieve nhiều chunks hơn, system prompt xử lý conflict

```python
# l2_advanced_rag.py
# (thêm vào l1_rag.py)

def ask_advanced(question: str):
    # Tăng K lên 8 để lấy nhiều chunks hơn
    chunks = retrieve(question, k=8)
    context = "\n\n".join(chunks)

    prompt = f"""Answer the question using the provided context.
When multiple documents provide different information:
- Check if one is marked as 'archived' or 'superseded' — prefer the current version
- If you cannot determine which is correct, state both values and explain the discrepancy

Context:
{context}

Question: {question}"""

    response = model.generate_content(prompt)
    return response.text

# Test conflict resolution
# Tạo 2 docs conflict để test
collection2 = client.create_collection("conflict_test")
collection2.add(
    documents=[
        "API rate limit is 500 requests/minute (archived, v1)",
        "API rate limit is 1000 requests/minute (current, v2 - updated March 2026)"
    ],
    ids=["v1", "v2"]
)

# Verify system chọn đúng version
results = collection2.query(query_texts=["What is the API rate limit?"], n_results=2)
print("Retrieved:", results["documents"])
```

---

## L3 — Tool Calling

**Concept cần hiểu:** LLM đọc tool description → tự quyết định gọi → execute → trả kết quả

```python
# l3_tools.py
import google.generativeai as genai
import sqlite3
import json
import requests

genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- Setup database giả (giống GeekBrain database) ---
conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE monthly_costs (
    service TEXT, month TEXT, total_cost REAL
)""")
conn.executemany("INSERT INTO monthly_costs VALUES (?, ?, ?)", [
    ("PaymentGW", "2026-01", 4500),
    ("PaymentGW", "2026-02", 4500),
    ("PaymentGW", "2026-03", 7500),
    ("NotificationSvc", "2026-01", 1200),
    ("NotificationSvc", "2026-02", 1200),
    ("NotificationSvc", "2026-03", 1800),
])
conn.commit()

conn.execute("""CREATE TABLE sla_targets (
    service TEXT, metric TEXT, target_value REAL
)""")
conn.executemany("INSERT INTO sla_targets VALUES (?, ?, ?)", [
    ("PaymentGW", "latency_p99_ms", 200),
    ("NotificationSvc", "latency_p99_ms", 2000),
    ("NotificationSvc", "error_rate_percent", 1.0),
])
conn.commit()

# --- Monitoring API giả (giống GeekBrain monitoring API) ---
# Chạy file này trước: uvicorn mock_api:app --port 8000
MOCK_METRICS = {
    "PaymentGW": {"latency_p99_ms": 185, "error_rate_percent": 0.3, "requests_per_min": 450},
    "NotificationSvc": {"latency_p99_ms": 3200, "error_rate_percent": 2.1, "requests_per_min": 120},
}

# --- Tool functions ---
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the database.
    Tables: monthly_costs(service, month, total_cost), sla_targets(service, metric, target_value).
    Use for HISTORICAL data: costs, SLA targets. NOT for current/live metrics."""
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        return json.dumps(result)
    except Exception as e:
        return f"Error: {e}"

def get_service_metrics(service_name: str) -> str:
    """Get CURRENT live performance metrics for a service.
    Returns: p99 latency (ms), error rate (%), requests per minute.
    Use for CURRENT/LIVE data only. For historical data, use query_database."""
    metrics = MOCK_METRICS.get(service_name)
    if not metrics:
        return f"Service {service_name} not found"
    return json.dumps({"service": service_name, **metrics})

# --- Tool calling loop (manual — giống raw function calling) ---
model = genai.GenerativeModel("gemini-1.5-flash")

TOOLS = {
    "query_database": query_database,
    "get_service_metrics": get_service_metrics,
}

TOOL_DEFINITIONS = [
    {
        "function_declarations": [
            {
                "name": "query_database",
                "description": "Execute SQL query. Use for historical costs, SLA targets.",
                "parameters": {
                    "type": "object",
                    "properties": {"sql": {"type": "string"}},
                    "required": ["sql"]
                }
            },
            {
                "name": "get_service_metrics",
                "description": "Get current live metrics for a service.",
                "parameters": {
                    "type": "object",
                    "properties": {"service_name": {"type": "string"}},
                    "required": ["service_name"]
                }
            }
        ]
    }
]

def ask_with_tools(question: str):
    print(f"\nQuestion: {question}")

    response = model.generate_content(
        question,
        tools=TOOL_DEFINITIONS
    )

    # Kiểm tra LLM có muốn gọi tool không
    part = response.candidates[0].content.parts[0]

    if hasattr(part, "function_call") and part.function_call.name:
        tool_name = part.function_call.name
        tool_args = dict(part.function_call.args)
        print(f"  → LLM calls tool: {tool_name}({tool_args})")

        # Execute tool
        tool_result = TOOLS[tool_name](**tool_args)
        print(f"  → Tool result: {tool_result}")

        # Gửi kết quả lại cho LLM
        final = model.generate_content([
            question,
            response.candidates[0].content,
            genai.protos.Content(
                parts=[genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                )],
                role="function"
            )
        ])
        print(f"  → Answer: {final.text}")
    else:
        print(f"  → Answer (no tool): {part.text}")

# Test L3
ask_with_tools("What was PaymentGW's total cost in Q1 2026?")
ask_with_tools("What is NotificationSvc's current p99 latency?")
ask_with_tools("Is NotificationSvc meeting its SLA targets?")
```

**Chạy thử:**
```bash
python l3_tools.py
```

---

## L4 — Memory / Multi-turn

**Concept cần hiểu:** giữ history → LLM resolve pronoun từ lượt trước

```python
# l4_memory.py
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Buffer memory — đơn giản nhất
conversation_history = []

def chat(user_message: str):
    conversation_history.append({
        "role": "user",
        "parts": [user_message]
    })

    # Gửi 10 messages gần nhất (5 lượt)
    recent = conversation_history[-10:]
    response = model.generate_content(recent)

    conversation_history.append({
        "role": "model",
        "parts": [response.text]
    })

    print(f"User: {user_message}")
    print(f"AI:   {response.text}\n")
    return response.text

# Test multi-turn — xem AI có resolve pronoun không
chat("Which service had the highest cost in March 2026? PaymentGW at $7500 or NotificationSvc at $1800?")
chat("Why did its costs spike?")           # "its" = PaymentGW
chat("Which team is responsible for it?")  # "it" = PaymentGW
chat("Is that team meeting their SLA?")    # "that team" = Team Platform
```

---

## Mapping chi tiết: Local → AWS Bedrock

> Source: [AWS Docs — Retrieve API](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve.html) và [Tool Use — Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)

---

### L1/L2 — RAG: ChromaDB vs Bedrock Knowledge Bases

**Local (ChromaDB):**
```python
# Index documents
collection.add(documents=["doc content..."], ids=["doc1"])

# Retrieve
results = collection.query(query_texts=["question"], n_results=5)
chunks = results["documents"][0]  # list of strings
```

**AWS Bedrock — 2 cách:**

**Cách 1: `Retrieve` API** — trả về raw chunks, bạn tự build prompt (giống local nhất)
```python
import boto3

# Client khác với bedrock-runtime — dùng bedrock-agent-runtime
client = boto3.client("bedrock-agent-runtime", region_name="ap-southeast-1")

response = client.retrieve(
    knowledgeBaseId="YOUR_KB_ID",       # lấy từ Bedrock console
    retrievalQuery={"text": "Who leads Team Platform?"},
    retrievalConfiguration={
        "vectorSearchConfiguration": {
            "numberOfResults": 5        # tương đương n_results=5
        }
    }
)

# Kết quả trả về
chunks = [r["content"]["text"] for r in response["retrievalResults"]]
# Mỗi result còn có: r["score"], r["location"]["s3Location"]["uri"]
```

**Cách 2: `RetrieveAndGenerate` API** — AWS tự lo cả retrieve + gọi LLM + cite source
```python
response = client.retrieve_and_generate(
    input={"text": "Who leads Team Platform?"},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": "YOUR_KB_ID",
            "modelArn": "arn:aws:bedrock:ap-southeast-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
        }
    }
)

answer = response["output"]["text"]
citations = response["citations"]  # source docs tự động
```

**Khác nhau chính:**

| | ChromaDB local | Bedrock `Retrieve` | Bedrock `RetrieveAndGenerate` |
|---|---|---|---|
| Embedding model | ChromaDB tự chọn | Amazon Titan Embeddings v2 | Amazon Titan Embeddings v2 |
| Vector store | In-memory | OpenSearch Serverless | OpenSearch Serverless |
| Bạn tự build prompt | Có | Có | Không — AWS lo |
| Control system prompt | Có | Có | Giới hạn |
| Boto3 client | N/A | `bedrock-agent-runtime` | `bedrock-agent-runtime` |
| Dùng khi | Học/local | L1/L2 project | Demo nhanh |

---

### L3 — Tool Calling: Gemini vs Bedrock Converse API

**Local (Gemini):**
```python
response = model.generate_content(question, tools=TOOL_DEFINITIONS)
part = response.candidates[0].content.parts[0]
if hasattr(part, "function_call"):
    tool_name = part.function_call.name
    tool_args = dict(part.function_call.args)
```

**AWS Bedrock — Converse API** (từ AWS Docs):
```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-1")

# Định nghĩa tools — cấu trúc khác Gemini
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "query_database",
                "description": "Execute SQL query. Use for HISTORICAL costs, SLA targets.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "sql": {"type": "string", "description": "SQL query to execute"}
                        },
                        "required": ["sql"]
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "get_service_metrics",
                "description": "Get CURRENT live metrics for a service. NOT for historical data.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "service_name": {"type": "string"}
                        },
                        "required": ["service_name"]
                    }
                }
            }
        }
    ]
}

def ask_with_tools_bedrock(question: str):
    messages = [{"role": "user", "content": [{"text": question}]}]

    # Lần 1: gửi câu hỏi + tool definitions
    response = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=messages,
        toolConfig=tool_config
    )

    output_message = response["output"]["message"]
    messages.append(output_message)

    # Kiểm tra model có muốn gọi tool không
    if response["stopReason"] == "tool_use":
        tool_results = []

        for block in output_message["content"]:
            if "toolUse" in block:
                tool = block["toolUse"]
                tool_name = tool["name"]
                tool_input = tool["input"]

                print(f"  → Bedrock calls tool: {tool_name}({tool_input})")

                # Execute tool
                result = TOOLS[tool_name](**tool_input)
                print(f"  → Tool result: {result}")

                tool_results.append({
                    "toolResult": {
                        "toolUseId": tool["toolUseId"],
                        "content": [{"json": {"result": result}}]
                    }
                })

        # Lần 2: gửi tool result lại cho model
        messages.append({"role": "user", "content": tool_results})

        final = bedrock.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=messages,
            toolConfig=tool_config
        )

        return final["output"]["message"]["content"][0]["text"]

    return output_message["content"][0]["text"]
```

**Khác nhau chính:**

| | Gemini (local) | Bedrock Converse API |
|---|---|---|
| Boto3 client | N/A | `bedrock-runtime` |
| Tool definition key | `function_declarations` | `toolSpec` |
| Schema key | `parameters` | `inputSchema.json` |
| Detect tool call | `hasattr(part, "function_call")` | `response["stopReason"] == "tool_use"` |
| Tool result format | `FunctionResponse` object | `{"toolResult": {"toolUseId": ..., "content": [...]}}` |
| Model ID format | `"gemini-1.5-flash"` | `"anthropic.claude-3-haiku-20240307-v1:0"` |

---

### L4 — Memory: Python list vs DynamoDB

**Local:**
```python
conversation_history = []  # in-memory, mất khi restart
```

**AWS Bedrock production pattern:**
```python
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("conversation_history")

def save_turn(session_id: str, turn_number: int, role: str, content: str):
    table.put_item(Item={
        "session_id": session_id,   # Partition Key
        "turn_number": turn_number, # Sort Key
        "role": role,
        "content": content
    })

def get_history(session_id: str, last_n: int = 10):
    response = table.query(
        KeyConditionExpression="session_id = :sid",
        ExpressionAttributeValues={":sid": session_id},
        ScanIndexForward=False,  # newest first
        Limit=last_n
    )
    return list(reversed(response["Items"]))
```

---

### Boto3 clients cần biết

Bedrock có **3 client khác nhau** — hay bị nhầm:

| Client | Dùng cho |
|---|---|
| `boto3.client("bedrock")` | Quản lý: list models, get model info |
| `boto3.client("bedrock-runtime")` | Gọi LLM: `converse()`, `invoke_model()` |
| `boto3.client("bedrock-agent-runtime")` | Query KB: `retrieve()`, `retrieve_and_generate()` |

---

### Khi làm project thật với nhóm — chỉ cần đổi

```python
# LOCAL                              # BEDROCK
collection.query(...)           →    client.retrieve(knowledgeBaseId=..., ...)
model.generate_content(...)     →    bedrock.converse(modelId=..., messages=...)
MOCK_METRICS[service]           →    requests.get(f"http://localhost:8000/metrics/{service}")
conversation_history = []       →    DynamoDB table với session_id + turn_number
```

Logic xử lý tool call, memory window, conflict resolution — **giữ nguyên hoàn toàn**.

---

## Thứ tự thực hành ngày mai

1. Setup + chạy được L1 (~30 phút)
2. Test conflict resolution L2 (~20 phút)
3. Chạy L3 tool calling, xem log LLM gọi tool gì (~45 phút)
4. Test L4 multi-turn conversation (~20 phút)
5. Đọc 36 docs GeekBrain khi data package về (~1 tiếng)
