# SUB_REGION as Primary Regional Field - Critical Update

## 🎯 Critical Change Summary

**SUB_REGION** is now the **PRIMARY field** for all regional queries. This update ensures:

1. ✅ **Always include BOTH fields** in SELECT: `region_name_group` AND `sub_region`
2. ✅ **Filter by SUB_REGION** when user mentions any region name
3. ✅ **Add clarifying note** when filtering by sub_region to explain the hierarchy
4. ✅ **GROUP BY both fields** for proper context

---

## Why This Change?

**Problem**: Users were confused about which regional field to use, and results lacked context about the hierarchy.

**Solution**: Make SUB_REGION the primary filter field, but always show both levels for clarity.

---

## The New Rules

### Rule 1: Always Include BOTH Fields in SELECT

```sql
-- ✅ CORRECT
SELECT
  c.region_name_group AS parent_region,  -- Context field
  c.sub_region,                           -- Primary field
  -- metrics
FROM ...

-- ❌ WRONG - Missing context
SELECT
  c.sub_region,  -- Missing parent region
  -- metrics
FROM ...
```

### Rule 2: Filter by SUB_REGION (Primary Field)

```sql
-- User asks: "Show Nordics performance"
-- ✅ CORRECT
WHERE c.sub_region = 'Nordics'

-- ❌ WRONG
WHERE c.region_name_group = 'Nordics'  -- Nordics is not in region_name_group!
```

### Rule 3: Always Add Clarifying Note

When filtering by SUB_REGION, add this note at the end of the response:

**Template**:
```
Note: [sub_region_name] is a sub-region within the [region_name_group] region.
```

**Examples**:
- "Note: Nordics is a sub-region within the EMEA region."
- "Note: Central Europe is a sub-region within the EMEA region, including Germany, Netherlands, Switzerland, and Austria."
- "Note: APEC NSC is a sub-region within the APEC region."

### Rule 4: GROUP BY Both Fields

```sql
-- ✅ CORRECT
GROUP BY c.region_name_group, c.sub_region

-- ❌ WRONG - Missing hierarchy
GROUP BY c.sub_region
```

---

## Response Patterns

### Pattern 1: User Asks About SUB_REGION

**User Question**: "Show me Nordics performance"

**SQL**:
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region = 'Nordics'  -- Filter by SUB_REGION
  AND ...
GROUP BY c.region_name_group, c.sub_region
```

**Response**:
```
Nordics Performance:

| Parent Region | Sub-Region | Click Rate | Sends |
|---------------|------------|------------|-------|
| EMEA          | Nordics    | 4.5%       | 2.1M  |

Note: Nordics is a sub-region within the EMEA region, including Sweden, Norway, Denmark, Finland, and Iceland.
```

---

### Pattern 2: User Asks About "Region" (Ambiguous)

**User Question**: "Show me European region performance"

**SQL**:
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.region_name_group = 'EMEA'  -- Broader query - use top-level filter
  AND ...
GROUP BY c.region_name_group, c.sub_region
ORDER BY click_rate DESC
```

**Response**:
```
European Region Performance by Sub-Region:

| Parent Region | Sub-Region      | Click Rate | Sends |
|---------------|-----------------|------------|-------|
| EMEA          | Nordics         | 4.5%       | 2.1M  |
| EMEA          | Central Europe  | 4.2%       | 3.5M  |
| EMEA          | Western Europe  | 3.8%       | 4.2M  |
| EMEA          | UK & Ireland    | 4.7%       | 3.8M  |
| EMEA          | Eastern Europe  | 3.5%       | 1.2M  |

Note: Results show EMEA region broken down by sub-regions for detailed analysis.
```

---

### Pattern 3: Compare Sub-Regions

**User Question**: "Compare Nordics vs Central Europe"

**SQL**:
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region IN ('Nordics', 'Central Europe')  -- Filter by SUB_REGION
  AND ...
GROUP BY c.region_name_group, c.sub_region
```

**Response**:
```
Nordics vs Central Europe Comparison:

| Parent Region | Sub-Region      | Click Rate | Sends |
|---------------|-----------------|------------|-------|
| EMEA          | Nordics         | 4.5%       | 2.1M  |
| EMEA          | Central Europe  | 4.2%       | 3.5M  |

Nordics outperforms Central Europe by 0.3 percentage points in click rate.

Note: Both Nordics and Central Europe are sub-regions within the EMEA region.
```

---

### Pattern 4: Top-Level Regional Comparison

**User Question**: "Compare all regions"

**SQL**:
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE ...
GROUP BY c.region_name_group, c.sub_region
ORDER BY click_rate DESC
```

**Response** (can aggregate if needed):
```
Global Regional Comparison:

| Parent Region | Total Sends | Click Rate | Top Sub-Region   |
|---------------|-------------|------------|------------------|
| EMEA          | 15.8M       | 4.1%       | UK & Ireland     |
| US/CAN        | 12.5M       | 4.3%       | USA and Canada   |
| APEC          | 8.2M        | 3.9%       | APEC NSC         |
| LATAM         | 2.1M        | 3.2%       | LATAM NSC        |

Note: Results show top-level regional comparison. Each parent region contains multiple sub-regions.
```

---

## Decision Logic

### When User Mentions a Region Name:

```
1. Check: Is this region name in SUB_REGION?
   ├─ YES → Filter by c.sub_region = 'region_name'
   │         Include both fields in SELECT
   │         Add clarifying note
   │
   └─ NO → Check: Is this in REGION_NAME_GROUP?
           ├─ YES → Filter by c.region_name_group = 'region_name'
           │         Include both fields in SELECT
           │         Show sub-region breakdown
           │
           └─ NO → Ask for clarification
```

### Examples:

| User Says | Field to Filter | SQL |
|-----------|-----------------|-----|
| "Nordics" | SUB_REGION | `WHERE c.sub_region = 'Nordics'` |
| "Central Europe" | SUB_REGION | `WHERE c.sub_region = 'Central Europe'` |
| "APEC NSC" | SUB_REGION | `WHERE c.sub_region = 'APEC NSC'` |
| "Europe" / "EMEA" | REGION_NAME_GROUP | `WHERE c.region_name_group = 'EMEA'` |
| "Asia" / "APEC" | REGION_NAME_GROUP | `WHERE c.region_name_group = 'APEC'` |

---

## Field Roles

| Field | Role | When to Use | Always Include? |
|-------|------|-------------|-----------------|
| **SUB_REGION** | **PRIMARY filter** | Default for all regional queries | ✅ YES |
| **REGION_NAME_GROUP** | Context/Parent | For top-level comparisons | ✅ YES |
| **COUNTRY_NAME** | Granular detail | For country-level analysis | When relevant |

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Only Including One Field
```sql
-- WRONG
SELECT
  c.sub_region,
  SUM(f.sends)
FROM ...
GROUP BY c.sub_region
```

**Problem**: User doesn't see parent region context

### ✅ Correct:
```sql
SELECT
  c.region_name_group AS parent_region,  -- Context
  c.sub_region,                           -- Primary
  SUM(f.sends)
FROM ...
GROUP BY c.region_name_group, c.sub_region
```

---

### ❌ Mistake 2: Filtering by Wrong Field
```sql
-- User asks: "Show Nordics performance"
-- WRONG
WHERE c.region_name_group = 'Nordics'  -- Nordics is not in this field!
```

### ✅ Correct:
```sql
WHERE c.sub_region = 'Nordics'  -- Nordics is in SUB_REGION
```

---

### ❌ Mistake 3: Missing Clarifying Note
```
Nordics Performance:

| Sub-Region | Click Rate |
|------------|------------|
| Nordics    | 4.5%       |

[No note - user doesn't understand hierarchy]
```

### ✅ Correct:
```
Nordics Performance:

| Parent Region | Sub-Region | Click Rate |
|---------------|------------|------------|
| EMEA          | Nordics    | 4.5%       |

Note: Nordics is a sub-region within the EMEA region.
```

---

## Files Updated

### 1. semantic.yaml

**SUB_REGION Field** (lines 408-451):
- Added "PRIMARY REGIONAL FIELD" designation
- Added `region`, `regional_area` to synonyms
- Added CRITICAL QUERY RULES section

**REGION_NAME_GROUP Field** (lines 472-511):
- Clarified as "SECONDARY field" for context
- Added note about using SUB_REGION as primary

**Regional Hierarchy Section** (lines 4528-4620):
- Added CRITICAL QUERY RULES
- Emphasized SUB_REGION as PRIMARY filter field
- Added response pattern with clarifying notes
- Included SQL examples with both fields

**Best Practices** (line 5013):
- Updated to emphasize including both fields
- Marked SUB_REGION as primary

**Sample Queries** (lines 3206-3225, 4173-4191, 4975-4987):
- Updated to include both fields in SELECT
- Updated to GROUP BY both fields
- Added comments explaining field roles

---

### 2. instructions_default.md

**Regional Hierarchy Section** (lines 428-462):
- Added CRITICAL QUERY RULES at the top
- Emphasized SUB_REGION as PRIMARY field
- Added template for clarifying notes
- Added GROUP BY guidance

---

### 3. response_default.md

**New Section** (lines 93-178):
- Added REGIONAL QUERY RESPONSE PATTERNS
- 5 detailed examples showing proper formatting
- Templates for clarifying notes
- Examples covering all scenarios

---

## Testing Checklist

After deploying, test these scenarios:

### ✅ Test 1: SUB_REGION Query
**Input**: "Show Nordics performance"
**Expected**:
- Filter: `WHERE c.sub_region = 'Nordics'`
- SELECT includes: `region_name_group`, `sub_region`
- Response includes clarifying note

### ✅ Test 2: Ambiguous "Region" Query
**Input**: "Show European region"
**Expected**:
- Shows breakdown by sub-regions
- Includes both parent region and sub-region columns
- Note explains the breakdown

### ✅ Test 3: Sub-Region Comparison
**Input**: "Compare Nordics vs Central Europe"
**Expected**:
- Filter: `WHERE c.sub_region IN ('Nordics', 'Central Europe')`
- Both columns present
- Note explains they're both in EMEA

### ✅ Test 4: Top-Level Comparison
**Input**: "Compare EMEA vs APEC"
**Expected**:
- May aggregate or show sub-region breakdown
- Both hierarchy levels visible
- Note explains top-level comparison

### ✅ Test 5: Region Not in REGION_NAME_GROUP
**Input**: "Show APEC NSC markets"
**Expected**:
- Filter: `WHERE c.sub_region = 'APEC NSC'`
- Shows parent region (APEC) for context
- Note: "APEC NSC is a sub-region within the APEC region"

---

## Quick Reference

### Always Remember:
1. 📋 **Include both fields** in SELECT
2. 🎯 **Filter by SUB_REGION** (primary)
3. 📝 **Add clarifying note** when using sub_region filter
4. 🔢 **GROUP BY both fields**

### Template:
```sql
SELECT
  c.region_name_group AS parent_region,  -- Context
  c.sub_region,                           -- Primary
  -- metrics
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region = 'SUB_REGION_NAME'    -- Primary filter
  AND ...
GROUP BY c.region_name_group, c.sub_region
```

**Response Note Template**:
```
Note: [sub_region] is a sub-region within the [parent_region] region.
```

---

**Created**: 2026-02-12
**Priority**: CRITICAL
**Impact**: All regional queries
