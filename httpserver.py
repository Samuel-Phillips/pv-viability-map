import flask
import pginterface
import api
import psycopg2
import json

app = flask.Flask(__name__)
DBUSER = 'samtheman'
DATABASE = pginterface.Rooftops(psycopg2.connect(database='test', user=DBUSER))
app.config.from_object(__name__)

with open('sunlight.js') as f:
    sjs_text = f.read()
with open('clientside.html') as f:
    root_text = f.read().replace('-*-magictext-*-', sjs_text)

@app.route("/rooftops/<wkt>")
def getrts(wkt=None):
    results = app.config['DATABASE'].get_rts(wkt)
    prejson = [
             {
               'geo': api.wkt2geojson(rr.wktshape),
               'light': rr.sunlight,
               'id': rr.id
             } for rr in results
           ]
    return json.dumps(prejson)

@app.route("/")
def index():
    return root_text

if __name__=='__main__':
    app.run(debug=True)
