
import plotly.express as px
import streamlit as st
import pandas as pd
from data_processing import load_data

def main():
    st.set_page_config(
        page_title="Energy RD&D Budgets Explorer", layout="wide")
    st.title("Public Energy Technology RD&D Budgets — Explorer")

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

    # Line chart: budgets by year
    st.subheader("Budgets over time")
    by_year = filtered.groupby('Year', as_index=False)['Value'].sum()
    if not by_year.empty:
        fig_line = px.line(by_year, x='Year', y='Value',
                           markers=True, title='Total budget by year')
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data in the selected filters for time series.")

    # Line chart: Budget overtime by country
    st.subheader("Budgets over time by country")
    countries_by_year = filtered.groupby(['Year','Country'], as_index=False)['Value'].sum()
    if not countries_by_year.empty:
        fig_area = px.area(countries_by_year, x='Year', y='Value', color='Country',
                        title='Budgets over time — stacked by country')
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("No data in the selected filters for country time series.")

    # Layout: charts
    left, right = st.columns([2, 1])

    # Top countries
    st.subheader("Top countries (selected) by total budget")
    top_countries = filtered.groupby('Country', as_index=False)[
        'Value'].sum().sort_values('Value', ascending=False).head(10)
    
    with left:
        # Choropleth map
        if not top_countries.empty:
            st.subheader("Geographical Distribution")
            fig_map = px.choropleth(top_countries, locations='Country', locationmode='country names', color='Value', title='Budgets by country')
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No country data available for the selected filters.")

    with right:
        # Top countries pie chart
        if not top_countries.empty:
            fig_pie = px.pie(top_countries, values='Value', names='Country',
                            title='Top countries by total budget (top 10)', hover_data=['Value'])
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No country data available for the selected filters.")

    # Bar chart: by technology for selected year range
    st.subheader("Breakdown by Technology")
    tech_year = filtered.groupby('Technology', as_index=False)[
        'Value'].sum().sort_values('Value', ascending=False)
    if not tech_year.empty:
        fig_bar = px.bar(
            tech_year,
            x='Value',
            y='Technology',
            orientation='h',
            title=f'Budgets by Technology — {sel_year_range[0]}–{sel_year_range[1]}'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No technology breakdown available for the selected filters.")

    # Data download
    st.subheader("Data")
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
