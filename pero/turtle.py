import numpy as np
from .pero import Pero
from .exceptions import *


class Turtle:
    """
    Class Turtle

    Methods:
        forward, rot, draw, transform, set, print

    --------------------------------------------------------------

    The Turtle object has an internal buffer.
    If the buffer size is 1, the pen moves
    automatically lead to a graph. Herewith
    operations with buffer using draw and Transform methods are not
    available (trying to execute them results in an error ).

    If the buffer size is greater than 1, move the pen (using
    methods forward, punct, vector) new point graphics temporarily accumulate
    in it, but not in the coordinate axes.
    To build a graph, in this case, you must use the draw method
    (only the last point is then stored in the buffer).

    Also, if the buffer size is greater than 1, then when the buffer is full, its size
    automatically increases ( by the value of the original
    buffer size )

    You can change the buffer size using the set method.
    """

    def __init__(self, x=None, y=None):
        """
        Turtle class constructor

        SYNTAX:
            obj = Turtle( x, y )

        GIVEN:
            - x, y = coordinates of the initial position of the turtle = float scalars

            Initially, the internal buffer contains only one point, later
            its contents may change when executing forward, draw methods

        GOTTA:
            - self = reference (<handle ) to a Turtle class object
            - the internal buffer of the self object contains the coordinates of the initial
            the position of the turtle

        :param x: 
        :param y: 
        """

        self.pero = Pero(x, y)
        self.ort = 1 + 0j  # vector (complex number) that determines the direction of the turtle
        self.angle = np.pi / 2  # the absolute value of the angle of rotation of the turtle

    def rot(self, side=None):
        """
        Turn the turtle at a fixed angle in a given direction

        SYNTAX:
            obj.rot( side )

        GIVEN:
            - obj = reference to a scalar object of Turtle class
            - side = direction of turn = (L / LEFT ) / (R / RIGHT) (no regist)

        GOTTA:
            - turtle is rotated at a fixed angle in a given
            direction (the angle can be set using the method
            set, initially the angle is 90 degrees.)

        :param side:
        """

        side = str.upper(side)

        if side in ('L', 'LEFT'):
            self.ort = self.ort * np.exp(1j * self.angle)
        elif side in ('R', 'RIGTH'):
            self.ort = self.ort * np.exp(-1j * self.angle)
        else:
            raise ParamsValueError

    def forward(self):
        """
        Move the turtle along the set direction by the set step

        SYNTAX:
            obj.forward()

        GIVEN:
            - self = reference to a scalar object of Turtle class

        GOTTA:
            - turtle "moved" forward to the set step
            (  (you can change the step value using the set method);
            new point added to the buffer ( but not shown in
            coordinate axes) if the buffer size is set to 1,
            or added directly to the graph if buffer size
            equals 1
        """

        self.pero.vector(self.ort.real, self.ort.imag)

    def draw(self, draw_type=None):
        """
        Draw a line or paints over a section ( or both family)
        whose point coordinates are contained in the internal buffer

        See draw method of the Pero class
        """

        return self.pero.draw(draw_type)

    def transform(self, f=None, *args):
        """
        Perform the conversion of point coordinates in the buffer according to a given law

        See transform method of the Pero class
        """

        self.pero.transform(f, *args)

    def set(self, *args):
        """
        Set the property values of the Turtle class object

        SYNTAX:
            obj.set('angle', angle) % - sets the absolute value of the turtle's turning angle
            obj.set('step', step) % - set the turtle step value

            Other properties see in set method of a Pero class

            any set of properties from this number can also be set at the same time:

            obj.set ('angle', angle,' step', step,' lineColor', color,..., 'delay', delay )

            (property-value pairs can follow in any order)

        GIVEN:
            - obj = scalar object of Turtle class
            - angle = the absolute value of the turtle's turning angle into rad.
            ( originally set in the corner np.pi/2 )
            step = step size of the turtle ( originally set in step 1 )
            -----------------------------------------------------------
            Other properties see in set method of the Pero class

        GOTTA:
         - the value of the property (s) has been changed to the corresponding values

        :param args:
        """

        if np.mod(len(args), 2) == 1:
            raise ParamsEvenError

        for i in range(0, len(args), 2):

            param = str.upper(args[i])
            if param == 'ANGLE':

                if isinstance(args[i + 1], (float, int)):
                    self.angle = args[i + 1]
                else:
                    raise ParamsAngleError

            elif param == 'STEP':

                if isinstance(args[i + 1], (float, int, complex)):
                    self.ort = args[i + 1]
                else:
                    raise ParamsStepError
            else:
                self.pero.set(args[i:i + 1])

    def print(self):
        """ Display information about turtle object in console """

        print()
        print('The object of the Turtle class:')
        print(' - argument (deg.) and the module of the vector of the direction of the turtle = ',
              str(np.angle(self.ort, deg=True)),
              abs(self.ort))
        print(' - absolute value of rotation angle = ', str(self.angle * 180 / np.pi), ' deg.')

        self.pero.print('prime')

        print(' - class methods: rot, forward, draw, set, print')
