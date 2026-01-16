# Project Overview: Global Energy RD&D Budgets Analysis

## 1. Executive Summary

This project aims to develop an interactive Streamlit application for analyzing global public Research, Development, and Demonstration (RD&D) budgets for energy technologies from 2020 to 2025. The application will provide users with a clear and intuitive platform to explore budget trends, compare allocations across technology sectors and countries, and identify key insights. The value proposition lies in enabling data-driven decision-making for energy policy, investment, and research strategy by making complex budget data accessible and understandable.

## 2. Scope Summary

**Included:**

* Ingestion and cleaning of raw global energy RD&D budget data.
* Data preprocessing to standardize formats, handle missing values, and optimize data types.
* Development of a Streamlit web application.
* Interactive filters for country/region, technology group, and year range.
* Key visualizations including overall budget trends over time, budget distribution by technology, and country-wise comparisons.
* Display of key statistics and optional raw data viewing.
* Deployment of the application to Streamlit Cloud.

## 3. Key Stakeholders

* **Analysts/Researchers:** Primary users seeking to understand energy RD&D budget allocation and trends.
* **Policymakers:** Users interested in informing energy policy and investment decisions.
* **Energy Sector Professionals:** Users needing insights into funding landscapes for various energy technologies.
* **Project Team:** Developers and data engineers responsible for building and maintaining the application.

## 4. Success Metrics

* **User Engagement:** Number of unique users accessing the application monthly.
* **Data Accuracy:** All visualizations and displayed data accurately reflect the cleaned source data.
* **Filter Functionality:** All filters (Country, Technology Group, Year Range) work as expected, dynamically updating visualizations.
* **Visualization Clarity:** Users can easily interpret the information presented in charts.
* **Deployment Stability:** The application is reliably accessible on Streamlit Cloud with minimal downtime.
* **Feedback Integration (Future):** Positive feedback from users on usability and insights gained.

## 5. Risk Overview

1. **Data Quality & Completeness:**
   * **Risk:** The raw data may contain unexpected inconsistencies, significant missing values, or ambiguities not fully addressed by the current cleaning plan, leading to inaccurate analysis.
   * **Mitigation:** Thorough manual review of a data sample post-cleaning. Implement robust data validation checks within the `clean_data.py` script. Clearly document any known data limitations in the application.
2. **Deployment & Performance on Streamlit Cloud:**
   * **Risk:** The application might experience performance issues (slow loading, unresponsive filters) or deployment failures on Streamlit Cloud, especially with larger datasets or complex visualizations.
   * **Mitigation:** Optimize data loading and processing using `@st.cache_data`. Ensure efficient Pandas operations. Monitor Streamlit Cloud logs for errors. Keep the `requirements.txt` minimal to reduce deployment footprint.
3. **User Experience & Adoption:**
   * **Risk:** The interface might not be intuitive, or the visualizations may not meet user needs, leading to low adoption.
   * **Mitigation:** Follow Streamlit best practices for UI/UX. Gather feedback from initial users for iterative improvements. Ensure clear labeling and explanatory text for all components.

## 6. Technical Specification

Goal:

- Deliver a minimal, maintainable Streamlit app powered by a cleaned CSV for interactive exploration of RD&D budgets.

Inputs & outputs:

- Input: `data/Energy-Technology-RD&D-Budgets-Filtered.csv` (filtered CSV included in the repo used by the app).
- Output: visualizations, downloadable filtered CSVs, and exploratory charts in `streamlit_app.py`.

Core components (implemented):

- Data loader: lightweight CSV loader with caching (`@st.cache_data`) that normalizes columns and parses numeric budget values.
- App: `streamlit_app.py` — interactive Streamlit application with sidebar filters and visualizations (implemented).
- Visualizations: time series of total budgets, bar chart of budgets by technology (aggregated across selected year range), pie chart of top countries (top 20), summary metrics, data table preview, and CSV download.

Notes on implemented filter behavior:

- Year range: slider to select start/end year; charts aggregate over this range where applicable.
- Countries: multi-select (default shows a suggested top subset); used to filter charts and table.
- Technologies: multi-select to filter technology-specific results.

Non-functional requirements:

- Reasonable performance for dataset size (<100k rows).
- Clear code style (PEP 8), documented `requirements.txt`.
- Reproducible environment via `requirements.txt`.

Acceptance tests (practical):

- `streamlit run streamlit_app.py` starts the app and the data loader loads the included CSV quickly (cached after first load).
- Filters (Country, Technology, Year range) update visualizations and tables without errors.
- The exported filtered CSV contains the expected columns (`Year`, `Country`, `Technology`, `Value`, etc.) and matches the applied filters.

Future work / next steps:

- Add Parquet export and faster loader for large datasets.
- Add unit tests for the data cleaning/normalization functions.
- Add more contextual descriptions on charts and units/currency conversions if cross-country monetary comparisons are required.
