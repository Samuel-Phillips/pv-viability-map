import geojson
import shapely.wkt

def wkt2geojson(wkt):
    """Converts a Well Known Text string to a GeoJson-format object."""
    g1 = shapely.wkt.loads(wkt)
    g2 = geojson.Feature(geometry=g1, properties={})
    return g2.geometry
