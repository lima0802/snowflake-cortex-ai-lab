# Troubleshooting: "Unable to obtain result for query"

## Error Message
```
Unable to obtain result for query: '<unspecified "desc">'; status summary: SUCCESS
```

## What This Means

- ✅ **Status: SUCCESS** - The SQL query executed successfully in Snowflake
- ❌ **Unable to obtain result** - Cortex Analyst couldn't retrieve/format the results
- ⚠️ **'<unspecified "desc">'** - The query doesn't have a proper description

## Common Causes

### 1. **Large Result Set**
Cortex Analyst may timeout or fail to process very large result sets.

**Solution**:
- Add `LIMIT` clauses to verified questions
- Add filters to reduce result size
- Check if any queries return millions of rows

### 2. **Malformed Query Response**
The query might return data in an unexpected format.

**Solution**:
- Check for NULL values in key columns
- Ensure all column names are valid
- Verify data types match expectations

### 3. **Cortex Analyst Token Limit**
Results may exceed Cortex's response token limit.

**Solution**:
- Reduce the number of columns in SELECT
- Add more restrictive WHERE clauses
- Use aggregation instead of detailed rows

### 4. **Missing Query Description in Agent Config**
The Cortex agent might be missing description metadata.

**Solution**:
- Check if all verified questions have proper `question:` fields
- Ensure the semantic model has a valid `description:` at the top

### 5. **Snowflake Session/Connection Issue**
Temporary connectivity or session timeout.

**Solution**:
- Refresh the Cortex Analyst session
- Re-deploy the semantic model
- Check Snowflake warehouse status

---

## Troubleshooting Steps

### Step 1: Identify the Problematic Query

**Option A**: If error occurs with a specific question:
1. Note which question triggers the error
2. Find that query in `semantic.yaml`
3. Test it directly in Snowflake

**Option B**: If error occurs on model load:
1. Check the Snowflake query history
2. Find the failing query
3. Test it manually

### Step 2: Test the Query Directly

```sql
-- Copy the exact SQL from the semantic.yaml verified question
-- Run it directly in Snowflake to see if it executes

SELECT ...
FROM ...
WHERE ...
LIMIT 100;  -- Add LIMIT if not present
```

**Check**:
- ✅ Does it run?
- ✅ Does it return results?
- ✅ How many rows?
- ✅ Are there NULL values?
- ✅ Are column names valid?

### Step 3: Check Result Size

If the query returns a large result set:

```sql
-- Add to the top of your query
SELECT COUNT(*) FROM (
  -- Your original query here
  SELECT ...
);
```

**Guideline**:
- ✅ < 1,000 rows: Usually fine
- ⚠️ 1,000 - 10,000 rows: May cause issues
- ❌ > 10,000 rows: Likely too large for Cortex

**Fix**: Add more restrictive filters or LIMIT clause

### Step 4: Simplify the Query

If the query is complex, try simplifying:

```sql
-- Instead of:
SELECT c.region_name_group, c.sub_region, c.country_name, f.business_unit, ...
  20 more columns
FROM ...

-- Try:
SELECT c.region_name_group, c.sub_region, SUM(f.sends) as total_sends
FROM ...
GROUP BY c.region_name_group, c.sub_region
LIMIT 50;
```

### Step 5: Check for Data Issues

```sql
-- Check for NULL values in key columns
SELECT
  COUNT(*) as total_rows,
  COUNT(region_name_group) as non_null_region,
  COUNT(sub_region) as non_null_subregion,
  COUNT(country_name) as non_null_country
FROM V_DIM_COUNTRY;
```

### Step 6: Verify Column Names

Ensure all column names in your queries match the actual table schema:

```sql
DESCRIBE TABLE DEV_MARCOM_DB.DM.V_DIM_COUNTRY;
```

Check:
- ✅ `SUB_REGION` (not `REGION`)
- ✅ `REGION_NAME_GROUP` (not `REGION_GROUP`)
- ✅ `VC_COUNTRY_CODE` (not `COUNTRY_CODE`)

---

## Quick Fixes to Try

### Fix 1: Add LIMIT to Large Queries

Find queries without LIMIT and add one:

```yaml
# In semantic.yaml
- name: LARGE_QUERY
  sql: |-
    SELECT ...
    FROM ...
    ORDER BY ...
    LIMIT 1000  # Add this
```

### Fix 2: Re-deploy Semantic Model

Sometimes Cortex Analyst needs a refresh:

1. In Snowflake UI, go to your Cortex Analyst
2. Re-upload or refresh the semantic model
3. Test again

### Fix 3: Check Query in Snowflake History

```sql
-- In Snowflake, run:
SELECT
  query_text,
  execution_status,
  error_message,
  rows_produced,
  execution_time
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_text ILIKE '%V_DIM_COUNTRY%'
  OR query_text ILIKE '%SFMC%'
ORDER BY start_time DESC
LIMIT 20;
```

Look for:
- ❌ Failed queries
- ⚠️ Queries with millions of rows
- ⚠️ Queries taking > 30 seconds

### Fix 4: Validate Verified Questions

Check all verified questions have proper structure:

```yaml
- name: QUERY_NAME           # ✅ Must have
  sql: |-                    # ✅ Must have
    SELECT ...
  question: What is...?      # ✅ Must have
  verified_at: 1234567890    # ✅ Must have
  verified_by: Your Name     # ✅ Must have
```

---

## Specific Checks for Recent Changes

Since we just updated the regional fields, check:

### 1. All queries use `SUB_REGION` (not `REGION`)

```bash
# Search for any remaining REGION references
grep -n "region," semantic.yaml
grep -n "c\.region[^_]" semantic.yaml
```

### 2. All queries include both regional fields

```sql
-- ✅ CORRECT
SELECT
  c.region_name_group,
  c.sub_region,
  ...

-- ❌ WRONG - Missing one
SELECT
  c.sub_region,
  ...
```

### 3. GROUP BY matches SELECT

```sql
-- ✅ CORRECT
SELECT c.region_name_group, c.sub_region, SUM(...)
GROUP BY c.region_name_group, c.sub_region

-- ❌ WRONG - Mismatch
SELECT c.region_name_group, c.sub_region, SUM(...)
GROUP BY c.region_name_group  -- Missing sub_region
```

---

## If Nothing Works

### Option 1: Test with Minimal Semantic Model

Create a minimal test version:

```yaml
name: TEST_MODEL
description: Test model
tables:
  - name: V_DIM_COUNTRY
    base_table:
      database: DEV_MARCOM_DB
      schema: DM
      table: V_DIM_COUNTRY
    dimensions:
      - name: COUNTRY_NAME
        expr: COUNTRY_NAME
        data_type: VARCHAR(200)
        description: Country name

verified_queries:
  - name: TEST_QUERY
    sql: SELECT country_name FROM V_DIM_COUNTRY LIMIT 10
    question: Test query
```

If this works, gradually add back tables/queries to find the issue.

### Option 2: Check Cortex Analyst Logs

In Snowflake:
1. Go to Cortex Analyst interface
2. Check for any error logs or warnings
3. Look for stack traces

### Option 3: Contact Snowflake Support

Provide them with:
- The semantic.yaml file
- The specific query that fails
- Query history from Snowflake
- Screenshots of the error

---

## Prevention

### 1. Always Add LIMIT to Development Queries

```yaml
verified_queries:
  - name: DEV_QUERY
    sql: |-
      SELECT ...
      LIMIT 1000  # Always limit during development
```

### 2. Test Queries in Snowflake First

Before adding to semantic.yaml:
1. Write the query in Snowflake UI
2. Run it and verify results
3. Check row count and performance
4. Then add to semantic model

### 3. Use Aggregation for Large Tables

```sql
-- Instead of: SELECT * FROM fact_table
-- Use: SELECT region, COUNT(*), SUM(sends) FROM fact_table GROUP BY region
```

### 4. Monitor Query Performance

Set up monitoring for:
- Query execution time
- Row counts
- Error rates

---

## Common Patterns to Avoid

### ❌ Don't: Return All Columns
```sql
SELECT * FROM V_FACT_SFMC_PERFORMANCE_TRACKING
```

### ✅ Do: Select Specific Columns
```sql
SELECT send_id, sends, unique_clicks FROM V_FACT_SFMC_PERFORMANCE_TRACKING LIMIT 1000
```

### ❌ Don't: No LIMIT on Fact Tables
```sql
SELECT * FROM fact_table WHERE date > '2020-01-01'
```

### ✅ Do: Always LIMIT
```sql
SELECT * FROM fact_table WHERE date > '2020-01-01' LIMIT 100
```

### ❌ Don't: Complex Nested Queries Without LIMIT
```sql
SELECT * FROM (
  SELECT * FROM (
    SELECT * FROM fact_table
  )
)
```

### ✅ Do: Limit Early
```sql
SELECT * FROM (
  SELECT * FROM fact_table LIMIT 1000
) LIMIT 100
```

---

## Contact Points

If you continue to experience issues:

1. **Check Snowflake Documentation**: https://docs.snowflake.com/en/user-guide/ui-snowsight-cortex-analyst
2. **Review Query History**: Use Snowflake Query History to see actual executed SQL
3. **Test Incrementally**: Start with simple queries and gradually add complexity

---

**Created**: 2026-02-12
**Error Type**: Cortex Analyst Result Retrieval
**Status**: Troubleshooting Guide
