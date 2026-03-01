import os
import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import wkt
import numpy as np

script_dir = Path(__file__).parent

# Process home value data
raw_home_values = script_dir / '../data/raw-data/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
output_home_values = script_dir / '../data/derived-data/home_values_processed.csv'

df_home_values = pd.read_csv(raw_home_values)

# Create column for percent growth in home values between 1/2016 and 1/2026
df_home_values['percent_growth'] = ((df_home_values['2026-01-31'] - 
    df_home_values['2016-01-31']) / df_home_values['2016-01-31']) * 100

# Keep only necessary columns
df_home_values = df_home_values[[
    'RegionName', 'State',  '2016-01-31', '2026-01-31', 'percent_growth'
]]

# Rename county and state columns for merging
df_home_values = df_home_values.rename(
    columns={'RegionName':'county', 'State':'state'}
)

# Get full state names from abbreviations
hv_states = []
for state in df_home_values['state']:
    if state == 'AL':
        hv_states.append('Alabama')
    elif state == 'AK':
        hv_states.append('Alaska')
    elif state == 'AZ':
        hv_states.append('Arizona')
    elif state == 'AR':
        hv_states.append('Arkansas')
    elif state == 'CA':
        hv_states.append('California')
    elif state == 'CO':
        hv_states.append('Colorado')
    elif state == 'CT':
        hv_states.append('Connecticut')
    elif state == 'DE':
        hv_states.append('Delaware')
    elif state == 'DC':
        hv_states.append('District Of Columbia')
    elif state == 'FL':
        hv_states.append('Florida')
    elif state == 'GA':
        hv_states.append('Georgia')
    elif state == 'HI':
        hv_states.append('Hawaii')
    elif state == 'ID':
        hv_states.append('Idaho')
    elif state == 'IL':
        hv_states.append('Illinois')
    elif state == 'IN':
        hv_states.append('Indiana')
    elif state == 'IA':
        hv_states.append('Iowa')
    elif state == 'KS':
        hv_states.append('Kansas')
    elif state == 'KY':
        hv_states.append('Kentucky')
    elif state == 'LA':
        hv_states.append('Louisiana')
    elif state == 'ME':
        hv_states.append('Maine')
    elif state == 'MD':
        hv_states.append('Maryland')
    elif state == 'MA':
        hv_states.append('Massachusetts')
    elif state == 'MI':
        hv_states.append('Michigan')
    elif state == 'MN':
        hv_states.append('Minnesota')
    elif state == 'MS':
        hv_states.append('Mississippi')
    elif state == 'MO':
        hv_states.append('Missouri')
    elif state == 'MT':
        hv_states.append('Montana')
    elif state == 'NE':
        hv_states.append('Nebraska')
    elif state == 'NV':
        hv_states.append('Nevada')
    elif state == 'NH':
        hv_states.append('New Hampshire')
    elif state == 'NJ':
        hv_states.append('New Jersey')
    elif state == 'NM':
        hv_states.append('New Mexico')
    elif state == 'NY':
        hv_states.append('New York')
    elif state == 'NC':
        hv_states.append('North Carolina')
    elif state == 'ND':
        hv_states.append('North Dakota')
    elif state == 'OH':
        hv_states.append('Ohio')
    elif state == 'OK':
        hv_states.append('Oklahoma')
    elif state == 'OR':
        hv_states.append('Oregon')
    elif state == 'PA':
        hv_states.append('Pennsylvania')
    elif state == 'RI':
        hv_states.append('Rhode Island')
    elif state == 'SC':
        hv_states.append('South Carolina')
    elif state == 'SD':
        hv_states.append('South Dakota')
    elif state == 'TN':
        hv_states.append('Tennessee')
    elif state == 'TX':
        hv_states.append('Texas')
    elif state == 'UT':
        hv_states.append('Utah')
    elif state == 'VT':
        hv_states.append('Vermont')
    elif state == 'VA':
        hv_states.append('Virginia')
    elif state == 'WA':
        hv_states.append('Washington')
    elif state == 'WV':
        hv_states.append('West Virginia')
    elif state == 'WI':
        hv_states.append('Wisconsin')
    elif state == 'WY':
        hv_states.append('Wyoming')
    else:
        hv_states.append('No state')
df_home_values['state'] = hv_states

# Add a column for FEMA region
fema_region = []
for state in df_home_values['state']:
    if ((state == 'Maine') | (state == 'New Hampshire') 
        | (state == 'Vermont') | (state == 'Massachusetts') 
        | (state == 'Connecticut') | (state == 'Rhode Island')):
        fema_region.append(1)
    elif ((state == 'Maryland') | (state == 'Pennsylvania') 
          | (state == 'West Virginia') 
          | (state == 'District of Columbia') 
          | (state == 'Delaware') | (state == 'Virginia')):
        fema_region.append(2)
    elif ((state == 'New York') | (state == 'New Jersey')):
        fema_region.append(3)
    elif ((state == 'North Carolina') | (state == 'South Carolina') 
          | (state == 'Georgia') | (state == 'Florida') 
          | (state == 'Alabama') | (state == 'Mississippi')
          | (state == 'Tennessee') | (state == 'Kentucky')):
        fema_region.append(4)
    elif ((state == 'Illinois') | (state == 'Indiana') 
          | (state == 'Ohio') | (state == 'Michigan') 
          | (state == 'Wisconsin') | (state == 'Minnesota')):
        fema_region.append(5)
    elif ((state == 'New Mexico') | (state == 'Texas') 
          | (state == 'Oklahoma') | (state == 'Louisiana') 
          | (state == 'Arkansas')):
        fema_region.append(6)
    elif ((state == 'Nebraska') | (state == 'Kansas') 
          | (state == 'Missouri') | (state == 'Iowa')):
        fema_region.append(7)
    elif ((state == 'Montana') | (state == 'North Dakota') 
          | (state == 'South Dakota') | (state == 'Wyoming') 
          | (state == 'Utah') | (state == 'Colorado')):
        fema_region.append(8)
    elif ((state == 'Nevada') | (state == 'Arizona') 
          | (state == 'California') | (state == 'Hawaii')):
        fema_region.append(9)
    elif ((state == 'Alaska') | (state == 'Washington') 
          | (state == 'Oregon') | (state == 'Idaho')):
        fema_region.append(10)
    else:
        fema_region.append('No region')
df_home_values['fema_region'] = fema_region

df_home_values = df_home_values.dropna()

# Process penetration rates data
raw_penetration_rates = script_dir / '../data/raw-data/NfipResidentialPenetrationRates.csv'
output_penetration_rates = script_dir / '../data/derived-data/residential_penetration_rates.csv'

df_penetration = pd.read_csv(raw_penetration_rates)

# Create a column for percentage of structures in special flood hazard areas
df_penetration['percent_sfha'] = df_penetration['totalResStructuresSfha'] / (
    df_penetration['totalResStructures']) * 100

# Make county names match property value data
penetration_counties = []
for county in df_penetration['county']:
    county_full = county + ' County'
    penetration_counties.append(county_full)
df_penetration['county'] = penetration_counties

# Drop unnecessary columns
df_penetration = df_penetration.drop(columns=['asOfDate', 'id'])

# Create a column for FEMA region
fema_region_penetration_rate = []
for state in df_penetration['state']:
    if ((state == 'Maine') | (state == 'New Hampshire') 
        | (state == 'Vermont') | (state == 'Massachusetts') 
        | (state == 'Connecticut') | (state == 'Rhode Island')):
        fema_region_penetration_rate.append(1)
    elif ((state == 'Maryland') | (state == 'Pennsylvania') 
          | (state == 'West Virginia') 
          | (state == 'District of Columbia') 
          | (state == 'Delaware') | (state == 'Virginia')):
        fema_region_penetration_rate.append(2)
    elif ((state == 'New York') | (state == 'New Jersey')):
        fema_region_penetration_rate.append(3)
    elif ((state == 'North Carolina') | (state == 'South Carolina') 
          | (state == 'Georgia') | (state == 'Florida') 
          | (state == 'Alabama') | (state == 'Mississippi')
          | (state == 'Tennessee') | (state == 'Kentucky')):
        fema_region_penetration_rate.append(4)
    elif ((state == 'Illinois') | (state == 'Indiana') 
          | (state == 'Ohio') | (state == 'Michigan') 
          | (state == 'Wisconsin') | (state == 'Minnesota')):
        fema_region_penetration_rate.append(5)
    elif ((state == 'New Mexico') | (state == 'Texas') 
          | (state == 'Oklahoma') | (state == 'Louisiana') 
          | (state == 'Arkansas')):
        fema_region_penetration_rate.append(6)
    elif ((state == 'Nebraska') | (state == 'Kansas') 
          | (state == 'Missouri') | (state == 'Iowa')):
        fema_region_penetration_rate.append(7)
    elif ((state == 'Montana') | (state == 'North Dakota') 
          | (state == 'South Dakota') | (state == 'Wyoming') 
          | (state == 'Utah') | (state == 'Colorado')):
        fema_region_penetration_rate.append(8)
    elif ((state == 'Nevada') | (state == 'Arizona') 
          | (state == 'California') | (state == 'Hawaii')):
        fema_region_penetration_rate.append(9)
    elif ((state == 'Alaska') | (state == 'Washington') 
          | (state == 'Oregon') | (state == 'Idaho')):
        fema_region_penetration_rate.append(10)
df_penetration['fema_region'] = fema_region_penetration_rate

# Process multiple loss property data
raw_multiple_loss = script_dir / '../data/raw-data/NfipMultipleLossProperties.csv'
output_multiple_loss = script_dir / '../data/derived-data/multiple_loss_properties.csv'

df_multiple_loss = pd.read_csv(raw_multiple_loss, low_memory=False)

# Filter to observations with most recent claim after the year 2000
df_multiple_loss['mostRecentDateofLoss'] = pd.to_datetime(
    df_multiple_loss['mostRecentDateofLoss'])
df_multiple_loss = df_multiple_loss[
    df_multiple_loss['mostRecentDateofLoss'].dt.year > 1999]

# Drop county column (we will match to penetration rate data using fips code)
# Drop other unnecessary columns
df_multiple_loss = df_multiple_loss.drop(columns=['county', 'reportedCity',
                               'communityIdNumber', 'communityName',
                               'censusBlockGroup', 'asOfDate', 'id'])

# Convert state name to title case for matching
states_ml = []
for state in df_multiple_loss['state']:
    state_name = str(state).title()
    if state_name == 'District Of Columbia':
        state_name = 'District of Columbia'
    states_ml.append(state_name)
df_multiple_loss['state'] = states_ml

# Add FEMA region columns
fema_region_multiple_claims = []
for state in df_multiple_loss['stateAbbreviation']:
    if ((state == 'ME') | (state == 'NH') | (state == 'VT') 
        | (state == 'MA') | (state == 'CT') | (state == 'RI')):
        fema_region_multiple_claims.append(1)
    elif ((state == 'MD') | (state == 'PA') | (state == 'WV')
          | (state == 'DC') | (state == 'DE') | (state == 'VA')):
        fema_region_multiple_claims.append(2)
    elif ((state == 'NY') | (state == 'NJ')):
        fema_region_multiple_claims.append(3)
    elif ((state == 'NC') | (state == 'SC') | (state == 'GA')
          | (state == 'FL') | (state == 'AL') | (state == 'MS')
          | (state == 'TN') | (state == 'KY')):
        fema_region_multiple_claims.append(4)
    elif ((state == 'IL') | (state == 'IN') | (state == 'OH')
          | (state == 'MI') | (state == 'WI') | (state == 'MN')):
        fema_region_multiple_claims.append(5)
    elif ((state == 'NM') | (state == 'TX') | (state == 'OK')
          | (state == 'LA') | (state == 'AR')):
        fema_region_multiple_claims.append(6)
    elif ((state == 'NE') | (state == 'KS') | (state == 'MO')
          | (state == 'IA')):
        fema_region_multiple_claims.append(7)
    elif ((state == 'MT') | (state == 'ND') | (state == 'SD')
          | (state == 'WY') | (state == 'UT') | (state == 'CO')):
        fema_region_multiple_claims.append(8)
    elif ((state == 'NV') | (state == 'AZ') | (state == 'CA')
          | (state == 'HI')):
        fema_region_multiple_claims.append(9)
    elif ((state == 'AK') | (state == 'WA') | (state == 'OR')
          | (state == 'ID')):
        fema_region_multiple_claims.append(10)
    else:
        fema_region_multiple_claims.append('No region')
df_multiple_loss['fema_region'] = fema_region_multiple_claims

# Add data to FEMA regions geography for streamlit
raw_fema_regions = script_dir / '../data/raw-data/FemaRegions.csv'
output_fema_regions = script_dir / '../data/derived-data/FemaRegionsProcessed.csv'

df_fema_regions = pd.read_csv(raw_fema_regions)

# Rename region column for merging
df_fema_regions = df_fema_regions.rename(
    columns={'region':'fema_region'}
)

# Drop unnecessary columns
df_fema_regions = df_fema_regions.drop(
    columns=['lastRefresh','hash','id']
)

# Reorder and drop main FEMA headquarters
df_fema_regions = df_fema_regions.dropna()
df_fema_regions = df_fema_regions.sort_values(
    by='fema_region', ascending=True
)

# Add a column for total residential structures
res_structures_by_region = df_penetration[[
    'fema_region','totalResStructures']].groupby(
    'fema_region').sum().reset_index()
df_fema_regions = df_fema_regions.merge(
    res_structures_by_region, how='inner', on='fema_region'
)

# Add a column for total SFHA res structures
res_structures_by_region_sfha = df_penetration[[
    'fema_region','totalResStructuresSfha']].groupby(
    'fema_region').sum().reset_index()
df_fema_regions = df_fema_regions.merge(
    res_structures_by_region_sfha, how='inner', on='fema_region'
)

# Add a column for % of structures in SFHAs
df_fema_regions['percent_sfha'] = (df_fema_regions[
    'totalResStructuresSfha'] / 
    df_fema_regions['totalResStructures']) * 100

# Add a column for average property value trends
res_structures_by_county = df_penetration[[
    'state', 'county', 'totalResStructures']]
df_home_values = df_home_values.merge(
    res_structures_by_county, how='inner', on=['state','county']
)
average_property_trends = []
for i in range(1, 11):
    subset = df_home_values[df_home_values['fema_region'] == i]
    average_trend = np.average(
        subset['percent_growth'],
        weights=subset['totalResStructures']
    )
    average_property_trends.append(average_trend)
df_fema_regions[
    'percent_growth_property_values'] = average_property_trends

# Add a column for average home value
average_home_value = []
for i in range(1, 11):
    subset = df_home_values[df_home_values['fema_region'] == i]
    average_value = np.average(
        subset['2026-01-31'],
        weights=subset['totalResStructures']
    )
    average_home_value.append(average_value)
df_fema_regions['average_property_value_2026'] = average_home_value

# Add a columns for total number of properties with multiple claims
# and percent of properties with multiple claims
multiple_loss_by_region = df_multiple_loss[[
    'fema_region', 'totalLosses']].groupby(
    'fema_region').sum().reset_index()
df_fema_regions = df_fema_regions.merge(
    multiple_loss_by_region, how='inner', on='fema_region'
)
multiple_loss_properties_by_region = df_multiple_loss[[
    'fema_region', 'totalLosses']].groupby(
    'fema_region').count().reset_index()
multiple_loss_properties_by_region = multiple_loss_properties_by_region.rename(
    columns={'totalLosses':'multiple_loss_properties'})
df_fema_regions = df_fema_regions.merge(
    multiple_loss_properties_by_region, how='inner', 
    on='fema_region'
)
df_fema_regions['percent_multiple_loss'] = (
    df_fema_regions['multiple_loss_properties'] / 
    df_fema_regions['totalResStructures']) * 100

df_home_values.to_csv(output_home_values)
df_penetration.to_csv(output_penetration_rates, index=False)
df_multiple_loss.to_csv(output_multiple_loss, index=False)
df_fema_regions.to_csv(output_fema_regions)