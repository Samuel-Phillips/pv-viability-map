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

# Read files into memory so they may be served quickly
with open('sunlight.js') as f:
    sjs_text = f.read()
with open('clientside.html') as f:
    root_text = f.read().replace('-*-magictext-*-', sjs_text)
with open('import.html') as f:
    iform_text = f.read()

@app.route("/")
def index():
    """Routing rule for the root page"""
    return root_text

@app.route("/rooftops/<wkt>")
def getrts(wkt=None):
    """Routing rule for the API. When the url /rooftops/<wkt> is requested,
    <wkt> is interpreted as a Well Known Text object, and all rooftops that
    intersect it are returned in a JSON list."""
    results = app.config['DATABASE'].get_rts(wkt)
    prejson = [
             {
               'geo': api.wkt2geojson(rr.wktshape),
               'building_area': rr.building_area,
               'useable_build_area': rr.useable_build_area,
               'percent_useable': rr.percent_usable,
               'kwhs': rr.kwhs,
               'system_size_kw': rr.system_size_kw,
               'savings_ord': rr.savings,
               'savings_str': '$' + str(rr.savings)[:-2] +
                              '.' + str(rr.savings)[-2:],
               'id': rr.id
             } for rr in results
           ]
    return json.dumps(prejson)

@app.route("/import", methods=["GET", "POST"])
def import_shapefile():
    """Routing rule for this "Import Shapefile" page."""
    db = app.config["DATABASE"]
    if flask.request.method == 'POST':
        if flask.request.form['secret'] != 'password':
            return "Incorrect passcode"
        myfile = flask.request.files['file']
        if myfile:
            with db.insert_lock:
                if 'cleardata' in flask.request.form:
                    db.clear()
                try:
                    import_tool.import_shape_file(
                            myfile, db, flask.request.form['proj'])
                    db.commit()
                    return "ok"
                except import_tool.error as e:
                    db.rollback()
                    return e.args[0]
        else:
            return "No file submitted"
    else:
        return iform_text

if __name__=='__main__':
    app.run(debug=True)

