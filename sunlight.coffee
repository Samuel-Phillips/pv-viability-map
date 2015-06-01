# Adds a polgon (as returned by /rooftops) to a Leaflet map
put_poly = (map, poly) ->
    unless poly.id in map.rooftop_ids
        map.rooftop_ids.push(poly.id)

        for coordlist in poly.geo.coordinates
            L.polygon(coordlist).addTo(map).bindPopup(
                "<b>KWHs:</b> #{poly.light}")

# Retrieves a list of rooftops from the /rooftops API and passes them to
# the supplied callback.
get_shapes = (shape_region, cb) ->
    req = new XMLHttpRequest()
    req.onload = ->
        shapes = JSON.parse(this.responseText)
        cb shapes
    req.open "get", "/rooftops/#{encodeURIComponent(shape_region)}", true
    req.send()

# creates a WKT polygon around the borders of the map
get_wkt_region = (map) ->
    bounds = map.getBounds()
    left = bounds._southWest.lat
    bottom = bounds._southWest.lng
    right = bounds._northEast.lat
    top = bounds._northEast.lng
    return "POLYGON((
        #{left} #{top},
        #{right} #{top},
        #{right} #{bottom},
        #{left} #{bottom},
        #{left} #{top}
    ))"

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
    map.on 'viewreset', (e) ->
        get_shapes get_wkt_region(map), (shapes) ->
            for shape in shapes
                put_poly(map, shape)
