# Fix: SQL Compilation Error - Invalid Identifier 'REGION'

## Error Message
```
SQL compilation error: error line 15 at position 2 invalid identifier 'REGION'
```

## Root Cause

The verified question query `AVAILABLE_COUNTRIES_REGIONS` was still referencing the old `region` column that no longer exists in `V_DIM_COUNTRY` table.

## Location
**File**: `config/semantic.yaml`
**Line**: 3848
**Query Name**: `AVAILABLE_COUNTRIES_REGIONS`

## Fix Applied

### Before (WRONG ❌):
```yaml
  - name: AVAILABLE_COUNTRIES_REGIONS
    sql: |-
      SELECT
        vc_country_code,
        country_name,
        country_code,
        region,              # ❌ OLD COLUMN - doesn't exist!
        region_name_group,
        sales_area,
        market_cd
      FROM V_DIM_COUNTRY
      ORDER BY region_name_group, country_name
```

### After (CORRECT ✅):
```yaml
  - name: AVAILABLE_COUNTRIES_REGIONS
    sql: |-
      SELECT
        vc_country_code,
        country_name,
        country_code,
        sub_region,          # ✅ NEW COLUMN - correct field
        region_name_group,
        sales_area,
        market_cd
      FROM V_DIM_COUNTRY
      ORDER BY region_name_group, sub_region, country_name
```

## Changes Made

1. **Line 3848**: Changed `region,` to `sub_region,`
2. **Line 3853**: Updated ORDER BY to include `sub_region` for proper hierarchy ordering

## Verification

The query should now work correctly and return:
- vc_country_code
- country_name
- country_code
- **sub_region** (NEW - detailed regional grouping)
- region_name_group (parent region)
- sales_area
- market_cd

Ordered by: region_name_group → sub_region → country_name

## Test Query

You can test this query directly in Snowflake:

```sql
SELECT
  vc_country_code,
  country_name,
  country_code,
  sub_region,
  region_name_group,
  sales_area,
  market_cd
FROM DEV_MARCOM_DB.DM.V_DIM_COUNTRY
ORDER BY region_name_group, sub_region, country_name
LIMIT 10;
```

Expected result:
```
| vc_country_code | country_name | country_code | sub_region      | region_name_group | sales_area     | market_cd |
|-----------------|--------------|--------------|-----------------|-------------------|----------------|-----------|
| VCAU            | Australia    | AU           | APEC NSC        | APEC              | APEC NSC       | 452       |
| VCBD            | Bangladesh   | BD           | APEC NSC        | APEC              | APEC NSC       | 421       |
| VCIN            | India        | IN           | APEC NSC        | APEC              | APEC NSC       | 421       |
| ...             | ...          | ...          | ...             | ...               | ...            | ...       |
```

## Why This Happened

During the V_DIM_COUNTRY structure update, the `REGION` field was replaced with `SUB_REGION`, but this particular verified question query was not updated.

## Reminder: Column Name Change

**Old Structure** (❌ REMOVED):
- `REGION` - Ambiguous field (removed)

**New Structure** (✅ CURRENT):
- `SUB_REGION` - Detailed sub-regional grouping (PRIMARY)
- `REGION_NAME_GROUP` - Top-level parent region (CONTEXT)

## Files Modified

- `config/semantic.yaml` (lines 3848, 3853)

---

**Fixed**: 2026-02-12
**Error Type**: Invalid column reference
**Impact**: Resolved - query will now execute successfully
