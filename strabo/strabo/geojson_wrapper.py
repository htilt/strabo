import geojson
from strabo import database

# returns a feature's type (point/polygon/line/etc.)
def get_type(feature):
  feature = geojson.loads(feature)
  feature_type = feature['geometry']['type']
  return(feature_type)

# adds and interest point's properties to that point's
# geojson object and returns the geojson object.
def add_info(feature, name,ip_id, color=None):
  feature = geojson.loads(feature)
  feature.geometry['name'] = name
  feature.geometry['db_id'] = ip_id
 # feature.geometry['db_id'] = ip_id
  if color:
    feature.properties['marker-color'] = color

  # defaults for marker size and symbol
  feature.properties['marker-size'] = 'medium'
  feature.properties['marker-symbol'] = ''
  feature = geojson.dumps(feature, sort_keys=True)
  return feature

# This function receives a list containing geojson strings.
# It returns a geojson feature collection.
def make_featureCollection(geojson_objs):
  feature_list = []
  for geojson_object in geojson_objs:
    geo_object = geojson.loads(geojson_object)
    feature_list.append(geo_object)
  feature_collection = geojson.FeatureCollection(feature_list)
  return feature_collection

def get_feature_collection(geojson_feature_type):
  db_geo_objs = database.get_geo_objects(geojson_feature_type)
  return make_featureCollection(db_geo_objs)


def get_all_feature_collections():
  points = get_feature_collection('Point')
  zones = get_feature_collection('Polygon')
  lines = get_feature_collection('LineString')
  return points,zones,lines
