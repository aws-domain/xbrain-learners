# Tech Stack

## Languages

- **Python 3.10+** — Lambda functions, RAG/AI lab scripts, test files
- **YAML** — SAM templates, CloudFormation templates
- **HTML/CSS/JS** — Static quizzes, interactive dashboards, chat UI (vanilla, no framework)
- **JSON** — SAM event payloads, test fixtures, quiz question banks
- **Markdown** — All notes, guides, and documentation

Vietnamese is preferred for explanations and learning material. Keep code, commands, service names, AWS feature names, and error messages in English.

## AWS Services in Use

| Domain | Services |
|---|---|
| Compute | Lambda (Python 3.10), EC2, ECS/Fargate |
| API | API Gateway (REST), Lambda Authorizer |
| Auth | Cognito User Pool, User Pool Client |
| Database | DynamoDB (PAY_PER_REQUEST billing) |
| Storage | S3 |
| AI/ML | Amazon Bedrock (Claude models), Knowledge Base, RAG |
| IaC | AWS SAM, CloudFormation |
| Observability | CloudWatch, X-Ray (Tracing: Active on all functions) |
| Networking | VPC, Subnets, Security Groups, Transit Gateway, Direct Connect |

This repository is a learning knowledge base, so the service list is descriptive rather than exhaustive. New AWS services may be added when a workshop or topic requires them.

## IaC & Build Tools

- **AWS SAM CLI** — primary tool for serverless projects
  - SAM templates use `Transform: AWS::Serverless-2016-10-31`
  - Default region: `ap-southeast-1`
- **CloudFormation** — underlying engine; used directly for non-serverless infrastructure

## Python Dependencies

Managed per-lab via `requirements.txt` and `venv`. Core libraries:

- `boto3` — AWS SDK (pinned `>=1.34.0`)
- `python-dotenv` — `.env` file loading for local dev
- Test deps live in `tests/requirements.txt`

## Common Commands

### SAM Serverless Projects

```bash
# Build
sam build

# Local test a function
sam local invoke FunctionName --event events/event.json

# Local API
sam local start-api --env-vars env.json

# Validate template
sam validate

# Deploy (first time, interactive)
sam deploy --guided

# Deploy (subsequent, uses samconfig.toml)
sam deploy
```

### Python Labs

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run a test
python test_l1.py
```

### SAM Logs

```bash
sam logs --stack-name <stack-name> --tail
```

## Lambda Defaults (SAM Globals)

```yaml
Globals:
  Function:
    Runtime: python3.10
    MemorySize: 128
    Timeout: 100
    Tracing: Active
```

Override per-function when needed; never remove `Tracing: Active` without reason.

## Environment & Secrets

- Local secrets go in `.env` files loaded via `python-dotenv` — never commit `.env`
- SAM local environment overrides go in `env.json` — safe to commit if no real credentials
- AWS credentials are managed via the default AWS CLI profile / IAM role

## Workshop Execution

- Workshop subprojects live under `workshop/<workshop-name>/`.
- Treat each workshop folder as independently runnable and easy to extract into a separate repository.
- Prefer official AWS workshop instructions as the source of truth for commands and architecture.
- Record local deviations, fixes, cleanup commands, and cost-sensitive steps in each workshop's `README.md` or `troubleshooting.md`.
