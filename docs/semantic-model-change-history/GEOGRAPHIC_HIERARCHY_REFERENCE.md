# Geographic Hierarchy - Quick Reference

## Hierarchy Structure

```
REGION_NAME_GROUP (Top Level)
    └── SUB_REGION (Detailed Level)
            └── COUNTRY_NAME (Granular Level)
```

---

## Complete Hierarchy Map

### 🌍 EMEA Region

#### Nordics
- 🇸🇪 Sweden (VCSE)
- 🇳🇴 Norway (VCNO)
- 🇩🇰 Denmark (VCDK)
- 🇫🇮 Finland (VCFI)
- 🇮🇸 Iceland (VCIS)

#### Central Europe
- 🇩🇪 Germany (VCDE)
- 🇳🇱 Netherlands (VCNL)
- 🇨🇭 Switzerland (VCCH)
- 🇦🇹 Austria (VCAT)

#### Western Europe
- 🇫🇷 France (VCFR)
- 🇪🇸 Spain (VCES)
- 🇮🇹 Italy (VCIT)
- 🇵🇹 Portugal (VCPT)
- 🇧🇪 Belgium (VCBE)

#### UK & Ireland
- 🇬🇧 United Kingdom (VCUK)
- 🇮🇪 Ireland (VCIE)

#### Eastern Europe
- 🇵🇱 Poland (VCPL)
- 🇬🇷 Greece (VCGR)
- 🇹🇷 Turkey (VCTR)
- 🇷🇺 Russia (VCRU)
- 🇿🇦 South Africa (VCZA)
- And other Eastern European markets...

#### EMEA Importers
- Smaller EMEA markets served through importers

---

### 🌏 APEC Region

#### APEC NSC (National Sales Companies)
- 🇯🇵 Japan (VCJP)
- 🇰🇷 South Korea (VCKR)
- 🇦🇺 Australia (VCAU)
- 🇹🇭 Thailand (VCTH)
- 🇲🇾 Malaysia (VCMY)
- 🇮🇳 India (VCIN)
- 🇧🇩 Bangladesh (VCBD)

#### APEC Importers
- 🇸🇬 Singapore (VCSG)
- 🇵🇭 Philippines (VCPH)
- 🇻🇳 Vietnam (VCVN)
- 🇳🇿 New Zealand (VCNZ)
- And other smaller APEC markets...

---

### 🌎 US/CAN Region

#### USA and Canada
- 🇺🇸 United States (VCUS)
- 🇨🇦 Canada (VCCA)

---

### 🌎 LATAM Region

#### LATAM NSC (National Sales Companies)
- 🇲🇽 Mexico (VCMX)
- 🇧🇷 Brazil (VCBR)

#### LATAM Importers
- 🇦🇷 Argentina (VCAR)
- 🇨🇱 Chile (VCCL)
- 🇨🇴 Colombia (VCCO)
- And other Latin American markets...

---

### 🌐 Other

#### Greater China
- 🇨🇳 China (VCCN)
- 🇹🇼 Taiwan (VCTW)
- 🇭🇰 Hong Kong (VCHK)

#### Special
- 🌍 Global (VDDM) - Global App
- 🌐 Multi-market (VMM) - Multi-market app
- 🏢 Global Major Accounts (VCGF)
- 🚗 GSS (VCZZ) - Special Vehicles & GSS

---

## Field Guide

| Field | Level | Data Type | Values | Use When |
|-------|-------|-----------|--------|----------|
| **REGION_NAME_GROUP** | Top | VARCHAR(100) | EMEA, APEC, US/CAN, LATAM, Other | High-level regional queries |
| **SUB_REGION** | Detailed | VARCHAR(100) | Nordics, Central Europe, etc. | Sub-regional analysis |
| **COUNTRY_NAME** | Granular | VARCHAR(200) | Sweden, Germany, Japan, etc. | Country-level analysis |
| **VC_COUNTRY_CODE** | Key | VARCHAR(202) | VCSE, VCDE, VCJP, etc. | Joining to fact tables |

---

## Join Pattern

```sql
-- Standard join from fact to country dimension
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c
  ON f.business_unit = c.vc_country_code
```

---

## Query Patterns

### Pattern 1: Top-Level Regional Analysis
```sql
-- "Compare regions"
SELECT
  c.region_name_group,
  COUNT(DISTINCT m.email_name) AS campaigns,
  SUM(f.sends) AS total_sends
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
LEFT JOIN V_DIM_SFMC_METADATA_JOB m ON f.comp_key = m.comp_key
GROUP BY c.region_name_group
ORDER BY total_sends DESC
```

### Pattern 2: Sub-Regional Analysis
```sql
-- "Show Nordics vs Central Europe"
SELECT
  c.sub_region,
  c.region_name_group,
  SUM(f.sends) AS total_sends,
  ROUND(SUM(f.unique_clicks) * 100.0 / NULLIF(SUM(f.sends) - SUM(f.bounces), 0), 1) AS click_rate
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.sub_region IN ('Nordics', 'Central Europe')
GROUP BY c.sub_region, c.region_name_group
```

### Pattern 3: Country-Level with Hierarchy
```sql
-- "Show all EMEA countries with their sub-regions"
SELECT
  c.country_name,
  c.sub_region,
  c.region_name_group,
  SUM(f.sends) AS total_sends
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.region_name_group = 'EMEA'
GROUP BY c.country_name, c.sub_region, c.region_name_group
ORDER BY c.sub_region, total_sends DESC
```

### Pattern 4: Drill-Down Analysis
```sql
-- "Show performance hierarchy for EMEA"
-- Top level
SELECT 'Region' AS level, c.region_name_group AS name, SUM(f.sends) AS sends
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.region_name_group = 'EMEA'
GROUP BY c.region_name_group

UNION ALL

-- Sub-region level
SELECT 'Sub-Region' AS level, c.sub_region AS name, SUM(f.sends) AS sends
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.region_name_group = 'EMEA'
GROUP BY c.sub_region

UNION ALL

-- Country level (top 10)
SELECT 'Country' AS level, c.country_name AS name, SUM(f.sends) AS sends
FROM V_FACT_SFMC_PERFORMANCE_TRACKING f
INNER JOIN V_DIM_COUNTRY c ON f.business_unit = c.vc_country_code
WHERE c.region_name_group = 'EMEA'
GROUP BY c.country_name
ORDER BY sends DESC
LIMIT 10
```

---

## Natural Language Guide

| User Says | Use Field | Filter Value |
|-----------|-----------|--------------|
| "Europe" / "EMEA" | REGION_NAME_GROUP | = 'EMEA' |
| "Asia" / "APEC" | REGION_NAME_GROUP | = 'APEC' |
| "Nordics" / "Scandinavia" | SUB_REGION | = 'Nordics' |
| "Central Europe" / "DACH" | SUB_REGION | = 'Central Europe' |
| "Western Europe" | SUB_REGION | = 'Western Europe' |
| "UK and Ireland" | SUB_REGION | = 'UK & Ireland' |
| "Eastern Europe" | SUB_REGION | = 'Eastern Europe' |
| "APEC NSC" | SUB_REGION | = 'APEC NSC' |
| "Greater China" | SUB_REGION | = 'Greater China' |
| "Sweden" | COUNTRY_NAME | = 'Sweden' |
| "Germany" | VC_COUNTRY_CODE | = 'VCDE' |

---

## Filter Synonyms Quick Lookup

### Region Filters
- **emea_region**: `emea`, `europe`, `european`, `eu`
- **apac_region**: `apac`, `asia`, `asia_pacific`, `apec`, `pacific`
- **us_can_region**: `usa`, `us`, `america`, `canada`, `north_america`
- **latam_region**: `latam`, `latin_america`, `south_america`

### Sub-Region Filters
- **nordics_subregion**: `nordics`, `nordic`, `scandinavia`, `scandinavian`
- **central_europe_subregion**: `central_europe`, `dach`, `central_eu`
- **western_europe_subregion**: `western_europe`, `west_europe`, `western_eu`
- **uk_ireland_subregion**: `uk_ireland`, `uk_and_ireland`, `british_isles`
- **eastern_europe_subregion**: `eastern_europe`, `east_europe`, `eastern_eu`
- **apec_nsc_subregion**: `apec_nsc`, `apac_nsc`
- **apec_importers_subregion**: `apec_importers`, `apac_importers`
- **greater_china_subregion**: `greater_china`, `china_region`
- **latam_nsc_subregion**: `latam_nsc`
- **latam_importers_subregion**: `latam_importers`

---

## Common Mistakes to Avoid

### ❌ DON'T
```sql
-- Don't filter by old REGION field (removed)
WHERE c.region = 'EMEA'

-- Don't confuse levels
WHERE c.region_name_group = 'Nordics'  -- Nordics is SUB_REGION, not REGION_NAME_GROUP
```

### ✅ DO
```sql
-- Use correct hierarchy level
WHERE c.region_name_group = 'EMEA'

-- Use sub-region for detailed filtering
WHERE c.sub_region = 'Nordics'

-- Use proper join key
INNER JOIN V_DIM_COUNTRY c
  ON f.business_unit = c.vc_country_code
```

---

## Validation Checklist

Before executing a geographic query:

- [ ] **Level selection**: Am I using the right hierarchy level?
  - Top-level comparison → Use REGION_NAME_GROUP
  - Sub-regional analysis → Use SUB_REGION
  - Country-specific → Use COUNTRY_NAME or VC_COUNTRY_CODE

- [ ] **Join correctness**: Am I joining correctly?
  - [ ] Using INNER JOIN (not LEFT JOIN unless specifically needed)
  - [ ] Joining on business_unit = vc_country_code

- [ ] **Filter accuracy**: Are my filters at the right level?
  - [ ] EMEA/APEC/LATAM → REGION_NAME_GROUP
  - [ ] Nordics/Central Europe → SUB_REGION
  - [ ] Sweden/Germany → COUNTRY_NAME or VC_COUNTRY_CODE

---

## Pro Tips

1. **Use hierarchy in GROUP BY for drill-down**:
   ```sql
   GROUP BY c.region_name_group, c.sub_region, c.country_name
   ```

2. **Order by hierarchy for better readability**:
   ```sql
   ORDER BY c.region_name_group, c.sub_region, c.country_name
   ```

3. **Include all levels in SELECT for context**:
   ```sql
   SELECT
     c.country_name,
     c.sub_region,
     c.region_name_group,
     -- metrics
   ```

4. **Use CASE statements for custom groupings**:
   ```sql
   CASE
     WHEN c.sub_region IN ('Nordics', 'Central Europe') THEN 'Northern EMEA'
     WHEN c.sub_region IN ('Western Europe', 'Eastern Europe') THEN 'Southern EMEA'
   END AS custom_group
   ```

---

**Quick Tip**: When in doubt about the level, remember:
- **Continent/region?** → REGION_NAME_GROUP
- **Sub-region/area?** → SUB_REGION
- **Specific country?** → COUNTRY_NAME

---

**Created**: 2026-02-12
**Version**: 1.0
