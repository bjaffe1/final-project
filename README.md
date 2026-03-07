# Home Value and Flood Analysis

This project visualizes relationships between Special Flood Hazard Areas (SFHAs), the prevalence of flood damage, takeup rates of National Flood Insurance Program (NFIP) flood insurance, and property values.

## Setup

```bash
conda env create -f environment.yml
conda activate final-project
```

## Project Structure

```
data/
  raw-data/           # Raw data files
    fire.csv          # Historical fire perimeter data
    canadian_cpi.csv  # Canadian Consumer Price Index data
  derived-data/       # Filtered data and output plots
    fire_filtered.gpkg  # Fire data filtered to post-2015
    cpi_filtered.csv    # CPI data filtered to 2020 onwards
code/
  preprocessing.py    # Filters fire and CPI data
  plot_fires.py       # Plots fire perimeters
```

## Usage

1. Run preprocessing to filter data:
   ```bash
   python code/preprocessing.py
   ```

2. Generate the fire perimeter plot:
   ```bash
   python code/plot_fires.py
   ```
   
3. The streamlit app can be accessed at the following url: https://final-project-gvz6bzmb9ah4nrbuytgysi.streamlit.app
   Please note that the app will need to be woken up if it has not been accessed within the past 24 hours.
