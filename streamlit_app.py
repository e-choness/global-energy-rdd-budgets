
import plotly.express as px
import streamlit as st
import pandas as pd
from data_processing import load_data

def main():
    st.set_page_config(
        page_title="Energy RD&D Budgets Explorer", layout="wide")
    st.title("Public Energy Technology RD&D Budgets — Explorer")

    st.markdown("---")

    st.markdown("""
    Welcome to the Public Energy Technology RD&D Budgets Explorer. This interactive dashboard allows you to explore and analyze government budgets for energy research, development, and demonstration (RD&D) from various countries over several decades.

    **How to use this explorer:**

    1.  **Select Filters**: Use the sidebar on the left to filter the data by year range, country, and technology. You can select multiple countries and technologies to compare their funding trends.
    2.  **Explore Visualizations**: The main panel displays various charts and maps based on your selections.
        *   **Budgets over time**: See how total funding has evolved.
        *   **Geographical Distribution**: Visualize the budget distribution on a world map.
        *   **Breakdown by Technology**: Understand which technology areas receive the most funding.
    3.  **Download Data**: You can download the filtered data as a CSV file for your own analysis.

    This tool is designed for policymakers, researchers, and analysts to gain insights into global energy R&D investment priorities. The data is sourced from the International Energy Agency (IEA).
    """)

    st.markdown("---")

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    years = sorted(df['Year'].dropna().unique())
    year_min, year_max = int(years[0]), int(years[-1])
    sel_year_range = st.sidebar.slider(
        "Year range", year_min, year_max, (year_min, year_max))

    all_countries = sorted(df['Country'].unique())
    sel_countries = st.sidebar.multiselect(
        "Countries (10 suggested)", all_countries, default=all_countries[:10])

    all_tech = sorted(df['Technology'].unique())
    sel_tech = st.sidebar.multiselect(
        "Technologies", all_tech, default=all_tech[:5])

    # apply filters
    filtered = df[(df['Year'] >= sel_year_range[0]) &
                  (df['Year'] <= sel_year_range[1])]
    if sel_countries:
        filtered = filtered[filtered['Country'].isin(sel_countries)]
    if sel_tech:
        filtered = filtered[filtered['Technology'].isin(sel_tech)]

    # summary metrics
    col1, col2, col3 = st.columns(3)
    total_budget = filtered['Value'].sum()
    avg_per_year = filtered.groupby('Year')['Value'].sum().mean()
    latest_year = filtered['Year'].max()
    latest_value = filtered[filtered['Year'] == latest_year]['Value'].sum(
    ) if pd.notna(latest_year) else 0

    col1.metric("Total budget (selection)", f"{total_budget:,.0f}")
    col2.metric("Avg total per year", f"{avg_per_year:,.0f}")
    col3.metric(
        f"Total in {int(latest_year) if pd.notna(latest_year) else 'N/A'}", f"{latest_value:,.0f}")

    st.markdown("---")

    # Line chart: budgets by year
    st.subheader("Budgets over time")
    
    # Description for line chart budgets by year
    st.markdown("""
    **Analysis of Budget Trends Over Time**

    This line chart illustrates the trend of total public energy RD&D budgets for the selected countries and technologies over the specified year range. 
    Each point on the line represents the aggregated budget for a single year.

    - **Trends**: An upward-sloping line indicates a growing commitment to energy R&D, while a downward slope may suggest budget cuts or shifts in policy focus. 
    - **Volatility**: Sharp peaks or troughs can signal one-time investments, economic cycles, or significant geopolitical events impacting funding.

    Use the filters in the sidebar to explore how budget trends differ across countries and technology domains.
    """)

    by_year = filtered.groupby('Year', as_index=False)['Value'].sum()
    if not by_year.empty:
        fig_line = px.line(by_year, x='Year', y='Value',
                           markers=True, title=f'Total budget — {sel_year_range[0]}–{sel_year_range[1]}')
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data in the selected filters for time series.")

    st.markdown("---")

    # Line chart: Budget overtime by country
    st.subheader("Budgets over time by country")

    # Description for line chart budgets by country
    st.markdown("""
    **Analysis of Budget Trends Over Time by Country**

    This line chart illustrates the trend of individual public energy RD&D budgets for the selected countries and technologies over the specified year range. 
    Each point on the line represents the aggregated budget for a single year.

    Use the filters in the sidebar to explore how budget trends differ across countries and technology domains.
    """)

    countries_by_year = filtered.groupby(['Year','Country'], as_index=False)['Value'].sum()
    if not countries_by_year.empty:
        fig_area = px.area(countries_by_year, x='Year', y='Value', color='Country',
                        title=f'Budgets — {sel_year_range[0]}–{sel_year_range[1]} — stacked by country')
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("No data in the selected filters for country time series.")

    st.markdown("---")

    # Layout: charts
    left, right = st.columns([2, 1])

    # Top countries
    
    top_countries = filtered.groupby('Country', as_index=False)[
        'Value'].sum().sort_values('Value', ascending=False).head(10)
    
    with left:
        # Choropleth map
        if not top_countries.empty:
            st.subheader("Geographical Distribution")
            # description for choropleth map
            st.markdown("""
            **Geographical Distribution of Budgets**

            This choropleth map visualizes the total public energy RD&D budgets for the selected countries and technologies over the specified year range. 
            Each country is shaded according to its total budget, with darker shades indicating higher spending.

            Use the filters in the sidebar to explore how budget distributions vary across countries and technology domains.
            """)

            fig_map = px.choropleth(top_countries, locations='Country', locationmode='country names', color='Value')
            fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No country data available for the selected filters.")

    with right:
        # Top countries pie chart
        st.subheader("Top countries (selected) by total budget over time")

        # description for pie chart
        st.markdown("""
        **Top Countries by Total Budget**

        This pie chart shows the distribution of total public energy RD&D budgets across the top countries for the selected technologies and year range. 
        Each slice represents a country, with its size indicating the proportion of the total budget allocated to that country.

        Use the filters in the sidebar to explore how budget distributions vary across countries and technology domains.
        """)

        if not top_countries.empty:
            fig_pie = px.pie(top_countries, values='Value', names='Country',
                            title=f'Top 10 countries by total budget — {sel_year_range[0]}–{sel_year_range[1]}', hover_data=['Value'])
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No country data available for the selected filters.")

    st.markdown("---")

    # Bar chart: by technology for selected year range
    st.subheader("Breakdown by Technology" )
    
    # Description for bar chart breakdown by technology
    st.markdown("""
    **Breakdown of Budgets by Technology**

    This bar chart displays the total public energy RD&D budgets allocated to different technology areas for the selected countries and year range. 
    Each bar represents a technology, with its length indicating the total funding received.

    - **Funding Priorities**: Quickly identify which technology areas are receiving the most significant investments.
    - **Comparison**: Compare funding levels across various technologies to understand strategic focus areas.

    Use the filters in the sidebar to examine how technology funding priorities change across different countries or over specific periods.
    """)

    tech_year = filtered.groupby('Technology', as_index=False)[
        'Value'].sum().sort_values('Value', ascending=False)
    if not tech_year.empty:
        fig_bar = px.bar(
            tech_year,
            x='Value',
            y='Technology',
            orientation='h',
            title=f'Budgets by Technology — {sel_year_range[0]}–{sel_year_range[1]}',
            color='Technology'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No technology breakdown available for the selected filters.")

    # Data download
    st.subheader("Data")
    # description for data download
    st.markdown("""
    This section allows you to download the filtered dataset in CSV format. 
    The data includes all rows that match your selected criteria from the sidebar filters.
    You can use this data for further analysis or reporting.
    """)

    st.write("Filtered sample (first 200 rows)")
    st.dataframe(filtered.head(200))
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download filtered data as CSV", data=csv,
                    file_name='filtered_rd_d_budgets.csv', mime='text/csv')

    st.markdown("---")
    with st.expander("Raw dataset (first 500 rows)"):
        st.dataframe(df.head(500))


if __name__ == '__main__':
    main()
