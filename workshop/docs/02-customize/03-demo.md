# Build & Test (Customer PoC)

## Test your solution

After generation completes, test the agent:

```bash
python scripts/08_test_foundry_agent.py
```

## Use the Generated Sample Questions

Each scenario generates ready-to-use sample questions in the data folder:

```bash
# View sample questions for your scenario
cat data/default/config/sample_questions.txt
```

The file contains three categories of questions:

| Category | Source | Example |
|----------|--------|---------|
| **Structured data questions** | Fabric IQ (data) | "How many open claims do we have?" |
| **Unstructured data questions** | Foundry IQ (docs) | "What's our process for filing a property claim?" |
| **Combined questions** | Both sources | "Which claims are approaching our SLA deadline based on our process guidelines?" |

!!! tip "Use these questions first"
    The generated questions are tailored to your scenario's data and documents. Start with these before improvising.

## Current tool contract

The workshop agent uses a small, explicit tool contract. Keeping your demo questions inside these boundaries makes the behavior much more predictable.

| Tool | Use it for | Do not use it for | Input schema | Result shape |
|------|------------|-------------------|--------------|--------------|
| **execute_sql** | Counts, totals, trends, rankings, joins, and record lookup in Fabric tables | Policies, procedures, narrative explanations, or any write operation | `sql_query: string` | Markdown table with row count |
| **search_documents** | Policies, procedures, FAQs, guidance, and other unstructured document content | Calculations or broad table scans | `query: string`, `top?: integer` | Cited passages with source, title, and page metadata |

In `--foundry-only` mode, the agent only registers `search_documents`.

### Response loop

When you run `python scripts/08_test_foundry_agent.py`, the runtime follows this loop:

1. The model inspects the question and decides whether it needs `execute_sql`, `search_documents`, or both.
2. The local script executes each requested tool and prints a preview so you can see what happened.
3. The raw tool output is sent back to the model as `function_call_output`.
4. The model synthesizes the final answer from those tool results.

### Example outputs

```text
[SQL Tool] Executing query:
    SELECT TOP 5 claim_id, status
    FROM claims

| claim_id | status |
|---|---|
| CLM-1001 | Open |
| CLM-1002 | Pending |

(2 rows returned)
```

```text
[Search Tool] Searching for: outage communication policy (top=3)...

--- Result 1 ---
Source: outage-policy.pdf (Page 2)
Title: Outage Management Policy
Content: Customers must be notified within 15 minutes of a confirmed outage...
```

## Testing Tips

### Start with structured data questions

Show the power of natural language over structured data:

```
"How many [entities] do we have?"
"What's the total [metric] for [time period]?"
"Show me the top 5 [entities] by [metric]"
```

### Then unstructured data questions

Demonstrate intelligent document retrieval:

```
"What's our policy on [topic]?"
"How do we handle [process]?"
"What are the requirements for [action]?"
```

### Finish with combined questions

This is the "wow" moment: questions that need both sources:

```
"Based on our [policy], which [entities] need attention?"
"Are we meeting our [documented SLA] according to the data?"
"Which [items] don't comply with our [policy/guidelines]?"
```

## Prepare your test script

Before customer meetings, prepare 5-7 questions:

| # | Question Type | Example |
|---|---------------|---------|
| 1 | Structured data | "How many open claims do we have?" |
| 2 | Structured data | "What's the total value of claims filed this month?" |
| 3 | Structured data | "Which agents have the most policies?" |
| 4 | Unstructured data | "What's our process for filing a property claim?" |
| 5 | Unstructured data | "What does our standard homeowner policy cover?" |
| 6 | **Combined** | "Which open claims are approaching our SLA deadline based on our process guidelines?" |
| 7 | **Combined** | "Do any current claims involve coverage types not in our standard policy?" |

!!! tip "Let customers ask questions"
    After your prepared questions, let customers ask their own questions. This shows the solution handles real scenarios, not just scripted ones.

## Checkpoint

!!! success "Ready for Customer PoC"
    Your custom PoC should:

    - [x] Answer structured data questions accurately
    - [x] Retrieve relevant unstructured document content
    - [x] Combine sources for complex questions
    - [x] Use industry-appropriate terminology

    **Next:** Review [Deep dive](../03-understand/index.md) to prepare for technical questions

## Quick Reference: Regenerate for another industry use case

```bash
# Edit .env with new customer's industry and use case, then:
python scripts/00_build_solution.py --clean

# Or inline:
python scripts/00_build_solution.py --clean \
  --industry "New Industry" \
  --usecase "New use case description"
```

---

[← Generate & Build](02-generate.md) | [Deep dive →](../03-understand/index.md)
