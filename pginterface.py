import contextlib
import collections

class Rooftops:
    """A database interface with methods that perform database operations on
    a PostGIS database."""
    def __init__(self, database_connection):
        self.db = database_connection
    
    def cursor(self):
        """Returns a context manager for a DB cursor."""
        return contextlib.closing(self.db.cursor())

    def get_rts(self, wktobj):
        """Finds and returns all rooftops that intersect wktobj. Rooftops are
        returned as RRect objects."""
        with self.cursor() as c:
            c.execute("""
            SELECT ST_AsText(shape), sunlight, id
            FROM rooftops
            WHERE ST_Intersects(shape, %s::geometry)
            """, (wktobj,))
            return (RRect(*r) for r in c.fetchall())

    def add_rects(self, rects):
        """Adds a list of Rect objects to the database."""
        with self.cursor() as c:
            c.executemany("""
            INSERT INTO rooftops (shape, sunlight)
            VALUES (%s, %s)
            """, rects)

    def add_rect(self, rect):
        """Adds a single Rect object to the database."""
        self.add_rects((rect,))

    def clear(self):
        """Deletes all rooftops. Dangerous!"""
        with self.cursor() as c:
            c.execute("DELETE FROM rooftops")

Rect = collections.namedtuple('Rect',   ['wktshape', 'sunlight'])
RRect = collections.namedtuple('RRect', ['wktshape', 'sunlight', 'id'])
