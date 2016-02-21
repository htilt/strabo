import sys, os
from strabo.database import get_geojson
from strabo.geojson import make_featureCollection

from strabo import app

def get_map_params():
  lat_setting = app.config['LAT_SETTING']
  long_setting = app.config['LONG_SETTING']
  tile_src = app.config["MAP_TILE_SRC"]
  tile_attr1 = app.config["MAP_ATTR1"]
  subdomains = app.config["SUBDOMAINS"]
  extension = app.config["EXTENSION"]
  return lat_setting, long_setting, tile_src, tile_attr1, subdomains, extension

def rewrite_geojson():
# Query db for geojson objects
  points = get_geojson('Point')
  zones = get_geojson('Polygon')
  lines = get_geojson('LineString')
  # Convert geojson objects to feature collections
  if points != None: 
    points = make_featureCollection(points)
  else: 
    points = []
  if zones != None: 
    zones = make_featureCollection(zones)
  else: 
    points = []
  if lines != None: 
    lines = make_featureCollection(lines)
  else: 
    lines = []
  # Write to the geojson file
  write_to(points, zones, lines)

# Write to the geojson file with the new interest points and the preset variables for map.js
def write_to(points, zones, lines):
  lat_setting, long_setting, tile_src, tile_attr1, subdomains, extension = get_map_params()
  file_content = "var lat_setting = " + str(lat_setting) + "\nvar long_setting = " + str(long_setting) + "\nvar tile_src = " + "\"" + str(tile_src) + "\""+ "\nvar tile_attr1 = " + "\"" + str(tile_attr1) + "\"" + "\nvar subdomains = " + "\"" + str(subdomains) + "\"" + "\nvar extension = " + "\"" + str(extension) + "\"" + "\nvar interest_points = " + str(points) + "\nvar interest_zones = " + str(zones) + "\nvar interest_lines = " + str(lines)
  geojson_file = open(os.path.join(app.config['JS_FOLDER'], app.config['INTPT_FILE']), 'w')
  geojson_file.write(file_content)
  geojson_file.close()