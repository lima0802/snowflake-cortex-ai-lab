# V_DIM_COUNTRY Structure Update - Summary

## Overview

Updated the semantic model to reflect the new V_DIM_COUNTRY structure with a proper 3-level geographic hierarchy:
- **REGION_NAME_GROUP** (highest level)
- **SUB_REGION** (detailed sub-regional level) - **NEW FIELD**
- **COUNTRY_NAME** (most granular level)

---

## Changes Made

### 1. Replaced REGION with SUB_REGION

**Removed**:
- `REGION` field (old field that was ambiguous)

**Added**:
- `SUB_REGION` field with comprehensive descriptions and examples

### 2. Updated Field Definitions

#### **SUB_REGION** (NEW - lines 408-451)

**Field Name**: `SUB_REGION`

**Synonyms**:
- detailed_region
- geographic_sub_region
- market_region
- regional_segment
- sales_region_detail
- sub_region_name
- subregion

**Sample Values**:
```yaml
- Nordics
- Central Europe
- Western Europe
- Eastern Europe
- UK & Ireland
- APEC NSC
- APEC Importers
- Greater China
- USA and Canada
- LATAM NSC
- LATAM Importers
- EMEA Importers
```

**Description**:
Provides detailed sub-regional grouping within the higher-level REGION_NAME_GROUP. Examples organized by parent region with specific country listings.

---

#### **REGION_NAME_GROUP** (ENHANCED - lines 472-511)

**Enhanced Features**:
- Added "Hierarchy" explanation at the top
- Clarified it's the "highest-level" regional grouping
- Added new synonyms: `high_level_region`, `top_level_region`, `region`
- Updated sample values to include all 5 values: APEC, EMEA, US/CAN, LATAM, Other
- Added "Regional Coverage" section with detailed market listings
- Added note about when to use SUB_REGION instead

**Sample Values** (updated):
```yaml
- APEC
- EMEA
- US/CAN
- LATAM
- Other
```

---

### 3. Added Sub-Region Filters

Added **10 new filters** for detailed sub-regional analysis:

#### EMEA Sub-region Filters:
1. **nordics_subregion**
   - Synonyms: nordic, nordics, scandinavia, scandinavian, nordic_countries, etc.
   - Expression: `sub_region = 'Nordics'`
   - Countries: Sweden, Norway, Denmark, Finland, Iceland

2. **central_europe_subregion**
   - Synonyms: central_europe, central_eu, dach, dach_region, etc.
   - Expression: `sub_region = 'Central Europe'`
   - Countries: Germany, Netherlands, Switzerland, Austria

3. **western_europe_subregion**
   - Synonyms: western_europe, western_eu, west_europe, etc.
   - Expression: `sub_region = 'Western Europe'`
   - Countries: France, Spain, Italy, Portugal, Belgium

4. **uk_ireland_subregion**
   - Synonyms: uk_and_ireland, uk_ireland, british_isles, etc.
   - Expression: `sub_region = 'UK & Ireland'`
   - Countries: United Kingdom, Ireland

5. **eastern_europe_subregion**
   - Synonyms: eastern_europe, eastern_eu, east_europe, etc.
   - Expression: `sub_region = 'Eastern Europe'`
   - Countries: Poland, Greece, Turkey, Russia, South Africa, etc.

#### APEC Sub-region Filters:
6. **apec_nsc_subregion**
   - Synonyms: apec_nsc, apac_nsc, apec_national_sales_companies, etc.
   - Expression: `sub_region = 'APEC NSC'`
   - Countries: Japan, Korea, Australia, Thailand, Malaysia, India, Bangladesh

7. **apec_importers_subregion**
   - Synonyms: apec_importers, apac_importers, asia_pacific_importers, etc.
   - Expression: `sub_region = 'APEC Importers'`
   - Countries: Singapore, Philippines, Vietnam, New Zealand, etc.

#### Other Sub-region Filters:
8. **greater_china_subregion**
   - Synonyms: greater_china, china_region, greater_china_region
   - Expression: `sub_region = 'Greater China'`
   - Countries: China, Taiwan, Hong Kong

#### LATAM Sub-region Filters:
9. **latam_nsc_subregion**
   - Synonyms: latam_nsc, latam_national_sales_companies, etc.
   - Expression: `sub_region = 'LATAM NSC'`
   - Countries: Mexico, Brazil

10. **latam_importers_subregion**
    - Synonyms: latam_importers, latin_america_importers, etc.
    - Expression: `sub_region = 'LATAM Importers'`
    - Countries: Argentina, Chile, Colombia, etc.

---

### 4. Updated Regional Filters

#### **emea_region** (UPDATED - line 588-608)

**Changes**:
- Removed sub-region-specific synonyms (moved to dedicated filters)
- Removed: `nordic`, `nordics`, `western_europe`, `eastern_europe`, and specific country names
- Kept high-level synonyms: `emea`, `eu`, `europe`, `european`, `middle_east`, `africa`
- Updated description to clarify it's for the entire EMEA region

**New Description**:
"Filters for Europe, Middle East, and Africa (EMEA) region markets at the highest level. For specific sub-regions like Nordics, Central Europe, or Western Europe, use the corresponding sub-region filters instead."

---

### 5. Updated Instructions

#### **instructions_default.md** (lines 428-462)

**Old Section**: "REGIONAL MAPPING (use REGION_NAME_GROUP)"
**New Section**: "REGIONAL HIERARCHY"

**New Content Structure**:
```
REGIONAL HIERARCHY:

**Hierarchy**: REGION_NAME_GROUP (highest) > SUB_REGION (detailed) > COUNTRY_NAME (most granular)

**REGION_NAME_GROUP** (Top-level regions):
[5 top-level regions with descriptions]

**SUB_REGION** (Detailed sub-regions):
[Organized by parent region with country listings]

**Usage**:
- For high-level regional queries: Use REGION_NAME_GROUP
- For detailed sub-regional queries: Use SUB_REGION
- Always join via: fact.business_unit = V_DIM_COUNTRY.vc_country_code
```

---

#### **semantic.yaml SQL Generation** (lines 4528-4585)

**Enhanced Section**: "Regional Hierarchy"

**New Content**:
- Replaced "Regional Groupings" with "Regional Hierarchy"
- Added hierarchy explanation
- Added separate sections for REGION_NAME_GROUP and SUB_REGION
- Included comprehensive sub-region listings organized by parent region
- Added usage guidance for each level
- Added example queries for both levels

---

### 6. Updated Best Practices

#### **semantic.yaml** (line 5013)

**Old**:
```
Use V_DIM_COUNTRY table to get COUNTRY_NAME and REGION_NAME_GROUP.
```

**New**:
```
Use V_DIM_COUNTRY table to get COUNTRY_NAME, SUB_REGION, and REGION_NAME_GROUP.
```

#### **semantic.yaml** (line 5045)

**Old**:
```
Join with V_DIM_COUNTRY to include country_name and region_name_group
```

**New**:
```
Join with V_DIM_COUNTRY to include country_name, sub_region, and region_name_group
```

---

## New Geographic Hierarchy

### Level 1: REGION_NAME_GROUP (5 values)
```
EMEA
├── APEC
├── US/CAN
├── LATAM
└── Other
```

### Level 2: SUB_REGION (13+ values)

**EMEA Sub-regions**:
- Nordics
- Central Europe
- Western Europe
- UK & Ireland
- Eastern Europe
- EMEA Importers

**APEC Sub-regions**:
- APEC NSC
- APEC Importers

**Greater China Sub-region**:
- Greater China (under 'Other' in REGION_NAME_GROUP)

**USA and Canada Sub-region**:
- USA and Canada

**LATAM Sub-regions**:
- LATAM NSC
- LATAM Importers

### Level 3: COUNTRY_NAME (120+ countries)

---

## Query Examples

### High-Level Regional Query
```sql
-- Question: "Compare performance across regions"
SELECT
  c.region_name_group,
  SUM(f.sends) AS total_sends,
  SUM(f.unique_clicks) AS total_clicks
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE ...
GROUP BY c.region_name_group
```

### Detailed Sub-Regional Query
```sql
-- Question: "Show Nordics vs Central Europe performance"
SELECT
  c.sub_region,
  SUM(f.sends) AS total_sends,
  SUM(f.unique_clicks) AS total_clicks
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region IN ('Nordics', 'Central Europe')
GROUP BY c.sub_region
```

### Country-Level Query
```sql
-- Question: "Compare Germany vs France performance"
SELECT
  c.country_name,
  c.sub_region,
  c.region_name_group,
  SUM(f.sends) AS total_sends,
  SUM(f.unique_clicks) AS total_clicks
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.vc_country_code IN ('VCDE', 'VCFR')
GROUP BY c.country_name, c.sub_region, c.region_name_group
```

---

## Natural Language Mapping

### User Says → Use Filter

| User Question | Level | Filter |
|---------------|-------|--------|
| "Show Europe performance" | Top-level | `region_name_group = 'EMEA'` |
| "Show Nordics performance" | Sub-regional | `sub_region = 'Nordics'` |
| "Show Sweden performance" | Country | `vc_country_code = 'VCSE'` |
| "Compare EMEA vs APEC" | Top-level | `region_name_group IN ('EMEA', 'APEC')` |
| "Compare Nordics vs Central Europe" | Sub-regional | `sub_region IN ('Nordics', 'Central Europe')` |
| "Show Asian markets" | Top-level | `region_name_group = 'APEC'` |
| "Show APEC NSC markets" | Sub-regional | `sub_region = 'APEC NSC'` |
| "Show Western Europe" | Sub-regional | `sub_region = 'Western Europe'` |
| "Show Greater China" | Sub-regional | `sub_region = 'Greater China'` |

---

## Files Modified

1. **semantic.yaml**
   - Lines 408-451: Added SUB_REGION field (replaced REGION)
   - Lines 472-511: Enhanced REGION_NAME_GROUP description
   - Lines 646-745: Added 10 new sub-region filters
   - Lines 588-608: Updated emea_region filter
   - Lines 4528-4585: Enhanced Regional Hierarchy section
   - Line 5013: Updated Best Practices
   - Line 5045: Updated market performance guidelines

2. **instructions_default.md**
   - Lines 428-462: Replaced REGIONAL MAPPING with REGIONAL HIERARCHY

---

## Testing Recommendations

After deploying these changes, test with:

### Top-Level Regional Queries:
- ✅ "Compare performance across regions"
- ✅ "Show EMEA performance"
- ✅ "APEC vs US/CAN comparison"

### Sub-Regional Queries:
- ✅ "Show Nordics performance"
- ✅ "Compare Central Europe vs Western Europe"
- ✅ "APEC NSC markets performance"
- ✅ "Show Greater China engagement"

### Country-Level Queries:
- ✅ "Germany vs France comparison"
- ✅ "Show Sweden click rate"
- ✅ "UK performance"

### Mixed-Level Queries:
- ✅ "Show Nordics countries breakdown" (should list Sweden, Norway, Denmark, Finland, Iceland)
- ✅ "Compare EMEA sub-regions" (should show Nordics, Central Europe, Western Europe, etc.)

---

## Benefits

1. **Clearer Hierarchy**: 3-level structure (Region > Sub-region > Country) is more intuitive
2. **Better Granularity**: Users can analyze at the appropriate level (not too broad, not too granular)
3. **Improved Filters**: 10 new sub-region filters for detailed analysis
4. **Enhanced Synonyms**: More natural language mappings (e.g., "Scandinavia" → Nordics)
5. **Consistent Naming**: Removed ambiguous "REGION" field, replaced with clear "SUB_REGION"
6. **Better Documentation**: Comprehensive descriptions with country listings

---

## Migration Notes

### Breaking Changes
- **REGION field removed**: Any queries using the old `REGION` field will need to be updated to use `SUB_REGION` instead
- **Region filter semantics changed**: The `emea_region` filter now applies only to top-level EMEA, not sub-regions

### Backwards Compatibility
- **REGION_NAME_GROUP unchanged**: All existing queries using this field will continue to work
- **Join logic unchanged**: Still use `fact.business_unit = V_DIM_COUNTRY.vc_country_code`

---

**Created**: 2026-02-12
**By**: Claude Code Assistant
**Change Type**: Data Model Structure Update
