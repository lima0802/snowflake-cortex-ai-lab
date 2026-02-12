# Module Custom Instructions - Regional Hierarchy Update

## Summary

✅ **Updated module_custom_instructions** in semantic.yaml to accurately reflect the correct regional hierarchy using only `region_name_group` and `sub_region` (NOT sales_area).

---

## Changes Made

### 1. **SUB_REGION Section** (Lines 4506-4549)

**Before**: Incorrectly listed detailed sub-regions like "Nordics", "Central Europe", "APEC NSC", "APEC Importers", etc.

**After**: Correctly lists only 6 values:
- APEC
- EMEA
- USA and Canada
- LATAM (includes ALL Latin American countries)
- Greater China
- Other (Global, Multi-market, Global Major Accounts)

**Key Updates**:
- ✅ Removed incorrect detailed sub-regions (those are from SALES_AREA, which is NOT used)
- ✅ Added clear mapping to REGION_NAME_GROUP
- ✅ Updated examples to use correct SUB_REGION values
- ✅ Clarified that LATAM includes ALL Latin countries (Mexico, Brazil, Argentina, Chile, Colombia, etc.)
- ✅ Updated response pattern example

---

### 2. **Region Name Mapping Section** (Lines 4552-4591)

**Before**: Used `region_name_group` as the primary filter field

**After**: Uses `sub_region` as the primary filter field with clear mapping

**Updated Mapping**:

| User Says | Filter By | Notes |
|-----------|-----------|-------|
| "Europe", "EMEA" | `WHERE c.sub_region = 'EMEA'` | Can use region_name_group = 'EMEA' as alternative |
| "Asia", "APAC" | `WHERE c.sub_region = 'APEC'` | Can use region_name_group = 'APEC' as alternative |
| "USA", "North America" | `WHERE c.sub_region = 'USA and Canada'` | Or use region_name_group = 'US/CAN' (different naming) |
| "Latin America", "LATAM" | `WHERE c.sub_region = 'LATAM'` | Includes ALL Latin countries |
| "Greater China" | `WHERE c.sub_region = 'Greater China'` | Maps to region_name_group = 'Other' |
| "Other", "Global App" | `WHERE c.sub_region = 'Other'` | - |

**For specific countries**: Filter by country_name or business_unit, NOT by region

**For global queries**: No region filter, but still include region_name_group and sub_region in SELECT/GROUP BY

---

## What Remains Unchanged

### CRITICAL QUERY RULES (Lines 4473-4494)
✅ These rules are correct and unchanged:

1. **ALWAYS include BOTH region_name_group AND sub_region in SELECT**
   ```sql
   SELECT
     c.region_name_group,  -- Always include for context
     c.sub_region,          -- Primary regional field
     -- other fields
   ```

2. **SUB_REGION is the PRIMARY filter field**
   - Filter by c.sub_region for specific regions

3. **Add clarifying note in response**

4. **GROUP BY both fields**
   ```sql
   GROUP BY c.region_name_group, c.sub_region
   ```

### REGION_NAME_GROUP Section (Lines 4496-4504)
✅ Correctly describes the 5 values: EMEA, APEC, US/CAN, LATAM, Other

---

## Impact on Query Generation

### Before Update:
```sql
-- INCORRECT - Would try to filter by non-existent values
SELECT ...
FROM ...
WHERE c.sub_region = 'Nordics'  -- ❌ WRONG: This is a SALES_AREA value, not SUB_REGION
```

### After Update:
```sql
-- CORRECT - Uses actual SUB_REGION values
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  f.business_unit AS market,
  c.country_name,
  -- metrics
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region = 'EMEA'  -- ✅ CORRECT: Valid SUB_REGION value
GROUP BY c.region_name_group, c.sub_region, f.business_unit, c.country_name
```

---

## Example User Questions and Correct Queries

### Question 1: "Show me EMEA performance"
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
LEFT JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE (m.email_name NOT ILIKE '%sparkpost%' OR m.email_name IS NULL)
  AND c.sub_region = 'EMEA'
GROUP BY c.region_name_group, c.sub_region
```

### Question 2: "Compare APEC vs LATAM"
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_opens) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS open_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
LEFT JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE (m.email_name NOT ILIKE '%sparkpost%' OR m.email_name IS NULL)
  AND c.sub_region IN ('APEC', 'LATAM')
GROUP BY c.region_name_group, c.sub_region
ORDER BY total_sends DESC
```

### Question 3: "Show all regions performance"
```sql
SELECT
  c.region_name_group AS parent_region,
  c.sub_region,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
LEFT JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE (m.email_name NOT ILIKE '%sparkpost%' OR m.email_name IS NULL)
GROUP BY c.region_name_group, c.sub_region
ORDER BY total_sends DESC
```

---

## Verification Checklist

After uploading to Cortex Analyst, test these queries:

- [ ] "Show EMEA performance" → Should filter by sub_region = 'EMEA'
- [ ] "Compare APEC vs LATAM" → Should filter by sub_region IN ('APEC', 'LATAM')
- [ ] "Show USA and Canada" → Should filter by sub_region = 'USA and Canada'
- [ ] "Greater China performance" → Should filter by sub_region = 'Greater China'
- [ ] "Show all regions" → Should include region_name_group and sub_region in results
- [ ] All results should have both parent_region and sub_region columns

---

## Files Modified

1. **config/semantic.yaml**:
   - Lines 4506-4549: SUB_REGION section
   - Lines 4552-4591: Region Name Mapping section
   - Removed stray "- Other" line

---

## Related Documentation

- **VERIFIED_QUERIES_REGIONAL_UPDATE.md** - Details of 17 verified queries updated
- **CORTEX_UI_UPLOAD_GUIDE.md** - Instructions for uploading semantic.yaml
- **GEOGRAPHIC_HIERARCHY_REFERENCE.md** - Complete hierarchy reference

---

**Updated**: 2026-02-12
**Section**: module_custom_instructions > Regional Hierarchy
**Impact**: Ensures Cortex Analyst generates correct SQL using only region_name_group and sub_region
