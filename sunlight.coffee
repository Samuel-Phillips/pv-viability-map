class Viewport
    constructor: (@canvas, @left, @right, @top, @bottom) ->
        @width = @right - @left
        @height = @top - @bottom
        @ctx = @canvas.getContext '2d'
        @wkt = "POLYGON((
            #{@left} #{@bottom},
            #{@right} #{@bottom},
            #{@right} #{@top},
            #{@left} #{@top},
            #{@left} #{@bottom}))"

    transform: (coord) ->
        x = (coord[0] - @left) * @canvas.width / @width
        y = (@top - coord[1]) * @canvas.height / @height
        return [x, y]

draw_geo_poly = (poly, viewport) ->
    for coordlist in poly.coordinates
        prev = undefined
        for coord in coordlist
            alert coord
            if prev == undefined
                prev = true
                viewport.ctx.beginPath()
                viewport.ctx.strokeStyle = 'green'
                viewport.ctx.moveTo.apply(this, viewport.transform coord)
            else
                viewport.ctx.lineTo.apply(this, viewport.transform coord)
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
    canvas = document.getElementById('canvas')
    viewport = new Viewport(canvas, -5, 5, 5, -5)
    redraw_canvas(viewport)
