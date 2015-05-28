draw_geo_poly = (poly, viewport) ->
    for coordlist in poly.coordinates
        prev = undefined
        for coord in coordlist
            if prev == undefined
                prev = true
                viewport.ctx.beginPath()
                viewport.ctx.strokeStyle = 'green'
                viewport.moveTo coord
            else
                viewport.lineTo coord
        viewport.ctx.stroke()

redraw_canvas = (viewport) ->
    req = new XMLHttpRequest()
    req.onload = ->
        shapes = JSON.parse(this.responseText)
        for shape in shapes
            draw_geo_poly(shape.geo, viewport)
    req.open "get", "/rooftops/#{encodeURIComponent(viewport.wkt)}"
    req.send()

window.onload = ->
    map = L.map('map').setView [51.505, -0.09], 13
    L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg',
        attribution: """Portions Courtesy NASA/JPL-Caltech and U.S. Depart.
            of Agriculture, Farm Service Agency. Tiles Courtesy of
            <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>
            <img src="http://developer.mapquest.com/content/osm/mq_logo.png">"""
        maxZoom: 18
    ).addTo map
