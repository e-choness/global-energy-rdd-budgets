**Dataset: IEA Energy Technology R&D and Budget Database**

**Source:**

- **Origin:** International Energy Agency (IEA) — Energy Technology RD&D & Budget Database
- **Original dataset URL:** https://www.iea.org/data-and-statistics/data-product/energy-technology-rd-and-d-budget-database-2

**Files in this folder:**

- **Filtered dataset:** [data/Energy-Technology-RD&amp;D-Budgets-Filtered.csv](src/data/Energy-Technology-RD&D-Budgets-Filtered.csv) — project-specific subset used in analysis and visualizations.
- **This file:** DATA_README.md (dataset notes and usage)

**Description:**

- The dataset contains research, development and demonstration (RD&D) budgets for energy technologies across economies and years as published by the IEA. Typical fields include year, economy (country/region), technology or technology group, budget/amount (monetary units), and source/notes. Please inspect the CSV headers to see the exact column names and any units used.

**How to load (Python / pandas):**

```python
````markdown
**Dataset: IEA Energy Technology RD&D and Budget Database (subset used here)**

**Source:**

- **Origin:** International Energy Agency (IEA) — Energy Technology RD&D & Budget Database
- **Original dataset page:** https://www.iea.org/data-and-statistics/data-product/energy-technology-rd-and-d-budget-database-2

**Files in this folder:**

- **Filtered dataset (used by the app):** [data/Energy-Technology-RD&D-Budgets-Filtered.csv](data/Energy-Technology-RD&D-Budgets-Filtered.csv)
- **This file:** DATA_README.md (dataset notes and usage)

**Quick description:**

- This repository contains a project-specific filtered subset of the IEA RD&D budgets table. Records include yearly public budgets for technology groups and economies, plus metadata about units and data quality.

**Typical columns (present in the filtered CSV):**

- `STRUCTURE`, `STRUCTURE_ID`, `STRUCTURE_NAME`
- `ACTION`
- `COUNTRY` / `Country/Region` (economy code and friendly name)
- `FREQUENCY` / `Frequency`
- `RDD_SECTOR` / `Sector`
- `RDD_TECH` / `Technology`
- `RDD_TYPE` / `Type`
- `UNIT` / `Unit` (e.g., `NC_N` meaning national currency nominal)
- `TIME_PERIOD` / `Time Period` (year)
- `OBS_VALUE` / `Observation value` (numeric budget amount)
- `QUALIFIER`, `CONF_STATUS` (quality / provisional flags)
- `UNIT_MULT` (unit multiplier hint, e.g., `6` with label "Millions")
- `DECIMALS` (reported decimals)

Inspect the CSV header to confirm exact column names before programmatic use.

**Units & monetary notes:**

- The IEA often reports nominal national currency values; the `UNIT` field and `UNIT_MULT`/`Unit multiplier` should be used to interpret `OBS_VALUE` correctly (for example, `UNIT_MULT` value `6` with label "Millions" implies values are in millions of local currency units). No currency conversion is performed in the repository — verify currency/unit choices before cross-country monetary comparisons.

**How the Streamlit app uses this file:**

- `streamlit_app.py` loads `data/Energy-Technology-RD&D-Budgets-Filtered.csv` and normalizes column names. In the app the following mappings are used:
	- `TIME_PERIOD` (or `Time Period`) → `Year` (integer)
	- `OBS_VALUE` (or `Observation value`) → `Value` (numeric)
	- `Country/Region`/`COUNTRY` → `Country`
	- `RDD_TECH`/`Technology` → `Technology`

- The app provides interactive filters: Year range slider, Country multi-select, Technology multi-select. Visualizations include:
	- Time series of total budgets by year (aggregated across filters)
	- Bar chart of budgets by technology (aggregated across the selected year range)
	- Pie chart of top countries by total budget (top 20)
	- Summary metrics and a downloadable filtered CSV

**Quick loading example (pandas):**

```python
import pandas as pd

df = pd.read_csv('data/Energy-Technology-RD&D-Budgets-Filtered.csv')
print(df.columns.tolist())
print(df[['TIME_PERIOD','OBS_VALUE','Country/Region','RDD_TECH']].head())
```

**Recommended validation steps before analysis:**

- Confirm the unit/multiplier (`UNIT`, `UNIT_MULT`, `Unit multiplier`) and, if required for comparisons, convert to a common currency and scale.
- Check for provisional or imputed values using `QUALIFIER` / `CONF_STATUS` and decide whether to include them.

**Citation & license:**

- Original data provided by the International Energy Agency (IEA). Follow the IEA terms of use and citation guidance when reusing data.

**Contact / provenance:**

- Repository: e-choness/m2m-capstone-01-energy-efficiency
- For questions about preprocessing in this repo, open an issue in the repository.
