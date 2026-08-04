# Agent Instructions

## Repository Context

This repository is a personal AWS knowledge base. It stores notes, diagrams, troubleshooting guides, quizzes, and workshop material for learning AWS cloud engineering.

Vietnamese is the primary language for explanations, plans, notes, and summaries. Keep AWS service names, CLI commands, API names, feature names, and error messages in English.

## Codex And Kiro CLI Workflow

When the user asks Codex to analyze, plan, or reason first and then have Kiro execute, use Kiro CLI from the relevant repository root.

Default parent repo:

```bash
cd /Users/enma/Downloads/Coding/Cloud_Engineer/Unitled/xbrain-learners-c
```

Default non-interactive Kiro call:

```bash
kiro-cli chat --no-interactive --wrap never "<prompt>"
```

Use this for quick questions, review requests, and small bounded tasks where Kiro does not need to preserve prior context.

Use Kiro CLI v3 spec mode when the user is explicitly working with Kiro specs or asks Kiro to implement from a spec:

```bash
kiro-cli chat --v3 --mode spec --no-interactive --wrap never "<prompt>"
```

Resume the latest Kiro session for the current directory only when continuity matters:

```bash
kiro-cli chat --resume --no-interactive --wrap never "<prompt>"
```

Use restricted trusted tools for simple file-only execution when possible:

```bash
kiro-cli chat --no-interactive --wrap never --trust-tools=fs_read,fs_write "<bounded implementation prompt>"
```

If the user explicitly wants Kiro to modify files and run commands, make the prompt precise and bounded. Use `--trust-all-tools` only when the user has clearly asked Kiro to perform the implementation, and after Codex has checked the current git status.

```bash
kiro-cli chat --no-interactive --wrap never --trust-all-tools "<bounded implementation prompt>"
```

## Choosing The Right Kiro Command

| Situation | Preferred command |
|---|---|
| Ask Kiro a one-off question | `kiro-cli chat --no-interactive --wrap never "<prompt>"` |
| Continue the latest Kiro conversation in this directory | `kiro-cli chat --resume --no-interactive --wrap never "<prompt>"` |
| Work with Kiro specs | `kiro-cli chat --v3 --mode spec --no-interactive --wrap never "<prompt>"` |
| Small file-only execution | `kiro-cli chat --no-interactive --wrap never --trust-tools=fs_read,fs_write "<prompt>"` |
| Implementation requiring commands/tests | `kiro-cli chat --no-interactive --wrap never --trust-all-tools "<prompt>"` |
| Large task requiring careful planning | Codex writes a markdown plan first, then Kiro reads and executes the plan in bounded steps |

For long prompts, avoid fragile inline shell quoting. Write the Kiro prompt to a markdown file first, then call:

```bash
kiro-cli chat --no-interactive --wrap never "$(cat path/to/kiro-prompt.md)"
```

## Large Task Handoff Pattern

For large tasks, Codex should not ask Kiro to "do everything" from a chat paragraph. Codex should first create or update a plan file, then ask Kiro to execute one bounded phase.

Recommended temporary plan path:

```text
.kiro/handoffs/<task-name>.md
```

Recommended plan structure:

```markdown
# Kiro Handoff: <Task Name>

## Context
<repo purpose, current state, relevant files>

## Objective
<clear end state>

## Allowed Edits
- <paths Kiro may edit>

## Do Not Edit
- <paths Kiro must avoid>

## Execution Plan
- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...

## Verification
- <commands to run>

## Output Required From Kiro
- changed files
- commands run
- verification result
- blockers or follow-up tasks
```

Then call Kiro with a prompt like:

```text
You are working in /Users/enma/Downloads/Coding/Cloud_Engineer/Unitled/xbrain-learners-c.
Read .kiro/handoffs/<task-name>.md.
Execute only Step 1 from the Execution Plan.
Respect Allowed Edits and Do Not Edit sections exactly.
Run the Verification commands listed for Step 1 if applicable.
When finished, report changed files, commands run, verification results, and any blockers.
```

## Prompt Contract For Calling Kiro

When delegating work to Kiro CLI, include:

- the repository path
- the task objective
- files or folders Kiro may edit
- files or folders Kiro must not edit
- verification commands to run, if any
- expected output format

Example:

```text
You are working in /Users/enma/Downloads/Coding/Cloud_Engineer/Unitled/xbrain-learners-c.
Task: create Vietnamese notes for the AWS 101 NoSQL Databases workshop.
Allowed edits: workshop/aws-101-nosql-databases/**.
Do not edit: .kiro/**, .gitmodules, parent repo topic folders.
After editing, summarize changed files and any commands run.
```

## Kiro CLI And Powers

Kiro CLI does not currently consume Kiro IDE Powers directly. MCP servers packaged by Powers must be installed for CLI through normal MCP configuration, such as `~/.kiro/settings/mcp.json` or `kiro-cli mcp add`.

Do not assume a Power-installed MCP is available to Kiro CLI. Check with:

```bash
kiro-cli mcp list
```

## Git Safety

Before asking Kiro to execute file changes, Codex should check:

```bash
git status --short
```

Do not revert user changes. If the working tree is dirty, mention the relevant dirty files and constrain Kiro's allowed edit paths.

## Imported Rules

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### 5. Naming With Intent

**Names should reveal purpose, not hide uncertainty.**

- Prefer names that describe responsibility, not vague roles.
- Match the naming conventions already used in the codebase.
- Avoid generic names like `helper`, `util`, `data`, `temp`, `manager`, or `newThing`.
- Use short names only for small, obvious local scope.
- File, function, class, and variable names should reflect what the code actually owns.

If naming is difficult, the design is probably still unclear. Simplify the responsibility before adding more code.

### 6. Token-Efficient Structure

**Keep code small enough that an AI can edit it cheaply and safely.**

- Avoid letting active working files grow into large context sinks.
- If a file is frequently edited and grows beyond ~300 lines, consider splitting it by responsibility.
- Prefer smaller modules when doing so reduces token cost, review cost, and bug-fix blast radius.
- Separate orchestration, business logic, data access, and presentation when they start changing for different reasons.
- Do not split purely for style - split when it makes future edits cheaper, safer, or clearer.

Treat ~300 lines as a warning threshold for actively edited files, not a universal hard limit.

Large files are expensive: they cost more to read, more to rewrite, and make follow-up fixes less precise.
