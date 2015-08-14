import geojson
from geojson import Feature, Point, LineString, FeatureCollection, Polygon

# returns a feature's coordinates
def get_coords(feature):
  feature = geojson.loads(feature)
  coords = list(geojson.utils.coords(feature))
  return(coords)

# returns a feature's type (point/polygon/line/etc.)
def get_type(feature):
  feature = geojson.loads(feature)
  feature_type = feature.get('type', default=None)
  return(feature_type)

# adds and interest point's properties to that point's
# geojson object and returns the geojson object.
def add_name_and_color(feature, name, color):
  feature = geojson.loads(feature)
  feature.geometry['name'] = name
  feature.properties['marker-color'] = color

  # defaults for marker size and symbol
  feature.properties['marker-size'] = 'medium'
  feature.properties['marker-symbol'] = ''
  feature = geojson.dumps(feature, sort_keys=True)
  return feature

# This function receives a list containing geojson strings.
# It returns a geojson feature collection.
def make_featureCollection(features):
  featureClt = []
  for item in features:
    feature = geojson.loads(item)
    featureClt = featureClt.append(feature)
  featureClt = FeatureCollection(featureClt)
  return (featureClt)




