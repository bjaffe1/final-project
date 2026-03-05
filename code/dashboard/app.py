import os
import streamlit as st
import pandas as pd
import altair as alt


# file mappings
path_regions = 'FemaRegionsProcessed.csv'
if not os.path.isfile(path_regions):
    path_regions = f'https://github.com/bjaffe1/final-project/tree/main/data/derived-data/{path_regions}'

path_property = 'home_values_processed.csv'
if not os.path.isfile(path_property):
    path_property = f'https://github.com/bjaffe1/final-project/tree/main/data/derived-data/{path_property}'

path_nfip = 'residential_penetration_rates.csv'
if not os.path.isfile(path_nfip):
    path_nfip = f'https://github.com/bjaffe1/final-project/tree/main/data/derived-data/{path_nfip}'

path_property_raw = 'County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
if not os.path.isfile(path_property_raw):
    path_property_raw = f'https://github.com/bjaffe1/final-project/tree/main/data/raw-data/{path_property_raw}'

# page configuration
st.set_page_config(
    page_title='Special Flood Hazard Areas and Property Values',
    layout='wide'
)
st.title('Special Flood Hazard Areas and Property Values')

# sidebar controls
level = st.sidebar.selectbox(
    'Region type',
    ['County','FEMA Region']
)
variable_to_compare = st.sidebar.selectbox(
    'Metric',
    ['Average property value, January 2026',
     'Average growth in property values, 2016-2026']
)

# load data
@st.cache_data
def load_data(level):
    if level == 'FEMA Region':
        df = pd.read_csv(path_regions)
    else:
        df = pd.read_csv(path_property)
        df_nfip = pd.read_csv(path_nfip)[[
            'state','county','percent_sfha']]
        df = df.merge(df_nfip, how='inner', on=['state','county'])
    return df

# Filter data
@st.cache_data
def filter_data(level, var):
    df = load_data(level)
    if level == 'FEMA Region':
        if var == 'Average property value, January 2026':
            df_to_plot = df[['fema_region','percent_sfha','average_property_value_2026']]
            plot_title = 'Average Property Value vs Residences in SFHAs (%), FEMA Regions'
        else:
            df_to_plot = df[['fema_region','percent_sfha','percent_growth_property_values']]
            plot_title = 'Average % Growth in Property Values from January 2016-January 2026 vs Residences in SFHAs (%), FEMA Regions'
    else:
        if var == 'Average property value, January 2026':
            df_to_plot = df[['county', 'percent_sfha','2026-01-31']]
            plot_title = 'Average Property Value vs Residences in SFHAs (%), Counties'
        else:
            df_to_plot = df[['county', 'percent_sfha', 'percent_growth']]
            plot_title = 'Average % Growth in Property Values from January 2016-January 2026 vs Residences in SFHAs (%), Counties'
    return df_to_plot, plot_title

# plot data
def plot_data(level, var):
    df_to_plot, plot_title = filter_data(level, var)
    if level == 'FEMA Region':
        if var == 'Average property value, January 2026':
            y_var = 'average_property_value_2026'
            y_title = 'Average Property Value ($)'
        else:
            y_var = 'percent_growth_property_values'
            y_title = '% Growth in home values'
    else:
        if var == 'Average property value, January 2026':
            y_var = '2026-01-31'
            y_title = 'Average Property Value ($)'
        else:
            y_var = 'percent_growth'
            y_title = '% Growth in home values'
    plot = alt.Chart(df_to_plot, title=plot_title).mark_point().encode(
        x = alt.X('percent_sfha').title('% of homes in SFHAs'),
        y = alt.Y(y_var).title(y_title)
    )
    return plot

st.altair_chart(plot_data(level, variable_to_compare))