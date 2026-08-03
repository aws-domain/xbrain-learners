# Project Structure

## Root Layout

```
xbrain-learners-c/
├── 01_Compute/
├── 02_Storage/
├── 03_Database/
├── 04_Networking/
├── 05_Security_Identity/
├── 06_AI_ML/
├── 07_Data_Engineering/
├── 08_Serverless_IaC/
├── 09_Observability_Operations/
├── 10_Cost_Governance/
├── Others/
├── workshop/
├── .kiro/
│   ├── specs/
│   └── steering/
├── README.md
└── DESIGN.md
```

## Domain Folder Convention

Every numbered domain folder (`NN_DomainName/`) follows the same internal layout:

```
NN_DomainName/
├── notes/          # Markdown study notes for this domain
├── troubleshooting/ # Troubleshooting guides (NN_domain_troubleshooting.md)
├── diagrams/       # Architecture diagrams (.png, .svg, .drawio)
├── practice/       # Hands-on labs, workshops, scripts
└── quizzes/        # HTML quiz files for self-assessment
```

Not every domain has all four subdirectories — only add a subdirectory when content exists for it.

## Notes Convention

- One `.md` file per topic (e.g., `vpc_with_multiple_subnets.md`, `dynamodb.md`)
- Filename: `snake_case`, descriptive, no spaces
- Language: Vietnamese or English — match the surrounding content in the same folder
- Structure notes with `##` sections; use tables for comparisons; use code blocks for YAML/CLI examples

## Troubleshooting Files

Each domain has one consolidated troubleshooting file named `NN_domain_troubleshooting.md`. Add new issues to the existing file rather than creating separate files per issue. Exception: detailed multi-step guides can be standalone (e.g., `ssh_connection_timeout.md`).

## Practice / Lab Projects

Labs live under `practice/` in a named subdirectory:

```
practice/
└── project-name/
    ├── README.md         # Lab overview and instructions
    ├── template.yaml     # SAM/CFN template (if IaC lab)
    ├── samconfig.toml    # SAM deploy config (if SAM lab)
    ├── src/              # Lambda function source code
    │   └── api/
    ├── events/           # SAM local test event payloads
    ├── tests/
    │   ├── unit/
    │   └── integration/
    ├── requirements.txt  # Runtime dependencies
    └── env.json          # Local env var overrides (no secrets)
```

Python labs (AI/ML) follow a flat structure with a `venv/`, `requirements.txt`, and numbered test files (`test_l1.py`, `test_l2.py`, ...).

## Workshop Workspace

The root-level `workshop/` directory is reserved for AWS workshops. Each workshop should live in its own subdirectory and should be treated as an independent learning project that can later become its own Git repository.

```
workshop/
└── workshop-name/
    ├── README.md              # Workshop purpose, source link, scope, and progress
    ├── notes/                 # Vietnamese-first study notes and summaries
    ├── labs/                  # Lab steps, commands, screenshots, or exercise notes
    ├── infra/                 # IaC if the workshop deploys AWS resources
    ├── scripts/               # Helper scripts for workshop exercises
    ├── troubleshooting.md     # Errors, fixes, and lessons learned
    └── references.md          # Official links and extra reading
```

Use `kebab-case` for workshop folder names. If a workshop is copied out as a separate repository, preserve its internal structure and keep only summary links or final notes in the main topic folders.

## SAM Project Specifics

- Handler path convention: `src/api/<module>.lambda_handler`
- DynamoDB tables use `PAY_PER_REQUEST` billing mode
- Stack naming: `ws-<project-name>-<resource>` (e.g., `ws-serverless-patterns-users`)
- Always include `Outputs` section with key resource ARNs and endpoints

## .kiro Directory

```
.kiro/
├── specs/
│   └── feature-name/
│       ├── requirements.md
│       ├── design.md
│       ├── tasks.md
│       └── .config.kiro
└── steering/
    ├── product.md
    ├── tech.md
    └── structure.md
```

## Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Note files | `snake_case.md` | `api_gateway_vs_alb.md` |
| Lab directories | `kebab-case` | `conduit-aws-networking` |
| Workshop directories | `kebab-case` | `aws-database-migration-workshop` |
| SAM stacks | `kebab-case` | `ws-serverless-patterns-users` |
| Python files | `snake_case.py` | `bedrock_client.py` |
| Quiz files | `topic_quiz.html` | `bedrock_ai_quiz.html` |
| Spec features | `kebab-case` | `cloud-journey` |

## What NOT to Commit

- `.env` files (contain API keys / AWS credentials)
- `venv/` directories
- `.DS_Store`
- `.aws-sam/build/` (generated build artifacts)
