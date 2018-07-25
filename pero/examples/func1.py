def draw_cube(p):
    """
    Draw green cube with side = 1,
    then set line color to blue
    """
    p.set('linecolor', 'g')
    p.vector(0, 1)
    p.vector(1, 0)
    p.vector(0, -1)
    p.vector(-1, 0)
    p.draw()
    p.set('linecolor', 'b')