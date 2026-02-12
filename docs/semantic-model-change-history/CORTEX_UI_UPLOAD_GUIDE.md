# Cortex Analyst UI Upload Guide

## Problem: Copy/Paste Issues

When pasting large semantic models into Cortex Analyst UI, you may encounter:
- ❌ "Unable to obtain result for query" errors
- ❌ UI freezing or timing out
- ❌ Incomplete paste (file truncated)
- ❌ Encoding/formatting issues

**Root Cause**: The semantic.yaml file is **~5MB / 68,000+ tokens**, which exceeds comfortable copy/paste limits for browser UIs.

---

## ✅ Solution 1: Upload via Snowflake Stage (RECOMMENDED)

### Step 1: Create a Stage
```sql
-- In Snowflake worksheet
USE DATABASE DEV_MARCOM_DB;
USE SCHEMA APP_DIRECTMARKETING;

CREATE STAGE IF NOT EXISTS semantic_models
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Storage for Cortex Analyst semantic models';
```

### Step 2: Upload File to Stage

**Option A: Using SnowSQL CLI**
```bash
snowsql -a <your_account> -u <username> -d DEV_MARCOM_DB -s APP_DIRECTMARKETING

PUT file://C:/Users/LiMa/OneDrive - WPP Cloud/Documentos/Li/05_Project/01_Volvo/DIA/snowflake-cortex-ai-lab/config/semantic.yaml @semantic_models/
  AUTO_COMPRESS=FALSE
  OVERWRITE=TRUE;
```

**Option B: Using Snowflake Web UI**
1. Navigate to **Data** → **Databases** → **DEV_MARCOM_DB** → **APP_DIRECTMARKETING**
2. Click on **Stages**
3. Click on **semantic_models** stage
4. Click **"+ Files"** button
5. Upload `semantic.yaml`

### Step 3: Verify Upload
```sql
LIST @semantic_models;
```

Should show:
```
semantic_models/semantic.yaml  |  5242880  |  ...
```

### Step 4: Reference in Cortex Analyst

In Cortex Analyst, use the stage path:
```
@DEV_MARCOM_DB.APP_DIRECTMARKETING.semantic_models/semantic.yaml
```

Or if in the same database/schema:
```
@semantic_models/semantic.yaml
```

---

## ✅ Solution 2: File Upload (If Available)

If Cortex Analyst UI has a file upload button:

1. Click **"Upload"** or **"Browse"** button
2. Select `semantic.yaml` from your local drive
3. Wait for upload to complete (may take 30-60 seconds for large files)

**Advantages**:
- ✅ No size limits
- ✅ No encoding issues
- ✅ Handles special characters correctly

---

## ✅ Solution 3: Test with Minimal Version First

I've created a minimal test file: **`semantic_minimal_test.yaml`**

**Use this to test**:
1. Copy the content of `semantic_minimal_test.yaml`
2. Paste into Cortex Analyst UI
3. If it works, the issue is file size

**If minimal version works**:
- The issue is file size
- Use Stage upload method for full file

**If minimal version fails**:
- The issue is configuration
- Check Cortex Analyst permissions
- Verify database/schema access

---

## ✅ Solution 4: Split into Modules (Advanced)

For very large models, split into sections:

**Main file** (semantic.yaml):
```yaml
name: SFMC_EMAIL_PERFORMANCE_DEV
description: Main semantic model

# Import other files
includes:
  - path: @semantic_models/tables/dimensions.yaml
  - path: @semantic_models/tables/facts.yaml
  - path: @semantic_models/queries/verified_queries.yaml
```

**Note**: Check if Cortex Analyst supports `includes` directive (may vary by version).

---

## Copy/Paste Best Practices (If You Must)

If you must copy/paste, follow these steps:

### Before Copying:

1. **Check file size**:
   ```bash
   # In command line
   dir "semantic.yaml"
   ```
   - ⚠️ If > 2MB, use Stage upload instead

2. **Remove unnecessary content** (temporarily):
   - Comment out large verified_queries sections
   - Remove extensive sample_values
   - Simplify descriptions

3. **Validate YAML**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('semantic.yaml'))"
   ```

### During Copy/Paste:

1. **Open file in proper text editor**:
   - ✅ VS Code, Notepad++, Sublime Text
   - ❌ NOT Word, WordPad

2. **Select All** (`Ctrl+A`) → **Copy** (`Ctrl+C`)

3. **Clear Cortex UI field** before pasting

4. **Paste** (`Ctrl+V`) and **wait**:
   - May take 10-30 seconds for large files
   - Don't click anything during paste

5. **Scroll to bottom** to verify complete paste

### After Pasting:

1. **Check for truncation**:
   - Scroll to end
   - Verify last line is complete

2. **Save/Apply** immediately

3. **Check for errors** in Cortex UI

---

## Common Issues & Fixes

### Issue 1: "Maximum size exceeded"
**Cause**: File too large for UI paste
**Fix**: Use Stage upload method

### Issue 2: "YAML parse error"
**Cause**: Special characters corrupted during paste
**Fix**:
- Save file as UTF-8 without BOM
- Use file upload instead of paste

### Issue 3: Paste appears truncated
**Cause**: Browser clipboard limit
**Fix**:
- Use Stage upload
- Or split into smaller sections

### Issue 4: UI freezes during paste
**Cause**: File too large for browser memory
**Fix**:
- Use Stage upload
- Or use minimal version first

### Issue 5: "Unable to obtain result"
**Cause**: Query in semantic model is too complex or returns too many rows
**Fix**:
- Add LIMIT clauses to verified queries
- Simplify complex queries
- See CORTEX_ERROR_TROUBLESHOOTING.md

---

## Verification Steps

After upload, verify it works:

### Test 1: Check Model Loaded
```sql
-- In Cortex Analyst, ask:
"What tables are available?"
```

**Expected**: Should list V_DIM_COUNTRY, V_FACT_SFMC_PERFORMANCE_TRACKING, etc.

### Test 2: Simple Query
```sql
-- Ask Cortex:
"What countries are available?"
```

**Expected**: Should return list of countries with regions

### Test 3: Performance Query
```sql
-- Ask Cortex:
"Show performance by region"
```

**Expected**: Should return regional performance breakdown

---

## File Size Guidelines

| Size | Method | Speed | Reliability |
|------|--------|-------|-------------|
| < 500 KB | Copy/Paste | Fast ⚡ | High ✅ |
| 500 KB - 2 MB | File Upload | Medium ⏱️ | High ✅ |
| 2 MB - 10 MB | Stage Upload | Slow 🐌 | High ✅ |
| > 10 MB | Split/Optimize | Slow 🐌 | Medium ⚠️ |

**Current file**: ~5 MB → **Use Stage Upload**

---

## Quick Command Reference

### Upload to Stage:
```sql
-- Create stage
CREATE STAGE semantic_models;

-- Upload file (SnowSQL)
PUT file://path/to/semantic.yaml @semantic_models/ AUTO_COMPRESS=FALSE;

-- List files
LIST @semantic_models;

-- Use in Cortex
@semantic_models/semantic.yaml
```

### Check File Size:
```bash
# Windows
dir semantic.yaml

# Linux/Mac
ls -lh semantic.yaml
```

### Validate YAML:
```bash
python -c "import yaml; yaml.safe_load(open('semantic.yaml'))"
```

---

## Next Steps

1. **Test minimal version first**: Use `semantic_minimal_test.yaml` to verify Cortex works
2. **If minimal works**: Upload full `semantic.yaml` via Stage
3. **If issues persist**: Check CORTEX_ERROR_TROUBLESHOOTING.md

---

## Files for Testing

1. **`semantic.yaml`** - Full production model (~5MB)
2. **`semantic_minimal_test.yaml`** - Minimal test model (~2KB)

**Recommendation**:
- Test with minimal version first (copy/paste OK)
- Deploy full version via Stage upload

---

**Created**: 2026-02-12
**File Size Issue**: Large YAML files in browser UI
**Best Solution**: Snowflake Stage upload
