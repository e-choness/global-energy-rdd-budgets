# Global Energy Technology RD&D Budget Analysis

This project aims to analyze and visualize global public Research, Development, and Demonstration (RD&D) budgets for energy technologies from 2020 to 2025. It will focus on identifying trends, comparing allocations across sectors and countries, and providing an interactive dashboard for data exploration.

## Features:

- Data Ingestion & Preprocessing
- Budget Trend Visualization over time
- Sectoral Budget Comparison
- Country-wise Budget Analysis
- [Interactive Dashboard](https://global-energy-rdd-budgets.streamlit.app/)

## Technologies:

Concise interactive dashboard for exploring public RD&D budgets by country, technology, and year (2020–2025). Data used in this project is derived from the International Energy Agency (IEA) Energy Technology RD&D & Budget Database.

Quick links

- Data: [data/Energy-Technology-RD&amp;D-Budgets-Filtered.csv](data/Energy-Technology-RD&D-Budgets-Filtered.csv)
- Data notes: [data/DATA_README.md](data/DATA_README.md)

Quick start

1. Create and activate a virtual environment (recommended).
   - Windows PowerShell: `python -m venv .venv` then `& .venv\Scripts\Activate.ps1`
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the interactive Streamlit app locally (the repository provides `streamlit_app.py`):

```powershell
streamlit run streamlit_app.py
```

Notes

- Source: IEA — https://www.iea.org/data-and-statistics/data-product/energy-technology-rd-and-d-budget-database-2
- The filtered CSV included in `data/` is used by the lightweight Streamlit app. The loader performs basic normalization and numeric parsing; verify units and currency if performing monetary comparisons.

Contributing

- Open an issue or submit a pull request on the repository for data fixes, schema updates, or feature requests.

Citation & license

- Data provided by the IEA — follow the IEA terms of use and citation guidance when reusing data.

Contact

- Repository: e-choness/m2m-capstone-01-energy-efficiency
- For questions about preprocessing, open an issue in the repo.
