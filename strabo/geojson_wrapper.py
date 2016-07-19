import geojson

def to_geo_obj(geo_json):
    """ Takes data and turns it into a geoJSON object. """
    return geojson.loads(geo_json)

def make_other_attributes_properties(ip):
    """ Returns a geojson feature object with properties of the same names as the
    interest point database fields. """
    feature = to_geo_obj(ip.geojson_object)
    feature.properties = {"name":ip.title,"db_id":ip.id,"layer":ip.layer,"icon":ip.icon}
    return feature
