draw_geo_poly = (canvas, poly, cv_size, cv_tl) ->
    for coordlist in poly.coordinates
        prev = undefined
        for coord in coordlist
            alert coord
            if prev == undefined
                prev = true
                canvas.beginPath()
                canvas.strokeStyle = 'green'
                canvas.moveTo(coord[0] - cv_tl[0], coord[1] - cv_tl[1])
            else
                canvas.lineTo(coord[0] - cv_tl[0], coord[1] - cv_tl[1])
        canvas.stroke()

redraw_canvas = (canvas, cv_size, cv_tl) ->
    req = new XMLHttpRequest()
    req.onload = ->
        shapes = JSON.parse(this.responseText)
        for shape in shapes
            draw_geo_poly(canvas, shape.geo, cv_size, cv_tl)
    req.open "get", "/rooftops/#{encodeURIComponent(
        "POLYGON((#{cv_tl[0]} #{cv_tl[1]},
                            #{cv_tl[0] + cv_size[0]} #{cv_tl[1]},
                            #{cv_tl[0] + cv_size[0]} #{cv_tl[1] + cv_size[1]},
                            #{cv_tl[0]} #{cv_tl[1] + cv_size[1]},
                            #{cv_tl[0]} #{cv_tl[1]}))")}"
    req.send()

window.onload = ->
    canvas = document.getElementById('canvas')
    ctx = canvas.getContext('2d')
    redraw_canvas(ctx, [10, 10], [-5, -5])
