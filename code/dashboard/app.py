import os
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt


# file mappings
path_regions = 'FemaRegionsProcessed.csv'
if not os.path.isfile(path_regions):
    path_regions = 'code/dashboard/FemaRegionsProcessed.csv'

path_property = 'home_values_processed.csv'
if not os.path.isfile(path_property):
    path_property = 'code/dashboard/home_values_processed.csv'

path_nfip = 'residential_penetration_rates.csv'
if not os.path.isfile(path_nfip):
    path_nfip = 'code/dashboard/residential_penetration_rates.csv'

path_states = 'states_processed.csv'
if not os.path.isfile(path_states):
    path_states = '/code/dashboard/states_processed.csv'

# page configuration
st.set_page_config(
    page_title='Special Flood Hazard Areas and Property Values',
    layout='wide'
)
st.title('Special Flood Hazard Areas and Property Values')

# sidebar controls
level = st.sidebar.selectbox(
    'Region type',
    ['County','State','FEMA Region']
)
variable_to_compare = st.sidebar.selectbox(
    'Metric',
    ['Average property value, January 2026',
     'Average growth in property values, 2016-2026']
)
exclude_outliers = st.sidebar.checkbox(
    'Exclude outliers',
    value=False
)

# load data
@st.cache_data
def load_data(level):
    if level == 'FEMA Region':
        df = pd.read_csv(path_regions)
    elif level == 'State':
        df = pd.read_csv(path_states)
    else:
        df = pd.read_csv(path_property)
        df_nfip = pd.read_csv(path_nfip)[[
            'state','county','percent_sfha']]
        df = df.merge(df_nfip, how='inner', on=['state','county']).reset_index()
    return df

# Filter data
@st.cache_data
def filter_data(level, var):
    df = load_data(level)
    if level == 'FEMA Region':
        if var == 'Average property value, January 2026':
            df_to_plot = df[['fema_region','percent_sfha','average_property_value_2026',
                             'totalResStructures','states']]
            plot_title = 'Average Property Value vs Residences in SFHAs (%), FEMA Regions'
        else:
            df_to_plot = df[['fema_region','percent_sfha', 'states',
                             'percent_growth_property_values','totalResStructures']]
            plot_title = 'Average % Growth in Property Values from January 2016-January 2026 vs Residences in SFHAs (%), FEMA Regions'
    elif level == 'State':
        if var == 'Average property value, January 2026':
            df_to_plot = df[['state','percent_sfha',
                             'average_value','totalResStructures']]
            plot_title = 'Average Property Value vs Residences in SFHAs (%), States'
        else:
            df_to_plot = df[['state','percent_sfha',
                             'percent_growth','totalResStructures']]
            plot_title = 'Average % Growth in Property Values from January 2016-January 2026 vs Residences in SFHAs (%), States'
    else:
        if var == 'Average property value, January 2026':
            df_to_plot = df[['county', 'state', 'percent_sfha',
                             '2026-01-31','totalResStructures']]
            plot_title = 'Average Property Value vs Residences in SFHAs (%), Counties'
        else:
            df_to_plot = df[['county', 'state', 'percent_sfha', 
                             'percent_growth','totalResStructures']]
            plot_title = 'Average % Growth in Property Values from January 2016-January 2026 vs Residences in SFHAs (%), Counties'
    return df_to_plot, plot_title

# plot data
def plot_data(level, var):
    df_to_plot, plot_title = filter_data(level, var)
    if exclude_outliers:
        df_to_plot = df_to_plot[df_to_plot['percent_sfha'] < 20]
    if level == 'FEMA Region':
        if var == 'Average property value, January 2026':
            y_var = 'average_property_value_2026'
            y_title = 'Average Property Value ($)'
        else:
            y_var = 'percent_growth_property_values'
            y_title = '% Growth in home values'
        tooltip=['fema_region','states','percent_sfha',
                 y_var,'totalResStructures']
    elif level == 'State':
        if var == 'Average property value, January 2026':
            y_var = 'average_value'
            y_title = 'Average Property Value ($)'
        else:
            y_var = 'percent_growth'
            y_title = '% Growth in home values'
        tooltip=['state','percent_sfha',
                 y_var,'totalResStructures']
    else:
        if var == 'Average property value, January 2026':
            y_var = '2026-01-31'
            y_title = 'Average Property Value ($)'
        else:
            y_var = 'percent_growth'
            y_title = '% Growth in home values'
        tooltip=['county','state','percent_sfha',
                 y_var,'totalResStructures']
    plot = alt.Chart(df_to_plot, title=plot_title).mark_point().encode(
        x = alt.X('percent_sfha').title('% of homes in SFHAs'),
        y = alt.Y(y_var).title(y_title),
        color = alt.Color('totalResStructures').title('Total residential properties'),
        tooltip=tooltip
    )
    return plot

st.altair_chart(plot_data(level, variable_to_compare))