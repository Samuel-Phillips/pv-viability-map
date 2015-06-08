# Adds a polgon (as returned by /rooftops) to a Leaflet map
put_poly = (map, poly) ->
    unless poly.id in map.rooftop_ids
        map.rooftop_ids.push(poly.id)
        for coordlist in poly.geo.coordinates
            L.polygon(coordlist).addTo(map).bindPopup """
            <table>
                <tr>
                    <th>Building Area:</th>
                    <td>#{poly.building_area} m<sup>2</sup></td>
                </tr><tr>
                    <th>Useable Build Area:</th>
                    <td>#{poly.useable_build_area} m<sup>2</sup></td>
                </tr><tr>
                    <th>Percent Useable:</th>
                    <td>#{poly.percent_useable}%</td>
                </tr><tr>
                    <th>Expected Output:</th>
                    <td>#{poly.kwhs} kWh</td>
                </tr><tr>
                    <th>System Size:</th>
                    <td>#{poly.system_size_kw} kW</td>
                </tr><tr>
                    <th>Expected Savings:</th>
                    <td>#{poly.savings_str}</td>
                </tr><tr>
                    <th>Rooftop ID:</th>
                    <td>#{poly.id}</td>
                </tr>
            </table>"""

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

window.debug = (type) ->
    switch type
        when 'clicky'
            map.on 'click', (e) ->
                alert "Lat, Lon: #{e.latlng.lat}, #{e.latlng.lng}"

# set up the map, etc.
window.onload = ->
    mapdiv = document.getElementById('map')
    fixsize = (event) ->
        ms = mapdiv.style
        [ms.width, ms.height] = [window.innerWidth, window.innerHeight]
    fixsize()
    addEventListener 'resize', fixsize

    map = L.map('map').setView [38.562025782836706, -77.31149911880492], 15
    L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg',
        attribution: """Portions Courtesy NASA/JPL-Caltech and U.S. Depart.
            of Agriculture, Farm Service Agency. Tiles Courtesy of
            <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>
            <img src="http://developer.mapquest.com/content/osm/mq_logo.png">"""
        maxZoom: 18
        subdomains: '1234'
    ).addTo map
#   L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg',
#       attribution: "TODO: ATTRIBUTION (MQ & OSM)"
#       maxZoom: 18
#       subdomains: '1234'
#   ).addTo map
    map.rooftop_ids = []
    map.on 'viewreset', (e) ->
        get_shapes get_wkt_region(map), (shapes) ->
            for shape in shapes
                put_poly(map, shape)
    # for debugging
    window.map = map
    window.setview = (lat, lng) ->
        map.setView [lat, lng], 10
    window.getframe = -> get_wkt_region map
