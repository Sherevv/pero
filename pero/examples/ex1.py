from pero import Pero, Turtle

p = Pero(0, 1)  # Create pero in point (0,1)
p.punct(1, 1)   # Move pero to point (1,1)
p.punct(0, 1)   # Move pero to point (0,1)
p.draw()        # Draw all lines
p.set('linecolor', 'r', 'lineWidth', 2)  # Set line color to red and width = 2
p.vector(1, 2)  # Shift pero on 1 by x and on 2 by y
p.draw()        # Draw all lines
# need to call draw() method before change parameters
# by set method (example, line color)

t = Turtle(-1, 2.3)    # Create turtle in point (-1, 2.3)
t.set('angle', 2.5)    # Set angle in rad.
t.set('step', 1 - 1j)  # Set step vector (1, -1)
t.print()              # Show info about turtle object

for i in range(20):
    t.rot('l')   # Rotate turtle left on 90 deg.
    t.forward()  # Move turtle forward by it's vector

t.draw()  # Draw all lines

input()  # to prevent close plot window
