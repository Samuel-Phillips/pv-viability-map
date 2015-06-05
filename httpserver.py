import flask
import interface
import api
import psycopg2
import json
import import_tool
import password

app = flask.Flask(__name__)
app.config.from_object('flaskconfig')
app.config["DATABASE"] = interface.Rooftops(
    psycopg2.connect(
        database=app.config["DBNAME"],
        user=app.config["DBUSER"],
        password=app.config["DBPASS"],
        host=app.config["DBHOST"]
    ))


# Read files into memory so they may be served quickly
with open('sunlight.js') as f:
    sjs_text = f.read()
with open('clientside.html') as f:
    root_text = f.read().replace('-*-magictext-*-', sjs_text)
with open('import.html') as f:
    iform_text = f.read()
with open('setpass.html') as f:
    setpass_text = f.read()


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


@app.route("/setpass", methods=["GET", "POST"])
def setpass():
    """Routing rule to set the password"""
    if flask.request.method == "POST":
        form = flask.request.form
        if not password.check(form['password']):
            return ("Incorrect current password. If you can't remember it, "
                    "try running this: <code>python3 password.py</code> in "
                    "the application directory.")
        else:
            if form['npass1'] != form['npass2']:
                return "Passwords don't match"
            else:
                password.set(form['npass1'])
                return "ok"
    else:
        return setpass_text


@app.route("/import", methods=["GET", "POST"])
def import_shapefile():
    """Routing rule for this "Import Shapefile" page."""
    db = app.config["DATABASE"]
    if flask.request.method == 'POST':
        if not password.check(flask.request.form['secret']):
            return "Incorrect passcode"
        myfile = flask.request.files['file']
        if myfile:
            with db.insert_lock:
                if 'cleardata' in flask.request.form:
                    db.clear()
                try:
                    import_tool.import_shape_file(myfile, db)
                    db.commit()
                    return "ok"
                except import_tool.error as e:
                    db.rollback()
                    return e.args[0]
        else:
            return "No file submitted"
    else:
        return iform_text

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"],
            host=app.config["HOST"],
            port=app.config["PORT"]
            )
