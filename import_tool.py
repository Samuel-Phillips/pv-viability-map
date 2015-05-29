import tempfile
import shutil
import os.path
import os
from zipfile import ZipFile
from contextlib import contextmanager
import shapefile

@contextmanager
def tempdir():
    the_dir = tempfile.mkdtemp()
    try:
        yield the_dir
    finally:
        shutil.rmtree(the_dir)

def import_shape_file(saveable, db):
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
            sf = shapefile.Reader(os.path.join(sf_dir, sf_names.pop()))
            perform_import(sf, db)
        else:
            raise error("Found multiple shapefiles with names {}. Only one shapefile may be present in the zip.".format(
                        ', '.join(sf_names)))

def perform_import(sf, db):
    try:
        db.add_rects(
                Rect(
                    wktshape=points2wkt(row.shape.points),
                    sunlight=13.37
                ) for sr in sf.iterShapeRecords()
        )
    except:
        traceback.print_exc()
        raise error("Database error, see log")

def points2wkt(points):
    return "POLYGON(({}))".format(
            ','.join(
                ' '.join(point) for point in points
            ))

class error(Exception): pass
