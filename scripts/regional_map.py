# Heidelberg Institute of International Conflict Research
# Bergheim Street 58
# 69115 Heidelberg
# Germany
# Developer: Eduard Ebert
# Contact: ebert@hiik.de

###                ###
### Import section ###
###                ###

import json
import bokeh.settings
import geopandas as gpd
import pandas as pd
import numpy as np

from bokeh.io import show
from bokeh.io.doc import curdoc
from bokeh.models import (Tabs, Panel, Slider, CDSView, ColorBar, ColumnDataSource, CustomJS, CustomJSFilter, GeoJSONDataSource, HoverTool, LinearColorMapper, Slider, Legend, LegendItem)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import output_file, show, figure

###                ###
###  Regional map  ###
###                ###

# Define paths to data and maps as variables
shp_subnational = "/Users/eduardebert/Downloads/hiikmap/maps/subnational.shp"
data_subnational = "/Users/eduardebert/Downloads/hiikmap/data/subnational.xlsx"

# Read shapefile
shp_gdf_subnational = gpd.read_file(shp_subnational)[["GID_0", "NAME_0", "GID_1", "NAME_1", "NL_NAME_1", "VARNAME_1", "TYPE_1", "ENGTYPE_1", "CC_1", "HASC_1", "geometry"]]
shp_gdf_subnational = shp_gdf_subnational[~shp_gdf_subnational["geometry"].isnull()]
shp_gdf_subnational = shp_gdf_subnational[~shp_gdf_subnational["HASC_1"].isnull()]

# Read spreadsheet
df_subnational = pd.read_excel(data_subnational, names = ["GID_1", "Country_1",
                                                          "Region", "HASC_1",
                                                          "TIME_1", "TIME_String",
                                                          "INTENSITY_1"], skiprows = 1)

df_subnational = df_subnational[~df_subnational["HASC_1"].isnull()]

# Filter data for year 2019
df_subnational_2019 = df_subnational[df_subnational["TIME_1"] == 0]

# Merge dataframes world_map and df for the year 2018
merged_subnational = shp_gdf_subnational.merge(df_subnational_2019, left_on = "HASC_1",
                                               right_on = "HASC_1", how = "inner")

merged_subnational.to_excel("regional.xlsx", index = False)

# Input GeoJSON source that contains features for plotting
merged_json_subnational = json.loads(merged_subnational.to_json())

json_data_subnational = json.dumps(merged_json_subnational)

# Define function json_data
def json_data_subnational(selectedYear_subnational):
    yr_subnational = selectedYear_subnational
    df_yr_subnational = df_subnational[df_subnational["TIME_1"] == yr_subnational]
    merged_subnational = shp_gdf_subnational.merge(df_yr_subnational, left_on = "HASC_1", right_on = "HASC_1", how = "inner")
    merged_subnational.to_excel("regionalplus.xlsx", index = False)
    merged_json_subnational = json.loads(merged_subnational.to_json())
    json_data_subnational = json.dumps(merged_json_subnational)
    return json_data_subnational

# Input GeoJSON source that contains features for plotting
geosource_subnational = GeoJSONDataSource(geojson = json_data_subnational(0))

# Define color palettes with HIIK colors and instantiate color mappers
hiik_colors = ["#f6f6f6", "#badaef", "#67bff1",
               "#2099d0","#006aa8", "#000116"]

color_mapper = LinearColorMapper(palette = hiik_colors, low = 0, high = 5, nan_color = "#d9d9d9")

# Create map for subnational values
p_subnational = figure(title = "Conflicts on a subnational level in 2019",
                       plot_height = 600, plot_width = 950,
                       toolbar_location = "below",
                       tools = "pan, wheel_zoom, box_zoom, reset")

p_subnational.xgrid.grid_line_color = None

p_subnational.ygrid.grid_line_color = None

p_subnational.axis.visible = False

# Legend
x = 1
y = 1

p_subnational.square(x, y, legend_label = "No Dispute",
                     fill_color = "#f6f6f6", line_color = None)

p_subnational.square(x, y, legend_label = "Dispute",
                     fill_color = "#badaef", line_color = None)

p_subnational.square(x, y, legend_label = "Non-violent crisis",
                     fill_color = "#67bff1", line_color = None)

p_subnational.square(x, y, legend_label = "Violent crisis",
                     fill_color = "#2099d0", line_color = None)

p_subnational.square(x, y, legend_label = "Limited war",
                     fill_color = "#006aa8", line_color = None)

p_subnational.square(x, y, legend_label = "War",
                     fill_color = "#000116", line_color = None)

p_subnational.legend.location = "bottom_left"

# Add patch renderer to figure.
regions = p_subnational.patches("xs","ys", source = geosource_subnational,
                                fill_color = {"field": "INTENSITY_1",
                                              "transform": color_mapper},
                                line_color = "gray", line_width = 0.25, fill_alpha = 1)

# Create hover tool
p_subnational.add_tools(HoverTool(renderers = [regions], tooltips = [("Region", "@Region"),
                                                                     ("Intensity", "@INTENSITY_1"),
                                                                     ("Time", "@TIME_STRING")]))

# Define the callback function: update_plot
def update_plot_subnational(attr, old, new):
    yr_subnational = slider_subnational.value
    new_data_subnational = json_data_subnational(yr_subnational)       
    geosource_subnational.geojson = new_data_subnational

# Define the slider object
slider_subnational = Slider(title = "Time", start = 0,
                            end = 12, step = 1, value = 0)

slider_subnational.on_change("value", update_plot_subnational)
