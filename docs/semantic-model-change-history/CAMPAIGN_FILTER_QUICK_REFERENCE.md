# Campaign Filter - Quick Reference Guide

## Decision Tree

```
User mentions "campaign"
    ├─ Does user provide a specific name/keyword?
    │  └─ YES → Use email_name fuzzy matching
    │     Examples: "EX30 campaign", "Sustainability campaign"
    │
    └─ NO → Apply program_or_compaign = 'Campaign' filter
       Examples: "campaign performance", "best campaign", "last month's campaign"
```

---

## Category Filter Triggers (Apply `program_or_compaign = 'Campaign'`)

When user says:
- ✅ "campaign" / "campaigns" (general, no specific name)
- ✅ "global campaign" / "global campaigns"
- ✅ "eDM campaign" / "eDM campaigns"
- ✅ "campaign performance"
- ✅ "campaign engagement"
- ✅ "campaign open rate"
- ✅ "campaign click rate"
- ✅ "best campaign"
- ✅ "top campaigns"
- ✅ "last month's campaign"
- ✅ "the campaign that has..."
- ✅ "What was the open rate for last month's global eDM campaign?"

---

## Specific Name Search Triggers (Use `email_name` fuzzy matching)

When user provides:
- ❌ "EX30 campaign"
- ❌ "Show me the Sustainability campaign"
- ❌ "Find campaigns with 'Black Friday'"
- ❌ "How did the Spring Launch campaign perform?"

---

## SQL Examples

### Category Query
**User**: "What campaigns performed best last month?"

**SQL**:
```sql
SELECT ...
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
WHERE m.email_name NOT ILIKE '%sparkpost%'
  AND m.program_or_compaign = 'Campaign'  -- ← CATEGORY FILTER
  AND f.send_date >= DATE_TRUNC('MONTH', DATEADD('MONTH', -1, CURRENT_DATE))
  AND f.send_date < DATE_TRUNC('MONTH', CURRENT_DATE)
ORDER BY click_rate_pct DESC
```

### Specific Name Query
**User**: "Show me the EX30 Launch campaign"

**SQL**:
```sql
SELECT ...
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
WHERE m.email_name NOT ILIKE '%sparkpost%'
  AND (  -- ← FUZZY MATCHING ON EMAIL_NAME
      m.email_name ILIKE '%EX30%Launch%'
      OR m.email_name ILIKE '%EX30-Launch%'
      OR m.email_name ILIKE '%EX30_Launch%'
      OR m.email_name ILIKE '%EX30Launch%'
  )
```

---

## Common Mistakes to Avoid

### ❌ DON'T DO THIS
```sql
-- User asks: "campaign performance"
WHERE email_name ILIKE '%campaign%'  -- ← WRONG! This searches for "campaign" in names
```

### ✅ DO THIS
```sql
-- User asks: "campaign performance"
WHERE program_or_compaign = 'Campaign'  -- ← CORRECT! This filters by category
```

---

## Other Email Types

### Program (Lifecycle/Automated)
**Triggers**: "program", "programs", "lifecycle", "automated"
**Filter**: `WHERE program_or_compaign = 'Program'`

### E-newsletter
**Triggers**: "newsletter", "e-newsletter", "enews", "enewsletter"
**Filter**: `WHERE program_or_compaign = 'E-newsletter'`

---

## Response Pattern for Category

When user asks about campaign as a category, confirm and proceed:

```
"Analyzing all Campaigns (category) - fixed sends based on business objectives,
excluding Programs and E-newsletters.

Retrieving metrics now..."
```

**DO NOT** ask for clarification when it's clear they mean the category.

---

## Response Pattern for Specific Name

When user provides a keyword, show matches and ask for confirmation:

```
"I found 3 campaigns matching 'EX30':

| # | Campaign Name |
|---|---------------|
| 1 | EX30_Launch_Q1_2025 |
| 2 | EX30_Cross_Country_Edition |
| 3 | EX30_Sustainability_Focus |

Would you like to see full names for more detail?
Reply with the number(s) to analyze, or say 'all' for all matches."
```

---

## Edge Cases

### "Show me EX30 campaigns"
- User mentions: "campaigns" (category) + "EX30" (car model)
- **Action**: Apply BOTH filters
- **SQL**: `WHERE program_or_compaign = 'Campaign' AND car_model = 'EX30'`

### "Compare program vs campaign performance"
- User mentions: "program" + "campaign" (both categories)
- **Action**: Compare the two categories
- **SQL**: `GROUP BY program_or_compaign`

---

## Validation Checklist

Before executing a query mentioning "campaign", check:

- [ ] Does user provide a specific campaign name/keyword?
  - YES → Use email_name fuzzy matching
  - NO → Continue to next check

- [ ] Does user say "campaign"/"campaigns" in general?
  - YES → Apply `program_or_compaign = 'Campaign'`
  - NO → No category filter needed

- [ ] Is sparkpost exclusion included?
  - [ ] YES: `email_name NOT ILIKE '%sparkpost%'`

---

## Key Files Reference

1. **Semantic Model**: `config/semantic.yaml`
   - Field: `PROGRAM_OR_COMPAIGN` (lines 1076-1095)
   - Filter: `campaign` (lines 1141-1165)

2. **Orchestration Instructions**: `config/agents/backup/orchestration/instructions_default.md`
   - Campaign Handling: Lines 214-293

3. **Response Instructions**: `config/agents/backup/orchestration/response_default.md`
   - Campaign Clarification: Lines 229-304

---

**Quick Tip**: When in doubt, ask yourself: "Is the user asking about ALL campaigns (category) or A SPECIFIC campaign (name)?" This simple question will guide you to the right approach.
