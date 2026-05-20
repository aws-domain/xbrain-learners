# Data Modeling for Amazon Neptune - Core Knowledge Summary

## Module 1: Data Modeling Basics

### Fundamental Concepts - Basic Graph Constructs

Graph database lưu trữ dữ liệu dưới dạng **nodes** (vertices), **edges** (relationships), và **properties** (key-value pairs).

| Thành phần | Mô tả | Ví dụ |
|-----------|-------|-------|
| **Node/Vertex** | Thực thể trong graph | Person, Product, City |
| **Edge/Relationship** | Kết nối giữa 2 nodes, có hướng (directed) | KNOWS, PURCHASED, LIVES_IN |
| **Property** | Cặp key-value gắn vào node hoặc edge | name: "John", age: 29 |
| **Label** | Phân loại node hoặc edge | :Person, :created |

**Đặc điểm quan trọng:**
- Edges luôn có hướng (from → to) và phải có đúng 1 label
- Nodes có thể có nhiều labels (multi-label)
- Properties có thể multi-valued (set cardinality) trong Neptune

### Graph Databases vs Relational Databases

| Tiêu chí | Relational DB | Graph DB |
|----------|--------------|---------|
| Mô hình | Tables, rows, columns | Nodes, edges, properties |
| Relationships | Foreign keys + JOINs | First-class citizens (edges) |
| Schema | Rigid, predefined | Flexible, schema-optional |
| Truy vấn quan hệ phức tạp | Nhiều JOINs → chậm | Traversal trực tiếp → nhanh |
| Tối ưu cho | Dữ liệu có cấu trúc, ACID transactions | Dữ liệu highly-connected |
| Ví dụ query | SQL với multiple JOINs | Pattern matching, traversal |

**Khi nào dùng Graph DB:**
- Dữ liệu có nhiều mối quan hệ phức tạp, đa chiều
- Cần traverse qua nhiều "hops" (bậc quan hệ)
- Schema thay đổi thường xuyên
- Use cases: fraud detection, recommendation engines, knowledge graphs, social networks, network security, drug discovery

### Importance of Graph Databases

- **Performance**: Truy vấn relationships nhanh hơn relational DB khi dữ liệu highly-connected (milliseconds latency cho billions of relationships)
- **Flexibility**: Thêm nodes, edges, labels mà không cần ALTER TABLE
- **Intuitive**: Mô hình graph gần với cách con người suy nghĩ về relationships
- **Index-free adjacency**: Mỗi node biết trực tiếp neighbors của nó → không cần global index lookups

---

## Module 2: Understanding Graph Models in Neptune

### Graph Models Supported by Neptune

Neptune hỗ trợ 2 mô hình chính:

#### 1. Property Graph (LPG - Labeled Property Graph)
- Query languages: **Gremlin** (imperative) và **openCypher** (declarative)
- Nodes có labels và properties
- Edges có type, direction, và properties
- Cả hai ngôn ngữ hoạt động trên cùng một graph

```
// openCypher example
MATCH (p:Person)-[:KNOWS]->(f:Person)
WHERE p.name = 'Alice'
RETURN f.name

// Gremlin example
g.V().has('Person','name','Alice').out('KNOWS').values('name')
```

#### 2. RDF (Resource Description Framework)
- Query language: **SPARQL**
- Dữ liệu dạng triples (subject-predicate-object) hoặc quads (+ named graph)
- Tuân theo W3C standards
- Phù hợp cho semantic web, linked data, knowledge graphs

```sparql
SELECT ?name WHERE {
  ?person rdf:type :Person .
  ?person :name ?name .
  ?person :knows :Alice .
}
```

#### Gremlin vs openCypher

| Gremlin | openCypher |
|---------|-----------|
| Imperative (step-by-step) | Declarative (pattern-based) |
| Quen thuộc với developers/data scientists | Quen thuộc với SQL users |
| `g.V().has()...out()...` | `MATCH ()-[]->() WHERE ... RETURN` |
| Linh hoạt hơn cho traversal phức tạp | Dễ đọc hơn cho queries đơn giản |

**Lưu ý:** Trong Neptune, bạn KHÔNG cần chọn một — có thể dùng cả Gremlin và openCypher trên cùng graph.

### Neptune Data Model Internals (Quad Model)

Neptune lưu trữ tất cả dữ liệu dưới dạng **quads** (4 positions):

```
Subject (S) | Predicate (P) | Object (O) | Graph (G)
```

| Position | Property Graph (LPG) | RDF |
|----------|---------------------|-----|
| **S** | Source vertex ID / Element ID | Subject URI |
| **P** | Edge label / Property key | Predicate URI |
| **O** | Target vertex ID / Property value | Object URI/Literal |
| **G** | Edge ID (cho edges) / Fixed value | Named Graph URI |

**Ví dụ mapping:**
- Relationship: S=vertex_source, P=edge_label, O=vertex_target, G=edge_id
- Property: S=element_id, P=property_key, O=property_value, G=fixed

### Neptune Indexing (SPOG Model)

Neptune dùng **3 indexes mặc định** để xử lý 16 access patterns:

| Index | Key Order | Tối ưu cho |
|-------|-----------|-----------|
| **SPOG** | Subject + Predicate + Object + Graph | Forward traversal (outgoing edges), vertex lookup |
| **POGS** | Predicate + Object + Graph + Subject | Lookup by edge label/property key |
| **GPSO** | Graph + Predicate + Subject + Object | Graph-scoped queries |

**OSGP Index (Optional - Lab Mode):**
- Index thứ 4, cần enable trước khi load data
- Tối ưu cho reverse traversal (incoming edges), `in()` steps
- Trade-off: insert rate giảm ~23%, storage tăng ~20%
- Nên enable nếu graph có nhiều distinct predicates

**Quan trọng:** Queries follow outgoing edges (SPOG) hiệu quả hơn incoming edges. Nếu không enable OSGP, hãy design model với edges hướng theo chiều query phổ biến nhất.

---

## Module 3: Loading Data & Transforming Data Models

### Loading Data into Neptune

#### 1. Bulk Loader (Recommended cho large datasets)

**Quy trình:**
1. Upload data files lên Amazon S3
2. Tạo IAM Role với Read/List access cho S3 bucket
3. Tạo S3 VPC Endpoint
4. Gọi Neptune Loader API (HTTP request)
5. Neptune assume IAM role để load data từ S3

**Hỗ trợ formats:**
- Property Graph: CSV format (Gremlin)
- RDF: N-Triples, N-Quads, RDF/XML, Turtle

#### 2. Query-based Loading (cho incremental updates)

| Method | Language | Ví dụ |
|--------|----------|-------|
| `neptune.read()` | openCypher | Đọc CSV/Parquet từ S3 trong CALL subquery |
| `LOAD` | SPARQL | Import RDF từ URI vào named graph |
| `g.io().read()` | Gremlin | Đọc GraphML, GraphSON từ S3 |

### Gremlin CSV Format cho Bulk Load

**Vertex file:**
```csv
~id,name:String,age:Int,lang:String,~label
v1,"marko",29,,person
v2,"lop",,,"java",software
```

**Edge file:**
```csv
~id,~from,~to,~label,weight:Double
e1,v1,v2,created,0.4
```

**System columns:**
- Vertex: `~id` (required), `~label` (optional, default: "vertex")
- Edge: `~id` (required), `~from` (required), `~to` (required), `~label` (optional)

**Property types:** Bool, Byte, Short, Int, Long, Float, Double, String, Date, Datetime

**Cardinality:** `single` hoặc `set` (default). Array dùng `type[]`.

### Transforming Relational → Graph Model

**Nguyên tắc chuyển đổi:**

| Relational | Graph |
|-----------|-------|
| Table | Node label |
| Row | Node instance |
| Column | Property |
| Foreign Key | Edge (relationship) |
| Join Table (M:N) | Edge với properties |
| Column with few distinct values | Label hoặc separate node |

**Best practices khi transform:**
1. **Entity tables** → Nodes với label là tên table
2. **Foreign keys** → Edges giữa các nodes
3. **Join/association tables** → Edges (có thể kèm properties)
4. **Promote unique property thành ~id** → lookup nhanh nhất
5. **Composite uniqueness** → Combine values thành ID (e.g., `"123_SEA"`)

---

## Module 4: Advanced Modeling Considerations

### Data Model Optimizations cho Neptune

#### 1. Edge Direction Optimization
- Outgoing traversal nhanh hơn incoming (vì SPOG index)
- Nếu query chính dùng incoming edges → đảo hướng edge
- Ví dụ: `person_A —parent_of→ person_B` → `person_B —child_of→ person_A`
- Hoặc enable OSGP index

#### 2. Property Filtering Optimization
- Neptune tối ưu khi filter trên property có tính selective cao nhất
- Combine multiple properties thành 1 để giảm index lookups:
  ```
  // Chậm: 2 index lookups + join
  WHERE n.first_name='John' AND n.last_name='Doe'
  
  // Nhanh: 1 index lookup
  WHERE n.name='John Doe'
  ```

#### 3. ID Strategy
- Neptune cho phép **user-supplied string IDs** cho vertices và edges
- Lookup by ID là cách nhanh nhất để tìm vertex
- Promote property có unique values lên làm vertex ID

#### 4. Schema Constraints
- Neptune chỉ có duy nhất constraint: **uniqueness of ID**
- Dùng composite ID cho multi-column uniqueness (e.g., `id=123_SEA`)

#### 5. Cardinality Considerations
- **Single cardinality**: Chỉ 1 giá trị, error nếu load thêm (trừ khi dùng `updateSingleCardinalityProperties`)
- **Set cardinality** (default): Cho phép nhiều giá trị trên cùng property
- Edge properties luôn single-valued

### openCypher Query Best Practices

- Dùng **directed edges** thay vì bidirectional trong queries
- Đặt **restrictive filters sớm** trong query
- Dùng **parameterized queries** cho plan caching
- **Specify edge labels** khi có thể (tránh scan tất cả predicates)
- Dùng **UNWIND** để batch inputs thay vì individual statements
- Tránh `COLLECT(DISTINCT())` — dùng alternatives
- Prefer **custom IDs** cho node/relationship

---

## Module 5: ETL Approaches

### Phương pháp ETL cho Neptune

#### 1. Neptune Bulk Loader
- Tối ưu cho initial data load và large batch updates
- Data phải ở S3, format CSV (LPG) hoặc RDF formats
- Nhanh nhất, ít overhead nhất cho large datasets

#### 2. AWS Database Migration Service (DMS)
- Migrate từ relational/NoSQL DB → Neptune
- Dùng **GraphMappingConfig** (JSON cho LPG, R2RML cho RDF)
- Flow: Source DB → DMS → S3 (staging) → Neptune
- Hỗ trợ ongoing replication (CDC)

#### 3. Nodestream (ETL Framework)
- Pipeline-based, YAML configuration
- Hỗ trợ nhiều data sources: CSV, JSON, Parquet, Kafka, Athena, REST APIs
- Features: TTL pipelines, schema migration, IAM auth
- Semantic modeling approach

#### 4. Graph.Build (No-code Platform)
- Collaborative graph design studio
- Transformers: Tạo graph models từ real data
- Writers: Write LPG/RDF models vào Neptune
- Data sources: Aurora, Athena, S3, Amazon MSK
- Hỗ trợ CDC, virtualization, materialization

#### 5. Custom ETL
- Dùng Lambda, Glue, hoặc custom scripts
- Write trực tiếp qua Gremlin/openCypher/SPARQL queries
- Phù hợp cho incremental updates, real-time ingestion

### Online vs Offline Migration

| | Offline | Online |
|---|---------|--------|
| **Downtime** | Có | Không |
| **Complexity** | Thấp | Cao |
| **Approach** | Export → Transform → Bulk Load | CDC stream + Bulk Load + Replay |
| **Use case** | Initial migration | Zero-downtime migration |

---

## Key Architecture Components

```
┌─────────────────────────────────────────┐
│           Neptune DB Cluster            │
├─────────────┬───────────────────────────┤
│ Primary     │  Read Replicas (≤15)      │
│ (Read/Write)│  (Read-only, Multi-AZ)    │
├─────────────┴───────────────────────────┤
│         Cluster Volume (SSD)            │
│    (Auto-replicated across AZs)         │
└─────────────────────────────────────────┘
         ↑                    ↑
    Gremlin/openCypher     SPARQL
    (Property Graph)       (RDF)
```

**High Availability:** >99.99%, Multi-AZ, auto-failover, continuous backup to S3

---

## Quick Reference: Chọn Query Language

| Nếu bạn... | Dùng |
|-------------|------|
| Quen SQL, muốn declarative pattern matching | **openCypher** |
| Muốn control traversal step-by-step | **Gremlin** |
| Làm việc với semantic web, linked data, ontologies | **SPARQL** |
| Cần cả imperative và declarative trên cùng data | **Gremlin + openCypher** |

---

*Sources: [AWS Neptune Documentation](https://docs.aws.amazon.com/neptune/latest/userguide/), [AWS Reference Architectures for Graph Databases](https://github.com/aws-samples/aws-dbs-refarch-graph)*
