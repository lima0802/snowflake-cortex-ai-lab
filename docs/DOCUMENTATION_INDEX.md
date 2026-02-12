# Snowflake Cortex AI Lab - Documentation Index

## 📁 Project Structure

```
snowflake-cortex-ai-lab/
├── config/
│   ├── semantic.yaml                    # Main semantic model configuration
│   ├── semantic_minimal_test.yaml       # Minimal test version
│   └── agents/
│       └── backup/
│           └── orchestration/
│               ├── instructions_default.md
│               └── response_default.md
│
├── docs/
│   ├── semantic-model-change-history/   # 📚 Adjustment history & references
│   │   ├── README.md                    # Index of all change documentation
│   │   ├── CAMPAIGN_FILTER_IMPROVEMENTS.md
│   │   ├── CAMPAIGN_FILTER_QUICK_REFERENCE.md
│   │   ├── V_DIM_COUNTRY_UPDATE_SUMMARY.md
│   │   ├── GEOGRAPHIC_HIERARCHY_REFERENCE.md
│   │   ├── SUB_REGION_PRIMARY_FIELD_UPDATE.md
│   │   ├── REGION_COLUMN_ERROR_FIX.md
│   │   ├── CORTEX_ERROR_TROUBLESHOOTING.md
│   │   ├── CORTEX_UI_UPLOAD_GUIDE.md
│   │   ├── VERIFIED_QUERIES_REGIONAL_UPDATE.md
│   │   └── MODULE_INSTRUCTIONS_REGIONAL_UPDATE.md
│   │
│   └── DOCUMENTATION_INDEX.md           # This file
│
├── AGENT_DEPLOYMENT_GUIDE.md            # Agent deployment instructions
├── WHY_USE_SNOWSIGHT.md                 # Snowsight usage guide
└── MIGRATION_SUMMARY.md                 # Migration notes
```

---

## 📚 Documentation Categories

### 🔧 Configuration Change History
**Location**: `docs/semantic-model-change-history/`

Complete history of all adjustments made to the semantic model configuration:
- Campaign filter enhancements
- Geographic hierarchy updates
- Query modifications
- Error fixes
- Troubleshooting guides

**Start here**: [semantic-model-change-history/README.md](./semantic-model-change-history/README.md)

---

### 🚀 Deployment Guides
**Location**: Project root

- **AGENT_DEPLOYMENT_GUIDE.md**: How to deploy Cortex agents
- **WHY_USE_SNOWSIGHT.md**: Snowsight benefits and usage
- **MIGRATION_SUMMARY.md**: Migration process notes

---

### ⚙️ Configuration Files
**Location**: `config/`

- **semantic.yaml**: Main semantic model (5MB, 68,000+ tokens)
- **semantic_minimal_test.yaml**: Minimal test version (2KB)
- **instructions_default.md**: Agent instructions
- **response_default.md**: Response formatting templates

---

## 🎯 Quick Start Guide

### For New Team Members:

1. **Understand the project setup**:
   - Read [AGENT_DEPLOYMENT_GUIDE.md](../AGENT_DEPLOYMENT_GUIDE.md)
   - Review [WHY_USE_SNOWSIGHT.md](../WHY_USE_SNOWSIGHT.md)

2. **Learn about recent changes**:
   - Start with [semantic-model-change-history/README.md](./semantic-model-change-history/README.md)
   - Read key references based on your needs

3. **Deploy or test**:
   - Follow [CORTEX_UI_UPLOAD_GUIDE.md](./semantic-model-change-history/CORTEX_UI_UPLOAD_GUIDE.md)
   - Use [CORTEX_ERROR_TROUBLESHOOTING.md](./semantic-model-change-history/CORTEX_ERROR_TROUBLESHOOTING.md) if issues arise

---

### For Troubleshooting:

**Issue**: Campaign filter not working correctly
→ See [CAMPAIGN_FILTER_QUICK_REFERENCE.md](./semantic-model-change-history/CAMPAIGN_FILTER_QUICK_REFERENCE.md)

**Issue**: Regional queries returning wrong data
→ See [GEOGRAPHIC_HIERARCHY_REFERENCE.md](./semantic-model-change-history/GEOGRAPHIC_HIERARCHY_REFERENCE.md)

**Issue**: "Unable to obtain result" error
→ See [CORTEX_ERROR_TROUBLESHOOTING.md](./semantic-model-change-history/CORTEX_ERROR_TROUBLESHOOTING.md)

**Issue**: File too large to upload
→ See [CORTEX_UI_UPLOAD_GUIDE.md](./semantic-model-change-history/CORTEX_UI_UPLOAD_GUIDE.md)

**Issue**: SQL compilation error
→ See [REGION_COLUMN_ERROR_FIX.md](./semantic-model-change-history/REGION_COLUMN_ERROR_FIX.md)

---

## 📖 Documentation Standards

### Change Documentation
All significant changes to the semantic model should be documented in `docs/semantic-model-change-history/`:

**Required sections**:
- Summary
- Changes made (before/after)
- Impact
- Examples
- Verification steps
- Date and author

### File Naming Convention
- `[FEATURE]_[ACTION].md` (e.g., `CAMPAIGN_FILTER_IMPROVEMENTS.md`)
- Use UPPERCASE for emphasis
- Use underscores between words
- Be descriptive but concise

---

## 🔄 Update Process

When making changes to the semantic model:

1. **Make changes** to config files
2. **Test changes** with minimal version first
3. **Document changes** in `semantic-model-change-history/`
4. **Update README.md** in change history folder
5. **Commit changes** with descriptive message

---

## 📊 Current Configuration Status

**Last Major Update**: 2026-02-12

### ✅ Completed:
- Campaign filter enhancements
- Geographic hierarchy restructure (REGION → SUB_REGION)
- All SALES_AREA references removed
- 17 verified queries updated
- module_custom_instructions corrected

### 🎯 Ready for:
- Deployment to Cortex Analyst
- User testing
- Production rollout

---

## 📧 Support

For questions or issues:
1. Check relevant documentation in `semantic-model-change-history/`
2. Review `CORTEX_ERROR_TROUBLESHOOTING.md` for common issues
3. Contact the semantic model configuration team

---

**Last Updated**: 2026-02-12
**Version**: 1.0
**Configuration Status**: Production Ready ✅
