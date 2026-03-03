import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import geopandas as gpd
import json

# file mappings
DASHBOARD_DIR = 'data/derived-data'

FLOOD_FILES = {
    'regional_data' : f'{DASHBOARD_DIR}/FemaRegionsProcessed.csv',
    'multiple_loss_data' : f'{DASHBOARD_DIR}/multiple_loss_properties.csv'
}

# page configuration
st.set_page_config(
    page_title='Residential Property Values and the National Flood Insurance Program',
    layout='wide'
)
st.title('Residential Property Values and the National Flood Insurance Program')

# sidebar controls
info = st.sidebar.selectbox(
    'Map type',
    ['Housing values', 'NFIP takeup']
)
multiple_loss_filter = st.sidebar.multiselect(
    'Multiple-claim properties',
    ['2','3','4','5+'],
    default=['2','3','4','5+']
)

# load data
@st.cache_data
def load_geodata():
    df_fema_regions = pd.read_csv(FLOOD_FILES['regional_data'])
    df_properties = pd.read_csv(FLOOD_FILES['multiple_loss_data'])
    gdf_fema_regions = gpd.GeoDataFrame(
        df_fema_regions, crs="EPSG:4326", geometry='regionGeometry'
    )
    gdf_properties = gpd.GeoDataFrame(
        df_properties, crs='EPSG:4326', geometry=gpd.points_from_xy(
            df_properties.longitude, df_properties.latitude
        )
    )
    return gdf_fema_regions, gdf_properties

def load_data(losses, type):
    gdf_fema_regions, gdf_properties = load_geodata()
    gdf_properties_subset = gpd.GeoDataFrame(columns = gdf_properties.columns)
    for n in losses:
        if n in ['2','3','4']:
            n_int = int(n)
            properties_n = gdf_properties[gdf_properties[
                'totalLosses'] == n_int]
            gdf_properties_subset = pd.concat(
                [gdf_properties_subset, properties_n]
            )
        else:
            properties_greater_5 = gdf_properties[gdf_properties[
                            'totalLosses'] > 4]
            gdf_properties_subset = pd.concat(
                [gdf_properties_subset, properties_greater_5]
            )
    if type == 'Housing values':
        gdf_fema_regions_subset = gdf_fema_regions[[
            'fema_region', 'states', 'percent_sfha', 'percent_growth_property_values',
            'average_property_value_2026'
        ]]
    elif type == 'NFIP takeup':
        # this is the part to change after we fix preprocessing to have the NFIP takeup data in the fema regions oops
        gdf_fema_regions_subset = gdf_fema_regions[[
            'fema_region', 'states', 'percent_sfha', 'percent_growth_property_values',
            'average_property_value_2026'
        ]]
    gdf_fema_regions_subset['fema_region'] = gdf_fema_regions_subset['fema_region'].to_string()
    return gdf_properties_subset, gdf_fema_regions_subset

properties_gdf, regions_gdf = load_data(multiple_loss_filter, info)