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
###   Global map   ###
###                ###

# Define paths to data and maps as variables
shp_global = "/Users/eduardebert/Downloads/hiikmap/maps/global.shp"
data_global = "/Users/eduardebert/Downloads/hiikmap/data/global.xlsx"

# Read shapefile
shp_gdf_global = gpd.read_file(shp_global)[["NAME_0", "GID_0", "HASC_0", "geometry"]]

# Filter data for missing values
shp_gdf_global = shp_gdf_global[~shp_gdf_global["geometry"].isnull()]

# Read spreadsheet
df_global = pd.read_excel(data_global,
                          names = ["GID_0", "Country_0", "TIME_0", "TIME_STRING", "HASC_0", "INTENSITY_0"],
                          skiprows = 1)

# Filter data for year 2019
df_2019_global = df_global[df_global["TIME_0"] == 0]

# Merge dataframes for the year 2019
merged_global = shp_gdf_global.merge(df_2019_global, left_on = "HASC_0",
                                     right_on = "HASC_0", how = "left")

merged_global.to_excel("global.xlsx", index = False)

merged_global_json = json.loads(merged_global.to_json())

json_data_global = json.dumps(merged_global_json)

# Define function json_data
def json_data_global(selectedYear_global):
    yr_global = selectedYear_global
    df_yr_global = df_global[df_global["TIME_0"] == yr_global]
    merged_global = shp_gdf_global.merge(df_yr_global, left_on = "HASC_0", right_on = "HASC_0", how = "left")
    merged_global.to_excel("globalplus.xlsx", index = False)
    merged_global_json = json.loads(merged_global.to_json())
    json_data_global = json.dumps(merged_global_json)
    return json_data_global

# Input GeoJSON source that contains features for plotting
geosource_global = GeoJSONDataSource(geojson = json_data_global(0))

# Define color palettes with HIIK colors and instantiate color mappers
hiik_colors = ["#f6f6f6", "#badaef", "#67bff1",
               "#2099d0","#006aa8", "#000116"]

color_mapper = LinearColorMapper(palette = hiik_colors, low = 0, high = 5, nan_color = "#d9d9d9")

# Create map for global values
p_global = figure(title = "Conflicts on a national level in 2019",
                  plot_height = 600, plot_width = 950,
                  toolbar_location = "below",
                  tools = "pan, wheel_zoom, box_zoom, reset")

p_global.xgrid.grid_line_color = None

p_global.ygrid.grid_line_color = None

p_global.axis.visible = False

# Legend
x = 1
y = 1

p_global.square(x, y, legend_label="No Dispute",
                fill_color="#f6f6f6", line_color=None)

p_global.square(x, y, legend_label = "Dispute",
                fill_color = "#badaef", line_color = None)

p_global.square(x, y, legend_label = "Non-violent crisis",
                fill_color = "#67bff1", line_color = None)

p_global.square(x, y, legend_label = "Violent crisis",
                fill_color = "#2099d0", line_color = None)

p_global.square(x, y, legend_label = "Limited war",
                fill_color = "#006aa8", line_color = None)

p_global.square(x, y, legend_label = "War",
                fill_color = "#000116", line_color = None)

p_global.legend.location = "bottom_left"

# Add patch renderer to figure.
states = p_global.patches("xs", "ys", source = geosource_global,
                   fill_color = {"field" : "INTENSITY_0",
                                 "transform" : color_mapper},
                   line_color = "gray", line_width = 0.25, fill_alpha = 1)

# Create hover tool
p_global.add_tools(HoverTool(renderers = [states], tooltips = [("Country", "@NAME_0"),
                                                               ("Intensity", "@INTENSITY_0"),
                                                               ("Time", "@TIME_STRING")]))

# Define the callback function: update_plot
def update_plot_global(attr, old, new):
    yr_global = slider_global.value
    new_data_global = json_data_global(yr_global)       
    geosource_global.geojson = new_data_global 

# Define the slider object
slider_global = Slider(title = "Time", start = 0,
                       end = 12, step = 1, value = 0)

slider_global.on_change("value", update_plot_global)
