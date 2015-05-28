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

    moveTo: (coord) ->
        [x, y] = @transform coord
        @ctx.moveTo x, y

    lineTo: (coord) ->
        [x, y] = @transform coord
        @ctx.lineTo x, y

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
    canvas = document.getElementById('canvas')
    viewport = new Viewport(canvas, -4, 4, 2, -2)
    redraw_canvas(viewport)
