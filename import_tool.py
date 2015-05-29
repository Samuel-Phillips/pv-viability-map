import tempfile
import traceback
import shutil
import os.path
import os
from zipfile import ZipFile
from contextlib import contextmanager
import shapefile
import pginterface

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
    have a .save method) into the pginterface.Rooftops object db. Raises
    import_tool.error with messages relating to the error encountered."""
    with tempdir() as root:
        zip_name = os.path.join(root, "map.zip")
        sf_dir = os.path.join(root, "shapes")

        saveable.save(zip_name)
        try:
            ZipFile(zip_name, mode='r').extractall(path=sf_dir)
        except:
            raise error("Error while opening the uploaded file. Make sure it is in zip format.")
        sf_names = set(name[:-4] for name in os.listdir(sf_dir)
                if name.endswith('.shp') or name.endswith('.shx')
                or name.endswith('.dbf'))
        if len(sf_names) == 0:
            raise error("No shapefile found in zip. The zip must contain exactly one shapefile, and it must not be in a subdirectory.")
        elif len(sf_names) == 1:
            try:
                sf = shapefile.Reader(os.path.join(sf_dir, sf_names.pop()))
                perform_import(sf, db)
            except shapefile.ShapefileException:
                raise error("Invalid shapefile")
        else:
            raise error("Found multiple shapefiles with names {}. Only one shapefile may be present in the zip.".format(
                        ', '.join(sf_names)))

def perform_import(sf, db):
    """Takes a pyshp instance and imports its point to the database."""
    kwhs_col = [f[0] for f in sf.fields].index('kwhs') - 1
    if kwhs_col < 0:
        kwhs_col = 0
    try:
        db.add_rects(
                pginterface.Rect(
                    wktshape=points2wkt(row.shape.points),
                    sunlight=row.record[kwhs_col]
                ) for row in sf.shapeRecords()
        )
    except:
        traceback.print_exc()
        raise error("Database error, see log")

def points2wkt(points):
    """Converts a list of points into a WKT polygon."""
    points.append(points[0]) # work around for polygons not being connected
    return "POLYGON(({}))".format(
            ','.join(
                ' '.join(str(dim) for dim in point) for point in points
            ))

class error(Exception):
    """Generic error from the import process that contains a human readable
    error string."""
    pass
