import flask
import pginterface
import api
import psycopg2
import json
import import_tool

app = flask.Flask(__name__)
DBUSER = 'samtheman'
DATABASE = pginterface.Rooftops(psycopg2.connect(database='test', user=DBUSER))
app.config.from_object(__name__)

with open('sunlight.js') as f:
    sjs_text = f.read()
with open('clientside.html') as f:
    root_text = f.read().replace('-*-magictext-*-', sjs_text)
with open('import.html') as f:
    iform_text = f.read()

@app.route("/")
def index():
    return root_text

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

@app.route("/import", methods=["GET", "POST"])
def import_shapefile():
    db = app.config["DATABASE"]
    if flask.request.method == 'POST':
        if flask.request.form['secret'] != 'password':
            return "Incorrect passcode"
        myfile = flask.request.files['file']
        if myfile:
            if 'cleardata' in flask.request.form:
                db.clear()
            try:
                import_tool.import_shape_file(myfile, db)
                return "ok"
            except import_tool.error as e:
                return e.message
        else:
            return "No file submitted"
    else:
        return iform_text

if __name__=='__main__':
    app.run(debug=True)

