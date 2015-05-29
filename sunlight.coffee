put_poly = (map, poly) ->
    for coordlist in poly.geo.coordinates
        L.polygon(coordlist).addTo(map).bindPopup(
            "<b>Sunlight:</b> #{poly.light}")

get_shapes = (shape_region, cb) ->
    req = new XMLHttpRequest()
    req.onload = ->
        shapes = JSON.parse(this.responseText)
        cb shapes
    req.open "get", "/rooftops/#{encodeURIComponent(viewport.wkt)}"
    req.send()

window.onload = ->
    map = L.map('map').setView [39.085463, -77.6442], 10
    L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg',
        attribution: """Portions Courtesy NASA/JPL-Caltech and U.S. Depart.
            of Agriculture, Farm Service Agency. Tiles Courtesy of
            <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>
            <img src="http://developer.mapquest.com/content/osm/mq_logo.png">"""
        maxZoom: 18
    ).addTo map
