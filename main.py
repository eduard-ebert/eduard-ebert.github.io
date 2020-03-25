# Heidelberg Institute of International Conflict Research
# Bergheim Street 58
# 69115 Heidelberg
# Germany
# Developer: Eduard Ebert
# Contact: ebert@hiik.de

# The last thing I need to add is the description of the conflicts.

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
from bokeh.embed import file_html, components
from bokeh.resources import CDN

from scripts.global_map import *
from scripts.regional_map import *

# Make a colum layout and plot (global)
layout_global = column(p_global, widgetbox(slider_global))

# First tab
tab_global = Panel(child=layout_global, title = "National and international level")

# Make a colum layout and plot (subnational)
layout_subnational = column(p_subnational, widgetbox(slider_subnational))

# Second tab
tab_subnational = Panel(child=layout_subnational, title = "Subnational level")

# Tab switch
tabs = Tabs(tabs=[tab_global, tab_subnational])

# Show plot
curdoc().add_root(tabs)

show(tabs)
