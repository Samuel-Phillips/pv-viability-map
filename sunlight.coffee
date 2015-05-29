# Adds a polgon (as returned by /rooftops) to a Leaflet map
put_poly = (map, poly) ->
    unless poly.id in map.rooftop_ids
        map.rooftop_ids.push(poly.id)

        for coordlist in poly.geo.coordinates
            L.polygon(coordlist).addTo(map).bindPopup(
                "<b>Sunlight:</b> #{poly.light}")

# Retrieves a list of rooftops from the /rooftops API and passes them to
# the supplied callback.
get_shapes = (shape_region, cb) ->
    req = new XMLHttpRequest()
    req.onload = ->
        shapes = JSON.parse(this.responseText)
        cb shapes
    req.open "get", "/rooftops/#{encodeURIComponent(viewport.wkt)}"
    req.send()

# converts a url to OSM format coordinate
url2osm = (url) ->
    return for x in 1..3
        url.replace /\/(\d+)\/(\d+)\/(\d+).jpg$/, "$#{x}"

# converts an OSM format tile coordinate to a WKT polygon
osm2wkt = (osm) ->
    [z, x, y] = osm
    [tsx, tsy] = tilesize(z)
    left = x * tsx
    right = left + tsx
    top = y * tsy
    bottom = top + tsy
    return "POLYGON((
        #{left} #{bottom},
        #{right} #{bottom},
        #{right} #{top},
        #{left} #{top},
        #{left} #{bottom}))"

url2wkt = (url) -> osm2wkt url2osm url

# set up the map, etc.
window.onload = ->
    map = L.map('map').setView [39.085463, -77.6442], 10
    L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg',
        attribution: """Portions Courtesy NASA/JPL-Caltech and U.S. Depart.
            of Agriculture, Farm Service Agency. Tiles Courtesy of
            <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>
            <img src="http://developer.mapquest.com/content/osm/mq_logo.png">"""
        maxZoom: 18
        subdomains: '1234'
    ).addTo map
    map.rooftop_ids = []
