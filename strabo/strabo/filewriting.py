import sys, os
from strabo.database import get_geojson
from strabo.geojson import make_featureCollection

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

def write_to(points, zones, lines):
  file_content = "var interest_points = " + str(points) + "\nvar interest_zones = " + str(zones) + "\nvar interest_lines = " + str(lines)
  geojson_file = open(os.path.join('../strabo/strabo/static/js/', 'interest_points.js'), 'w')
  geojson_file.write(file_content)
  geojson_file.close()