import geojson

# returns a feature's coordinates
def get_coords(feature):
  feature = geojson.loads(feature)
  coords = list(geojson.utils.coords(feature))
  return(coords)

# returns a feature's type (point/polygon/line/etc.)
def get_type(feature):
  feature = geojson.loads(feature)
  feature_type = feature['geometry']['type']
  return(feature_type)

# adds and interest point's properties to that point's
# geojson object and returns the geojson object.
def add_name_and_color(feature, name, color=None):
  feature = geojson.loads(feature)
  feature.geometry['name'] = name
  if color: 
    feature.properties['marker-color'] = color

  # defaults for marker size and symbol
  feature.properties['marker-size'] = 'medium'
  feature.properties['marker-symbol'] = ''
  feature = geojson.dumps(feature, sort_keys=True)
  print (feature)
  return feature

# This function receives a list containing geojson strings.
# It returns a geojson feature collection.
def make_featureCollection(features):
  feature_collection = []
  for feature in features:
    geojson_object = feature['geojson_object']
    geojson_object = geojson.loads(geojson_object)
    feature_collection.append(geojson_object)
  feature_collection = geojson.FeatureCollection(feature_collection)
  return feature_collection