import traceback
import json
import geojson
import shapely.wkt

def wkt2geojson(wkt):
    g1 = shapely.wkt.loads(wkt)
    g2 = geojson.Feature(geometry=g1, properties={})
    return g2.geometry

def _getresponse(dbo, inpt, outpt):
    form = json.load(inpt)
    result = dbo.get_rects(*(form[q] for q in 'left right top bottom'.split()))
    json.dump(
            {'geo': wkt2geojson(rect.wktshape),
             'light': rect.sunlight,
             'status': 'success'
            } for rect in rects)

def getresponse(dbo, inpt, outpt):
    try:
        _getresponse(dbo, inpt, outpt)
    except:
        json.dump({'status': 'failed'}, outpt)
        traceback.print_exc()
