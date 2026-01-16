import streamlit as st
import pandas as pd
import plotly.express as px

DATA_PATH = "data/Energy-Technology-RD&D-Budgets-Filtered.csv"


@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    # prefer uppercase TIME_PERIOD and OBS_VALUE which hold values
    if 'TIME_PERIOD' in df.columns:
        df['Year'] = pd.to_numeric(
            df['TIME_PERIOD'], errors='coerce').astype(pd.Int64Dtype())
    elif 'Time Period' in df.columns:
        df['Year'] = pd.to_numeric(
            df['Time Period'], errors='coerce').astype(pd.Int64Dtype())
    else:
        df['Year'] = pd.NA

    if 'OBS_VALUE' in df.columns:
        df['Value'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
    elif 'Observation value' in df.columns:
        df['Value'] = pd.to_numeric(df['Observation value'], errors='coerce')
    else:
        df['Value'] = pd.NA

    # friendly names
    if 'Country/Region' in df.columns:
        df['Country'] = df['Country/Region']
    elif 'COUNTRY' in df.columns:
        df['Country'] = df['COUNTRY']

    if 'Technology' in df.columns:
        df['Technology'] = df['Technology']
    elif 'RDD_TECH' in df.columns:
        df['Technology'] = df['RDD_TECH']

    if 'Sector' in df.columns:
        df['Sector'] = df['Sector']

    # drop rows missing values
    df = df.dropna(subset=['Year', 'Value', 'Country'])

    return df


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
        "Countries (top 10 suggested)", all_countries, default=all_countries[:10])

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

    st.markdown("---")

    # Layout: charts
    left, right = st.columns([2, 1])

    with left:
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

    with right:
        # Top countries pie chart
        st.subheader("Top countries by total budget")
        top_countries = filtered.groupby('Country', as_index=False)[
            'Value'].sum().sort_values('Value', ascending=False).head(20)
        if not top_countries.empty:
            fig_pie = px.pie(top_countries, values='Value', names='Country',
                            title='Top countries by total budget (top 20)', hover_data=['Value'])
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No country data available for the selected filters.")

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
