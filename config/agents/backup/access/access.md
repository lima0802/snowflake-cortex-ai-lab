#  Agent Access Control

> **Purpose**: Defines who can access and interact with the Direct Marketing Analytics Agent across Dev and Prod environments.

---

## Roles and Permissions

### APP_DIRECTMARKETING Schema

#### PROD Environment
| Role | Schema | Agent | Snowflake Intelligence Display Name | Access Level | Description |
|------|--------|-------|--------------------------------------|--------------|-------------|
| `CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ETL-SG` | `APP_DIRECTMARKETING` | `SFMC_EMAIL_ANALYTICS_PROD_AGENT` | Direct Marketing Analytics PROD Agent | **Ownership / Full Access** | AI Developers and Data Engineers. Can develop, edit, and manage the PROD semantic view in Cortex Analyst. |
| `CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ANALYST-SG` | `APP_DIRECTMARKETING` | `SFMC_EMAIL_ANALYTICS_PROD_AGENT` | Direct Marketing Analytics PROD Agent | **Usage Only** | AI Developers + Business Stakeholders. Use the agent to ask questions. |

#### DEV Environment
| Role | Schema | Agent | Snowflake Intelligence Display Name | Access Level | Description |
|------|--------|-------|--------------------------------------|--------------|-------------|
| `CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ETL-SG` | `APP_DIRECTMARKETING` | `SFMC_EMAIL_ANALYTICS_AGENT` | Direct Marketing Analytics DEV Agent | **Ownership / Full Access** | AI Developers and Data Engineers. Can develop, edit, and manage the DEV semantic view in Cortex Analyst. |
| `CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ANALYST-SG` | `APP_DIRECTMARKETING` | `SFMC_EMAIL_ANALYTICS_AGENT` | Direct Marketing Analytics DEV Agent | **Usage Only** | Business Stakeholders. Use the agent to ask questions. |

---

### AGENT_DIRECTMARKETING Schema

#### PROD Environment
| Role | Schema | Agent | Snowflake Intelligence Display Name | Access Level | Description |
|------|--------|-------|--------------------------------------|--------------|-------------|
| `CLD-SNOWFLAKE-PROD-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG` | `AGENT_DIRECTMARKETING` | `AY_TEST_DIRECTMARKETING_ETL_AGENT` | Test - AY_TEST_DIRECTMARKETING_ETL_AGENT | **Usage Only** | Business Stakeholders. Same access pattern as APP_DIRECTMARKETING PROD roles, scoped to AGENT_DIRECTMARKETING schema. |

#### DEV Environment
| Role | Schema | Agent | Snowflake Intelligence Display Name | Access Level | Description |
|------|--------|-------|--------------------------------------|--------------|-------------|
| `CLD-SNOWFLAKE-DEV-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG` | `AGENT_DIRECTMARKETING` | `AY_TEST_DIRECTMARKETING_ETL_AGENT` | Test - AY_TEST_DIRECTMARKETING_ETL_AGENT | **Usage Only** | Business Stakeholders. Same access pattern as APP_DIRECTMARKETING DEV roles, scoped to AGENT_DIRECTMARKETING schema. |

---

## Specific User Access

*Primary developer/owner:*
- User: `lima0802`
- Access: Owner/Editor

---

##  How to Configure
In the **Access** tab in Snowsight:
1. Click **+ Add role**
2. Add the relevant Account Roles from the tables above.
3. Assign the appropriate permission levels (Ownership, Usage & Monitor, or Usage Only).

---

##  Grant Privileges

### APP_DIRECTMARKETING Schema
```sql
-- DEV Permissions (APP_DIRECTMARKETING)
GRANT USAGE ON AGENT DEV_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ETL-SG";
GRANT OWNERSHIP ON AGENT DEV_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ETL-SG";
GRANT USAGE ON AGENT DEV_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ANALYST-SG";
GRANT MONITOR ON AGENT DEV_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-APP-DIRECTMARKETING-ANALYST-SG";

-- PROD Permissions (APP_DIRECTMARKETING)
GRANT USAGE ON AGENT PROD_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_PROD_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ETL-SG";
GRANT OWNERSHIP ON AGENT PROD_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_PROD_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ETL-SG";
GRANT USAGE ON AGENT PROD_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_PROD_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ANALYST-SG";
GRANT MONITOR ON AGENT PROD_MARCOM_DB.APP_DIRECTMARKETING.SFMC_EMAIL_ANALYTICS_PROD_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ANALYST-SG";
```

### AGENT_DIRECTMARKETING Schema
```sql
-- DEV Permissions (AGENT_DIRECTMARKETING)
GRANT USAGE ON AGENT DEV_MARCOM_DB.AGENT_DIRECTMARKETING.AY_TEST_DIRECTMARKETING_ETL_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG";
GRANT MONITOR ON AGENT DEV_MARCOM_DB.AGENT_DIRECTMARKETING.AY_TEST_DIRECTMARKETING_ETL_AGENT TO ROLE "CLD-SNOWFLAKE-DEV-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG";

-- PROD Permissions (AGENT_DIRECTMARKETING)
GRANT USAGE ON AGENT PROD_MARCOM_DB.AGENT_DIRECTMARKETING.AY_TEST_DIRECTMARKETING_ETL_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG";
GRANT MONITOR ON AGENT PROD_MARCOM_DB.AGENT_DIRECTMARKETING.AY_TEST_DIRECTMARKETING_ETL_AGENT TO ROLE "CLD-SNOWFLAKE-PROD-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG";
```

---

## Testing Procedure

### APP_DIRECTMARKETING — PROD Agent

| Step | Action |
| :--- | :--- |
| **1** | Open: [Snowflake AI Enterprise](https://ai.snowflake.com/volvocars/enterprise/#/homepage) |
| **2** | Click the **User Icon** (bottom left) |
| **3** | Set role to: `CLD-SNOWFLAKE-PROD-MARCOM-APP-DIRECTMARKETING-ANALYST-SG` |
| **4** | Set warehouse to: `PROD_MARCOM_APP_DIRECTMARKETING_ANALYST_WHS` |
| **5** | Look for **"Direct Marketing Analytics PROD Agent"** in the chat |

### AGENT_DIRECTMARKETING — Test Agent

| Step | Action |
| :--- | :--- |
| **1** | Open: [Snowflake AI Enterprise](https://ai.snowflake.com/volvocars/enterprise/#/homepage) |
| **2** | Click the **User Icon** (bottom left) |
| **3** | Set role to: `CLD-SNOWFLAKE-DEV-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG` or `CLD-SNOWFLAKE-PROD-MARCOM-AGENT-DIRECTMARKETING-ANALYST-SG` |
| **4** | Set warehouse to: `DEV_MARCOM_AGENT_DIRECTMARKETING_ANALYST_WHS` or `PROD_MARCOM_AGENT_DIRECTMARKETING_ANALYST_WHS` |
| **5** | Look for **"Test - AY_TEST_DIRECTMARKETING_ETL_AGENT"** in the chat |

