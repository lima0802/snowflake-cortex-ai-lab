# Verified Queries - Regional Fields Update

## Summary

✅ **Updated 17 verified queries** to include both `region_name_group` and `sub_region` fields for proper regional hierarchy display.

## Changes Applied

### Pattern Applied to All Queries:

**Before**:
```sql
SELECT
  f.business_unit AS market,
  c.country_name,
  -- metrics
FROM ...
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
GROUP BY f.business_unit, c.country_name
```

**After**:
```sql
SELECT
  c.region_name_group AS parent_region,  -- ✅ ADDED
  c.sub_region,                          -- ✅ ADDED
  f.business_unit AS market,
  c.country_name,
  -- metrics
FROM ...
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
GROUP BY c.region_name_group, c.sub_region, f.business_unit, c.country_name  -- ✅ UPDATED
```

---

## Queries Updated

### 1. Regional Performance Queries

#### ✅ PERFORMANCE_SUMMARY_APAC
- **Question**: "Show me the email performance summary for Asia Pacific region"
- **Changes**: Added `parent_region` and `sub_region` to SELECT and GROUP BY

#### ✅ PERFORMANCE_SUMMARY_LATAM
- **Question**: "Show me the email performance for Latin America"
- **Changes**: Added both regional fields

#### ✅ PERFORMANCE_SUMMARY_USCAN
- **Question**: "Show me email performance in US and Canada"
- **Changes**: Added both regional fields

#### ✅ REGIONAL_PERFORMANCE_COMPARISON
- **Question**: "How do the different regions compare in email performance?"
- **Changes**: Added `parent_region` and `sub_region` to all groupings

---

### 2. Market Comparison Queries

#### ✅ MARKET_COMPARISON_FR_ES_IT
- **Question**: "Compare open rates for France, Spain, and Italy"
- **Changes**: Added both regional fields to show these markets are in EMEA region

#### ✅ EX30_NL_VS_BE_COMPARISON
- **Question**: "Compare open and click rates for EX30 campaigns in NL versus BE"
- **Changes**: Added regional hierarchy context

#### ✅ REGION_COMPARISON_EMEA_VS_APAC
- **Question**: "How does EMEA compare to APAC in email performance?"
- **Changes**: Added `parent_region` and `sub_region` to show breakdown by sub-regions

---

### 3. Performance Analysis Queries

#### ✅ BOTTOM_PERFORMING_MARKETS
- **Question**: "Which markets have the lowest click rate?"
- **Changes**: Added regional context to identify which region low performers belong to

#### ✅ HIGH_OPTOUT_MARKETS
- **Question**: "Which markets have high opt-out rates?"
- **Changes**: Added regional fields to understand geographic patterns

#### ✅ BOUNCE_RATE_BY_MARKET
- **Question**: "What is the bounce rate by market?"
- **Changes**: Added regional hierarchy for context

---

### 4. Program Performance Queries

#### ✅ FIRST_YEAR_PROGRAM_PERFORMANCE
- **Question**: "How is the First Year Program performing?"
- **Changes**: Added regional fields to see performance by region

#### ✅ ORDER_TO_DELIVERY_PROGRAM_PERFORMANCE
- **Question**: "How is the Order to Delivery program performing?"
- **Changes**: Added regional hierarchy

#### ✅ LEAD_NURTURE_PROGRAM_PERFORMANCE
- **Question**: "How is the Lead Nurture program performing?"
- **Changes**: Added regional context

#### ✅ ENEWSLETTER_PERFORMANCE_BY_MARKET
- **Question**: "How are eNewsletters performing by market?"
- **Changes**: Added regional fields for geographic analysis

---

### 5. Benchmark Queries

#### ✅ MARKET_PERFORMANCE_VS_INDUSTRY_BENCHMARK
- **Question**: "How do markets compare to industry benchmark?"
- **Changes**: Updated CTE and final SELECT to include both regional fields

#### ✅ MARKET_PERFORMANCE_WITH_BENCHMARK_STATUS
- **Question**: "Show market performance with benchmark status"
- **Changes**: Added regional hierarchy throughout the query

#### ✅ REGIONAL_COMPARISON_NO_BENCHMARK
- **Question**: "Compare regional performance"
- **Changes**: Added both fields to SELECT and GROUP BY

---

## Benefits

### 1. **Complete Regional Context**
Users now see the full hierarchy:
```
| Parent Region | Sub-Region      | Market | Country  | Metric |
|---------------|-----------------|--------|----------|--------|
| EMEA          | Nordics         | VCSE   | Sweden   | 4.5%   |
| EMEA          | Central Europe  | VCDE   | Germany  | 4.2%   |
| APEC          | APEC NSC        | VCJP   | Japan    | 3.9%   |
```

### 2. **Better Grouping & Filtering**
Sub-regions can be compared within parent regions:
```sql
-- Now possible: Compare Nordics vs Central Europe within EMEA
WHERE c.region_name_group = 'EMEA'
  AND c.sub_region IN ('Nordics', 'Central Europe')
```

### 3. **Consistent Hierarchy**
All queries follow the same 3-level pattern:
- **REGION_NAME_GROUP** (parent_region) - EMEA, APEC, US/CAN, LATAM
- **SUB_REGION** - Nordics, Central Europe, Western Europe, APEC NSC, etc.
- **COUNTRY_NAME** - Individual countries

### 4. **Enhanced Analytics**
Enables drill-down analysis:
1. View by parent region (EMEA vs APEC)
2. Drill into sub-regions (Nordics vs Central Europe)
3. Drill into countries (Sweden vs Germany)

---

## Query Structure Template

All regional queries now follow this pattern:

```sql
SELECT
  -- ALWAYS include both regional fields at the top
  c.region_name_group AS parent_region,
  c.sub_region,

  -- Then market/country identifiers
  f.business_unit AS market,
  c.country_name,

  -- Then metrics
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate

FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
LEFT JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
LEFT JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code

WHERE (m.email_name NOT ILIKE '%sparkpost%' OR m.email_name IS NULL)
  AND [additional filters]

-- ALWAYS group by both regional fields
GROUP BY c.region_name_group, c.sub_region, f.business_unit, c.country_name

ORDER BY [sort criteria]
```

---

## Example Query Results

### Before Update:
```
| Market | Country  | Click Rate |
|--------|----------|------------|
| VCSE   | Sweden   | 4.5%       |
| VCDE   | Germany  | 4.2%       |
| VCJP   | Japan    | 3.9%       |
```
❌ Missing regional context - can't tell which region markets belong to

### After Update:
```
| Parent Region | Sub-Region      | Market | Country  | Click Rate |
|---------------|-----------------|--------|----------|------------|
| EMEA          | Nordics         | VCSE   | Sweden   | 4.5%       |
| EMEA          | Central Europe  | VCDE   | Germany  | 4.2%       |
| APEC          | APEC NSC        | VCJP   | Japan    | 3.9%       |
```
✅ Full context - users can see the complete hierarchy

---

## Verification Steps

To verify these changes work:

### 1. Test Regional Query
```sql
-- Ask Cortex: "Show me email performance for Asia Pacific"
-- Should return results with parent_region and sub_region columns
```

### 2. Test Market Comparison
```sql
-- Ask Cortex: "Compare France, Spain, and Italy"
-- Should show all three are in EMEA region, Western Europe sub-region
```

### 3. Test Hierarchy Grouping
```sql
-- Ask Cortex: "How do different regions compare?"
-- Should group by parent_region and sub_region
```

---

## Files Modified

1. **semantic.yaml** - 17 verified queries updated

## Queries NOT Modified

The following queries were not modified because they either:
- Don't involve market/country comparisons
- Use aggregated comparison logic
- Are already correctly structured
- Don't include V_DIM_COUNTRY joins

Examples:
- OVERALL_OPEN_RATE
- OVERALL_CLICK_RATE
- YTD_PERFORMANCE
- Campaign-specific queries without regional breakdown

---

## Testing Checklist

- [ ] Upload updated semantic.yaml to Cortex Analyst
- [ ] Test query: "Show performance for Asia Pacific"
- [ ] Test query: "Compare EMEA vs APEC"
- [ ] Test query: "Which markets have lowest click rate?"
- [ ] Test query: "How are programs performing by market?"
- [ ] Verify both parent_region and sub_region appear in all results
- [ ] Verify GROUP BY produces correct aggregations

---

## Next Steps

1. **Upload to Cortex**: Use Stage upload method (see CORTEX_UI_UPLOAD_GUIDE.md)
2. **Test Queries**: Run sample queries to verify results
3. **User Training**: Inform users about the new regional hierarchy in results
4. **Documentation**: Update any query documentation to reflect new column names

---

**Updated**: 2026-02-12
**Queries Modified**: 17
**Impact**: All regional/market comparison queries now include full geographic hierarchy
