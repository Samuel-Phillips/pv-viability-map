import tempfile
import traceback
import shutil
import os.path
import os
from zipfile import ZipFile
from contextlib import contextmanager
import shapefile
import interface
import pyproj
from osgeo import osr

## Web Mercator (Not used for interaction)
#leaflet_proj = pyproj.Proj(
#    '+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 '
#    '+b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
# EPSG 4326 (Not the actual CRS, but is used for interaction
leaflet_proj = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')


@contextmanager
def tempdir():
    """Contect manager for a temporary directory. Directory is deleted
    when the context manager exits."""
    the_dir = tempfile.mkdtemp()
    try:
        yield the_dir
    finally:
        shutil.rmtree(the_dir)


def import_shape_file(saveable, db):
    """Imports a zipped shapefile (form the saveable parameter, which must
    have a .save method) into the interface.Rooftops object db. Raises
    import_tool.error with messages relating to the error encountered."""
    with tempdir() as root:
        zip_name = os.path.join(root, "map.zip")
        sf_dir = os.path.join(root, "shapes")

        saveable.save(zip_name)
        try:
            ZipFile(zip_name, mode='r').extractall(path=sf_dir)
        except:
            raise error("Error while opening the uploaded file. Make sure "
                        "it is in zip format.")
        sf_names = set(
            name[:-4] for name in os.listdir(sf_dir) if name.endswith(
                '.shp') or name.endswith('.shx') or name.endswith('.dbf'))
        if len(sf_names) == 0:
            raise error("No shapefile found in zip. The zip must contain "
                        "exactly one shapefile, and it must not be in a "
                        "subdirectory.")
        elif len(sf_names) == 1:
            name = sf_names.pop()
            joined = os.path.join(sf_dir, name)
            for ext in 'shp dbf prj'.split():
                if not os.path.isfile(joined + '.' + ext):
                    return error('.' + ext + ' file missing from zip! Please '
                                 'include the entire shapefile.')
            srs = osr.SpatialReference()
            with open(joined + '.prj', mode='r', encoding='ascii') as f:
                srs.ImportFromWkt(f.read())
            p4str = srs.ExportToProj4()
            sf_projection = pyproj.Proj(p4str)
            try:
                sf = shapefile.Reader(joined)
                perform_import(sf, sf_projection, db)
            except shapefile.ShapefileException:
                raise error("Invalid shapefile")
        else:
            raise error("Found multiple shapefiles with names {}. Only one "
                        "shapefile may be present in the zip.".format(
                            ', '.join(sf_names)))


def perform_import(sf, proj, db):
    """Takes a pyshp instance and imports its point to the database."""
    cols = {n: None for n in
            'kwhs BuidArea Perc System Savings UseRoof Zone'.split()}
    for i, f in enumerate(sf.fields):
        if f[0] in cols:
            cols[f[0]] = i - 1
    try:
        db.add_rects(
            interface.Rect(
                wktshape=points2wkt(row.shape.points, proj),
                building_area=row.record[cols['BuidArea']],
                useable_build_area=row.record[cols['UseRoof']],
                percent_usable=row.record[cols['Perc']],
                kwhs=row.record[cols['kwhs']],
                system_size_kw=row.record[cols['System']],
                savings=int(100 * float(row.record[cols['Savings']]))
            ) for row in sf.shapeRecords() if is_useful(row)
        )
    except:
        traceback.print_exc()
        raise error("Database error, see log")


def points2wkt(points, inproj):
    """Converts a list of points into a WKT polygon."""
    points.append(points[0])  # work around for polygons not being connected

    return "POLYGON(({}))".format(
        ','.join(
            ' '.join(str(dim) for dim in pyproj.transform(
                inproj, leaflet_proj, *point)[:2]
            ) for point in points
        ))


def is_useful(row):
    return True


class error(Exception):
    """Generic error from the import process that contains a human readable
    error string."""
    pass
