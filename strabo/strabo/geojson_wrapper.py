import geojson

def to_geo_obj(geo_json):
    return geojson.loads(geo_json)

def make_other_attributes_properties(ip):
    feature = to_geo_obj(ip.geojson_object)
    feature.properties = {"name":ip.title,"db_id":ip.id,"layer":ip.layer,"icon":ip.icon}
    return feature
