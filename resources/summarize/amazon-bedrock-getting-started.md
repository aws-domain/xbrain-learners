# Amazon Bedrock - Kiến Thức Cốt Lõi

## Tổng Quan về Amazon Bedrock

Amazon Bedrock là dịch vụ được quản lý hoàn toàn (fully managed service) cung cấp quyền truy cập an toàn, cấp doanh nghiệp vào các foundation models (mô hình nền tảng) hiệu suất cao từ các công ty AI hàng đầu, cho phép bạn xây dựng và mở rộng các ứng dụng AI tạo sinh (generative AI).

### Đặc Điểm Chính
- **Fully Managed**: AWS quản lý toàn bộ hạ tầng
- **Enterprise-Grade Security**: Bảo mật cấp doanh nghiệp
- **Multiple Model Providers**: Hỗ trợ 100+ foundation models từ nhiều nhà cung cấp
- **Flexible APIs**: Nhiều API khác nhau để tích hợp

---

## 1. Foundation Models (Mô Hình Nền Tảng)

### Các Nhà Cung Cấp Mô Hình Chính

#### Amazon Nova 2
- Mô hình mới nhất của Amazon
- Hỗ trợ đa phương thức (multimodal)
- Tối ưu cho các tác vụ text và image

#### Anthropic Claude
- **Claude Opus 4.7**: Mô hình mạnh nhất, phù hợp cho agentic coding, công việc chuyên nghiệp
- **Claude Opus 4.6**: Phiên bản trước, vẫn rất mạnh mẽ
- **Claude Sonnet 4.6**: Cân bằng giữa hiệu suất và chi phí
- **Claude Haiku**: Nhanh và tiết kiệm chi phí
- **Claude Mythos Preview**: Mô hình tiên tiến nhất (gated preview) cho cybersecurity, coding, reasoning

#### OpenAI
- **GPT-OSS-120B**: Mô hình open-source scale lớn
- **GPT-OSS-20B**: Phiên bản nhỏ hơn

#### Các Nhà Cung Cấp Khác
- **DeepSeek 3.2**: Mô hình từ DeepSeek
- **Kimi K2.5**: Từ Moonshot AI
- **MiniMax M2.1**: Từ MiniMax
- **Writer AI Palmyra**: Cho enterprise workflows

### Cách Lấy Thông Tin về Models
```python
# Sử dụng ListFoundationModels API
import boto3

client = boto3.client('bedrock')
response = client.list_foundation_models()

# Lấy thông tin chi tiết về một model cụ thể
model_info = client.get_foundation_model(
    modelIdentifier='anthropic.claude-opus-4-7'
)
```

---

## 2. APIs và Cách Gọi Models

### 2.1 Messages API (Anthropic SDK)
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="anthropic.claude-opus-4-7",
    max_tokens=1024,
    messages=[{
        "role": "user", 
        "content": "Can you explain the features of Amazon Bedrock?"
    }]
)
print(response)
```

### 2.2 Converse API (AWS SDK - Khuyến Nghị)
```python
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.converse(
    modelId='anthropic.claude-opus-4-7',
    messages=[
        {
            'role': 'user',
            'content': [{'text': 'Can you explain the features of Amazon Bedrock?'}]
        }
    ]
)
print(response)
```

**Ưu điểm Converse API:**
- API thống nhất cho tất cả models
- Dễ chuyển đổi giữa các models
- Hỗ trợ streaming
- Tích hợp tốt với các tính năng AWS khác

### 2.3 Invoke API (Low-level)
```python
import json
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.invoke_model(
    modelId='anthropic.claude-opus-4-7',
    body=json.dumps({
        'anthropic_version': 'bedrock-2023-05-31',
        'messages': [{
            'role': 'user', 
            'content': 'Can you explain the features of Amazon Bedrock?'
        }],
        'max_tokens': 1024
    })
)

result = json.loads(response['body'].read())
print(result)
```

### 2.4 Chat Completions API (OpenAI Compatible)
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="openai.gpt-oss-120b",
    messages=[{
        "role": "user", 
        "content": "Can you explain the features of Amazon Bedrock?"
    }]
)
print(response)
```

---

## 3. Amazon Bedrock Agents

### Khái Niệm
Agents là các ứng dụng AI có khả năng:
- Thực hiện các tác vụ phức tạp tự động
- Gọi APIs và thực thi actions
- Sử dụng tools và knowledge bases
- Ra quyết định dựa trên context

### Thành Phần Chính của Agent
1. **Foundation Model**: Mô hình AI cơ bản
2. **Instructions**: Hướng dẫn cho agent
3. **Action Groups**: Các hành động agent có thể thực hiện
4. **Knowledge Bases**: Nguồn kiến thức để truy vấn

### Tối Ưu Hiệu Suất Agent
- Sử dụng single knowledge base khi có thể
- Disable các action groups không cần thiết
- Sử dụng default orchestration settings
- Tối ưu prompt instructions

---

## 4. Knowledge Bases và RAG

### Retrieval Augmented Generation (RAG)
RAG là kỹ thuật kết hợp:
- **Retrieval**: Truy xuất thông tin từ knowledge base
- **Generation**: Tạo câu trả lời dựa trên thông tin đã truy xuất

### Amazon Bedrock Knowledge Bases
```python
# Tạo Knowledge Base
import boto3

bedrock_agent = boto3.client('bedrock-agent')

response = bedrock_agent.create_knowledge_base(
    name='MyKnowledgeBase',
    description='Knowledge base for product documentation',
    roleArn='arn:aws:iam::123456789012:role/BedrockKBRole',
    knowledgeBaseConfiguration={
        'type': 'VECTOR',
        'vectorKnowledgeBaseConfiguration': {
            'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1'
        }
    },
    storageConfiguration={
        'type': 'OPENSEARCH_SERVERLESS',
        'opensearchServerlessConfiguration': {
            'collectionArn': 'arn:aws:aoss:us-east-1:123456789012:collection/abc123',
            'vectorIndexName': 'bedrock-knowledge-base-index',
            'fieldMapping': {
                'vectorField': 'vector',
                'textField': 'text',
                'metadataField': 'metadata'
            }
        }
    }
)
```

### So Sánh Long-term Memory vs RAG
- **Long-term Memory**: Lưu trữ context người dùng, preferences
- **RAG**: Truy xuất facts hiện tại từ documents
- **Combined**: Cung cấp responses cá nhân hóa và chính xác

---

## 5. Guardrails (Bảo Vệ An Toàn)

### Mục Đích
- Phát hiện và lọc nội dung có hại
- Bảo vệ thông tin nhạy cảm (PII)
- Đảm bảo AI an toàn và có trách nhiệm

### Các Tính Năng Guardrails
1. **Content Filtering**: Lọc nội dung độc hại, không phù hợp
2. **PII Protection**: Bảo vệ thông tin cá nhân
3. **Topic Filtering**: Chặn các chủ đề không mong muốn
4. **Word Filtering**: Lọc từ ngữ cụ thể
5. **Contextual Grounding**: Đảm bảo câu trả lời dựa trên context

### Tạo Guardrail
```python
import boto3

bedrock = boto3.client('bedrock')

response = bedrock.create_guardrail(
    name='MyGuardrail',
    description='Guardrail for customer service chatbot',
    contentPolicyConfig={
        'filtersConfig': [
            {
                'type': 'HATE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'VIOLENCE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            }
        ]
    },
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {
                'type': 'EMAIL',
                'action': 'BLOCK'
            },
            {
                'type': 'PHONE',
                'action': 'ANONYMIZE'
            }
        ]
    }
)
```

### Sử dụng Guardrail với Inference
```python
response = client.converse(
    modelId='anthropic.claude-opus-4-7',
    messages=[
        {
            'role': 'user',
            'content': [{'text': 'User message here'}]
        }
    ],
    guardrailConfig={
        'guardrailIdentifier': 'guardrail-id',
        'guardrailVersion': '1'
    }
)
```

---

## 6. Prompt Engineering và Management

### Prompt Optimization
Amazon Bedrock cung cấp tính năng tự động tối ưu prompts:

```python
import boto3

bedrock_agent = boto3.client('bedrock-agent')

response = bedrock_agent.optimize_prompt(
    input={
        'textPromptTemplate': 'Summarize the following text: {{text}}'
    },
    targetModelId='anthropic.claude-sonnet-4-6'
)

# Response chứa optimized prompt
optimized_prompt = response['optimizedPrompt']
```

### Prompt Management
- **Versioning**: Quản lý các phiên bản prompt
- **Templates**: Tạo template có thể tái sử dụng
- **Variables**: Sử dụng biến trong prompts
- **Testing**: Test và so sánh các prompts khác nhau

### Best Practices cho Prompt Engineering
1. **Be Specific**: Càng cụ thể càng tốt
2. **Provide Context**: Cung cấp đủ context
3. **Use Examples**: Đưa ví dụ (few-shot learning)
4. **Structure Output**: Yêu cầu format output cụ thể
5. **Iterate**: Thử nghiệm và cải thiện liên tục

---

## 7. Amazon Bedrock Flows

### Khái Niệm
Flows cho phép tạo các workflows phức tạp kết hợp:
- Multiple models
- Knowledge bases
- Lambda functions
- Prompt chains
- Conditional logic

### Async Flow Executions
```python
import boto3

bedrock_agent = boto3.client('bedrock-agent')

# Tạo flow execution
response = bedrock_agent.create_flow_execution(
    flowIdentifier='flow-id',
    flowVersion='1',
    inputs=[
        {
            'content': {'document': {'text': 'Input text here'}},
            'nodeName': 'InputNode',
            'nodeOutputName': 'document'
        }
    ]
)

execution_id = response['id']

# Check status
status_response = bedrock_agent.get_flow_execution(
    flowExecutionId=execution_id,
    flowIdentifier='flow-id'
)
```

### Use Cases cho Flows
- Multi-step reasoning tasks
- Document processing pipelines
- Complex decision-making workflows
- Integration với multiple data sources

---

## 8. Model Customization (Tùy Chỉnh Mô Hình)

### Các Phương Pháp Customization

#### 8.1 Fine-tuning
Huấn luyện model trên dữ liệu cụ thể của bạn:

```python
import boto3

bedrock = boto3.client('bedrock')

response = bedrock.create_model_customization_job(
    jobName='my-fine-tuning-job',
    customModelName='my-custom-model',
    roleArn='arn:aws:iam::123456789012:role/BedrockCustomizationRole',
    baseModelIdentifier='amazon.titan-text-express-v1',
    trainingDataConfig={
        's3Uri': 's3://my-bucket/training-data/'
    },
    validationDataConfig={
        's3Uri': 's3://my-bucket/validation-data/'
    },
    outputDataConfig={
        's3Uri': 's3://my-bucket/output/'
    },
    hyperParameters={
        'epochCount': '3',
        'batchSize': '1',
        'learningRate': '0.00001'
    }
)
```

#### 8.2 Reinforcement Fine-tuning (GRPO)
- Tối ưu model thông qua reward-driven learning
- Cải thiện accuracy trung bình 66%
- Phù hợp cho các tác vụ cần reasoning phức tạp

#### 8.3 Continued Pre-training
- Tiếp tục pre-training trên domain-specific data
- Phù hợp khi cần model hiểu domain knowledge sâu

### Supported Models cho Fine-tuning
- Amazon Titan models
- Anthropic Claude (select versions)
- Amazon Nova models

---

## 9. Cost Management và Optimization

### Cách Amazon Bedrock Tính Phí
- **Token-based Pricing**: Tính theo số tokens (input + output)
- **Model Invocation**: Mỗi lần gọi model
- **Custom Models**: Phí training và hosting
- **Knowledge Bases**: Phí storage và queries

### Cost Allocation by IAM Principal
Amazon Bedrock hỗ trợ phân bổ chi phí theo:
- IAM users
- IAM roles
- Teams
- Projects

```python
# Tag resources để tracking costs
bedrock.tag_resource(
    resourceARN='arn:aws:bedrock:us-east-1:123456789012:agent/agent-id',
    tags={
        'Team': 'DataScience',
        'Project': 'CustomerSupport',
        'Environment': 'Production'
    }
)
```

### Cost Optimization Strategies
1. **Choose Right Model**: Chọn model phù hợp với use case
2. **Optimize Prompts**: Giảm số tokens không cần thiết
3. **Use Caching**: Cache responses khi có thể
4. **Batch Processing**: Xử lý nhiều requests cùng lúc
5. **Monitor Usage**: Theo dõi và phân tích usage patterns

### Sử dụng AWS Cost Explorer
```python
import boto3
from datetime import datetime, timedelta

ce = boto3.client('ce')

response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'End': datetime.now().strftime('%Y-%m-%d')
    },
    Granularity='DAILY',
    Metrics=['UnblendedCost'],
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': ['Amazon Bedrock']
        }
    },
    GroupBy=[
        {
            'Type': 'TAG',
            'Key': 'Team'
        }
    ]
)
```

---

## 10. Security và Best Practices

### Security Best Practices
1. **IAM Permissions**: Sử dụng least privilege principle
2. **VPC Endpoints**: Kết nối private qua VPC
3. **Encryption**: Mã hóa data at rest và in transit
4. **Guardrails**: Luôn sử dụng guardrails cho production
5. **Monitoring**: Theo dõi với CloudWatch và CloudTrail

### IAM Policy Example
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:Retrieve"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/*"
            ]
        }
    ]
}
```

### Monitoring với CloudWatch
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Tạo alarm cho model invocation errors
cloudwatch.put_metric_alarm(
    AlarmName='BedrockModelErrors',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='ModelInvocationClientError',
    Namespace='AWS/Bedrock',
    Period=300,
    Statistic='Sum',
    Threshold=10.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-east-1:123456789012:bedrock-alerts']
)
```

---

## 11. Regions và Endpoints

### Supported Regions
Amazon Bedrock có sẵn ở nhiều AWS Regions:
- US East (N. Virginia) - us-east-1
- US West (Oregon) - us-west-2
- Europe (Frankfurt) - eu-central-1
- Asia Pacific (Tokyo) - ap-northeast-1
- Và nhiều regions khác

### Service Endpoints
```python
# Runtime endpoint
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com'
)

# Agent runtime endpoint
bedrock_agent_runtime = boto3.client(
    'bedrock-agent-runtime',
    region_name='us-east-1',
    endpoint_url='https://bedrock-agent-runtime.us-east-1.amazonaws.com'
)
```

---

## 12. Quick Start - Bắt Đầu Nhanh

### Bước 1: Setup AWS Account
1. Tạo AWS account nếu chưa có
2. Setup IAM user với permissions phù hợp
3. Configure AWS CLI

```bash
aws configure
```

### Bước 2: Request Model Access
```python
import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

# List available models
models = bedrock.list_foundation_models()

# Request access (thông qua console hoặc API)
```

### Bước 3: Install SDK
```bash
pip install boto3
pip install anthropic  # Nếu dùng Anthropic SDK
```

### Bước 4: First API Call
```python
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.converse(
    modelId='anthropic.claude-sonnet-4-6',
    messages=[
        {
            'role': 'user',
            'content': [{'text': 'Hello! What is Amazon Bedrock?'}]
        }
    ]
)

print(response['output']['message']['content'][0]['text'])
```

---

## 13. Use Cases Phổ Biến

### 1. Chatbots và Virtual Assistants
- Customer support automation
- Internal knowledge assistants
- Conversational interfaces

### 2. Content Generation
- Marketing copy
- Product descriptions
- Blog posts và articles
- Social media content

### 3. Document Processing
- Summarization
- Information extraction
- Document classification
- Q&A over documents

### 4. Code Generation và Analysis
- Code completion
- Bug detection
- Code explanation
- Test generation

### 5. Data Analysis
- Report generation
- Insight extraction
- Data visualization recommendations

---

## 14. Troubleshooting Common Issues

### Issue 1: Model Access Denied
**Solution**: Request model access trong Bedrock console

### Issue 2: Throttling Errors
**Solution**: 
- Implement exponential backoff
- Request quota increase
- Optimize request patterns

### Issue 3: High Latency
**Solution**:
- Use streaming responses
- Optimize prompt length
- Choose appropriate model size
- Consider regional endpoints

### Issue 4: Unexpected Outputs
**Solution**:
- Refine prompts
- Use guardrails
- Implement output validation
- Test with different models

---

## 15. Resources và Learning Path

### Official Documentation
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/)

### Learning Resources
1. **AWS Skill Builder**: Amazon Bedrock courses
2. **AWS Workshops**: Hands-on labs
3. **GitHub Examples**: Sample code và templates
4. **AWS Blog**: Latest updates và best practices

### Community
- AWS Forums
- Stack Overflow
- AWS re:Post
- GitHub Discussions

---

## Tổng Kết

Amazon Bedrock là nền tảng mạnh mẽ cho việc xây dựng ứng dụng AI tạo sinh với:
- **Đa dạng models**: 100+ foundation models từ nhiều providers
- **Dễ sử dụng**: APIs đơn giản, fully managed
- **An toàn**: Guardrails, encryption, compliance
- **Linh hoạt**: Customization, fine-tuning, RAG
- **Tiết kiệm**: Pay-per-use, cost optimization tools

Để thành công với Bedrock:
1. Bắt đầu với use case đơn giản
2. Thử nghiệm với nhiều models khác nhau
3. Implement guardrails từ đầu
4. Monitor và optimize costs
5. Liên tục học hỏi và cải thiện

---

**Lưu ý**: Tài liệu này được tạo dựa trên AWS documentation tính đến tháng 5/2026. Luôn tham khảo [official documentation](https://docs.aws.amazon.com/bedrock/) để có thông tin mới nhất.
