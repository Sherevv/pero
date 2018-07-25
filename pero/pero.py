import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, lines
import matplotlib.colors as mclr
from .exceptions import *


class Pero:
    """
    Class Pero

    Methods:
        punct, vector, draw, flip, transform, set, print

    Properties of the graphic object (created by the draw method ) by default:
        linecolor = 'b'
        patchcolor = 'b' - fill color
        linewidth = 0.5
        linestyle =' -'
        marker = 'none'
        markersize = 6

        bufsize = 200 - is the column size of the buffer (1-th size of the arrays xdata, ydata)
        numpoint - number of line points buffered
        xdata - buffer
        ydata - buffer

        draw_enable_at_bufsize_equal_1 = 'off' - relevant only when bufsize = 1,
        used to enable invocation of the method draw of the methods punct, vector when bufsize = 1

        delay = 0 - added artificial time delay in the execution of the method draw, h

    -------------------------------------------------------------------------

    The Pero object has an internal buffer.
    If buffer size (number of points to fit) is 1,
    plant of the pen (using the methods punct, vector) automatically lead
    to build the graph. In this case, operations with the buffer using methods
    draw and transform are not available ( an attempt to execute them results in an error ).

    If the buffer size is greater than 1, move the pen (using
    methods punct, vector) new point graphics temporarily accumulate
    in it, but not in the coordinate axes.
    In this case, you need to use the draw method to build the chart
    (only the last point is then stored in the buffer).

    Also, if the buffer size is greater than 1, then when the buffer is full, its size
    automatically increases ( by the value of the original buffer size).

    You can change the buffer size using the set method.

    """

    def __init__(self, *args):
        """
        Pero class constructor

        SYNTAX:
            obj = Pero( x, y )
            obj = Pero( p1, ..., pn )

        GIVEN:
            x, y - initial position coordinates of the pen = float scalars

        OR
            p1,..., pn (n>0) - references to Pero class objects

        GOTTA:
            - obj = reference to a new Pero class object
            - the internal buffer of the obj object contains the coordinates of the initial
            the position of your pen

        OR
            the internal buffer of an obj object contains a concatenation
            the coordinates of the pen positions contained in p1...,p2
        """

        # Defaults:
        self.linecolor = 'b'
        self.patchcolor = 'b'
        self.linewidth = 0.5
        self.linestyle = '-'
        self.marker = ''
        self.markersize = 6
        self.delay = 0

        self.draw_enable_at_bufsize_equal_1 = 'off'

        self.bufsize = 200
        self.numpoint = None

        self.xdata = None
        self.ydata = None

        f = isinstance(args[0], (float, int))
        if f and len(args) != 2:
            raise CountParamsError

        for i in range(len(args)):
            if f and not isinstance(args[i], (float, int)):
                raise ParamsTypeError

            elif not f and not isinstance(args[i], Pero):
                raise ParamsPeroTypeError

        if f:  # && len(args) == 2 && both are of type float
            x = args[0]
            y = args[1]
            if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
                raise ParamsScalarTypeError

            self.xdata = np.zeros(self.bufsize, dtype=float)
            self.ydata = np.zeros(self.bufsize, dtype=float)

            self.xdata[0] = x
            self.ydata[0] = y
            self.numpoint = 1
        else:  # f == 0 && all args elements are of Pero type

            n = 0
            m = 0
            for i in range(len(args)):
                n = n + len(args[i].xdata)
                m = m + args[i].numpoint

            self.numpoint = m

            if m <= 200:
                self.bufsize = 200
            else:
                self.bufsize = 2 * m

            self.xdata = np.zeros(self.bufsize, dtype=float)
            self.ydata = np.zeros(self.bufsize, dtype=float)
            m = 0
            for i in range(len(args)):
                k = args[i].numpoint
                self.xdata[m:m + k - 1] = args[i].xdata[0:k - 1]
                self.ydata[m:m + k - 1] = args[i].ydata[0:k - 1]
                m = m + k

        self.hFig = plt.gcf()
        self.hAxes = plt.gca()
        self.hAxes.set_aspect('equal')
        plt.show(block=False)

    def flip(self):
        """
        Flip the contents of the object's internal buffer backwards

        SYNTAX:
            obj2 = obj.flip()

        GIVEN:
            - obj = scalar object of Pero class

        :return: new Pero object with flipped buffer
        """

        obj2 = Pero(self)
        obj2.xdata = np.flipud(obj2.xdata)
        obj2.ydata = np.flipud(obj2.ydata)
        return obj2

    def set(self, *args):
        """
        Set the property values of the Pero class object

        SYNTAX:
            obj.set('lineColor', color) % - set line color
            obj.set('patchColor', color) % - set patch color
            obj.set('lineStyle', style) % - set line style
            obj.set('lineWidth', width) % - set line width
            obj.set('marker', marker) % - set marker type
            obj.set('markerSize , size) % - set marker size
            obj.set('bufsize', bufSize) % - set buffer size
            obj.set('delay', delay) % - set the value of the artificial delay

            any set of properties from this number can also be set at the same time:

            obj.set('lineColor', color,..., 'delay', delay )

            (property-value pairs can follow in any order)

        GIVEN:
            - obj = scalar object of Pero class
            - color = color = ' b ' | ' r ' | ' g ' | ' y ' | ' k ' | ' w ' | ' m ' / 3-vector float
            (initially the color is set to 'b')
            - style = line style= 'solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':', 'None', ' ', ''
            (initially the line style is set to' -')
            - width = line thickness = scalar float
            (initially the line thickness is set to 0.5)
            - marker = marker type = '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8',
                        '*', '+', '|', '_', 's', 'h', 'H', 'D', 'd', 'p', 'P', 'x', 'X', 'None', ' ', ''
            (originally set to 'none' )
            - size = marker size = scalar float ( originally set to 6 )
            - bufSize = buffer size
            - delay = the duration of the artificial delay a sec. = scalar float
            (initially set to 0 )

        GOTTA:
            - the value of the property (s) has been changed to the corresponding values

        :param args:  -  property-value pairs
        """

        if np.mod(len(args), 2) == 1:
            raise ParamsEvenError

        for i in range(0, 2, len(args)):
            if not isinstance(args[i], str):
                raise ParamsStringError

            param = str.upper(args[i])
            if param == 'LINECOLOR':
                if mclr.is_color_like(args[i + 1]):
                    self.linecolor = args[i + 1]
                else:
                    raise ParamsLineColorError

            elif param == 'PATCHCOLOR':
                if mclr.is_color_like(args[i + 1]):
                    self.patchcolor = args[i + 1]
                else:
                    raise ParamsPatchColorError

            elif param == 'LINESTYLE':
                if args[i + 1] in ('solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':', 'None', ' ', ''):
                    self.linestyle = args[i + 1]
                else:
                    raise ParamsLineStyleError

            elif param == 'LINEWIDTH':

                if isinstance(args[i + 1], (float, int)):
                    self.linewidth = args[i + 1]
                else:
                    raise ParamsLineWidthError

            elif param == 'MARKER':
                if args[i + 1] in (
                        '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8',
                        '*', '+', '|', '_', 's', 'h', 'H', 'D', 'd', 'p', 'P', 'x', 'X', 'None', ' ', ''):

                    self.marker = args[i + 1]
                else:
                    raise ParamsMarkerError

            elif param == 'MARKERSIZE':

                if isinstance(args[i + 1], (float, int)):
                    self.markersize = args[i + 1]
                else:
                    raise ParamsMarkerSizeError

            elif param == 'DELAY':

                if isinstance(args[i + 1], (float, int)):
                    self.delay = args[i + 1]
                else:
                    raise ParamsDelayError

            elif param == 'BUFSIZE':
                if self.numpoint > 1:
                    raise BufferSizeChangeError

                if isinstance(args[i + 1], int) and args[i + 1] > 0:
                    self.bufsize = args[i + 1]

                    xbuf = self.xdata[0:self.numpoint - 1]
                    ybuf = self.ydata[0:self.numpoint - 1]

                    n = int(self.numpoint / self.bufsize) + 1

                    self.xdata = np.zeros(self.bufsize, n)
                    self.ydata = np.zeros(self.bufsize, n)

                    self.xdata[0:self.numpoint - 1] = xbuf
                    self.ydata[0:self.numpoint - 1] = ybuf

                else:
                    raise ParamsBufsizeError

            else:
                raise ParamsNameError

    def draw(self, *args):
        """
        Draw a line or paints over a section ( or both family)
        whose point coordinates are contained in the internal buffer

        SYNTAX:
            obj.draw()
            obj.draw( type )
            h = obj.draw()
            h = obj.draw( type )
            obj.draw( type, dx, dy )
            h = obj.draw( type, dx, dy )

        GIVEN:
            - obj = scalar object of Pero class
            - set internal buffer size greater than 1
            - the internal buffer contains the coordinate sequence of the line points
            - type = 'line' | 'patch' | []
            ( default type = 'line' < = > type = [] )
            - dx, dy-coordinates of the pen displacement vector
            (default dx = dy = 0 )

        GOTTA:
            - a line is built in the current coordinate axes with predefined properties
            ( changing predefined properties can be done with the set method )
            - h = descriptor of the constructed line
            - the internal buffer contains only the last point from the source
            sequences of points SHIFTED by vector dx, dy
            (the buffer contains the coordinates of the current pen position )
            - the construction lines are made with extra artificial temporary
            a delay of a preset value
            (default delay value is set to 0, change
            this setting can be done using the Set method )

        :param args:  -  type, dx, dy
        :return: h  -  descriptor of the constructed line
        """

        if self.bufsize == 1 and self.draw_enable_at_bufsize_equal_1 == 'off':
            raise DrawBufsizeError

        n = self.numpoint

        if self.delay > 0:
            for i in range(n - 1):
                h = lines.Line2D(
                    xdata=self.xdata[i:i + 1],
                    ydata=self.ydata[i:i + 1],
                    color=self.linecolor,
                    linewidth=self.linewidth,
                    linestyle=self.linestyle,
                    marker=self.marker,
                    markersize=self.markersize)

                self.hAxes.add_line(h)
                self.hFig.canvas.draw()
                self.hAxes.relim()
                self.hAxes.autoscale()

                time.sleep(self.delay / (n - 1))

            if self.bufsize == 1:
                self.xdata[0] = self.xdata[n - 1]
                self.ydata[0] = self.ydata[n - 1]
                self.numpoint = 1

                return

        if len(args) == 0 or args[0] == 'line' or not args[0]:
            h = lines.Line2D(
                xdata=self.xdata[0:n],
                ydata=self.ydata[0:n],
                color=self.linecolor,
                linewidth=self.linewidth,
                linestyle=self.linestyle,
                marker=self.marker,
                markersize=self.markersize)
            self.hAxes.add_line(h)

        elif args[0] == 'patch':

            h = patches.Patch(
                xdata=self.xdata[0:n - 1],
                ydata=self.ydata[0:n - 1],
                edgecolor=self.linecolor,
                facecolor=self.patchcolor,
                markerEdgeColor=self.linecolor,
                markerFaceColor=self.linecolor,
                linewidth=self.linewidth,
                linestyle=self.linestyle,
                marker=self.marker,
                markersize=self.markersize)
            self.hAxes.add_patch(h)

        else:
            raise ParamsValueError

        self.hFig.canvas.draw()
        self.hAxes.relim()
        self.hAxes.autoscale()

        dx = 0
        dy = 0
        if len(args) == 2:
            raise ParamsCoordinatesError
        elif len(args) == 3:
            dx = args[1]
            dy = args[2]
            if not isinstance(dx, (float, int)) or not isinstance(dy, (float, int)):
                raise ParamsCoordinatesError

        elif len(args) > 3:
            raise TooManyParamsError

        self.xdata[0] = self.xdata[n - 1] + dx
        self.ydata[0] = self.ydata[n - 1] + dy
        self.numpoint = 1

        return h

    def vector(self, dx=None, dy=None):
        """
        Move the pen to the specified vector from the last point of the line under construction to the new one

        SYNTAX:
            obj.vector(dx, dy)

        GIVEN:
            - obj = scalar object of Pero class
            - the internal buffer of the object obj does not contain the empty
            a sequence of points (at least one point)
            - dx, dy = coordinates of the pen displacement vector to the next
            line point = float scalars

        GOTTA:
            - coordinates of a new chart point are added to the buffer if
            set buffer size greater than 1, or new point
            added directly to the graph if buffer size is 1

        :param dx:  x coordinates of the pen displacement vector to the next
        :param dy:  y coordinates of the pen displacement vector to the next
        """

        if not isinstance(dx, (float, int)) or not isinstance(dy, (float, int)):
            raise ParamsScalarTypeError

        if len(self.xdata) == self.numpoint:
            self._add_colon()

        self.xdata[self.numpoint] = np.array(self.xdata[self.numpoint - 1]) + dx
        self.ydata[self.numpoint] = np.array(self.ydata[self.numpoint - 1]) + dy
        self.numpoint += 1

        if self.bufsize == 1:
            self.draw_enable_at_bufsize_equal_1 = 'on'
            self.draw()
            self.draw_enable_at_bufsize_equal_1 = 'off'

    def punct(self, x=None, y=None):
        """
        Move the pen to a point with specified coordinates

        SYNTAX:
            obj.punct( x, y )

        GIVEN:
            - obj = scalar object of Pero class
            - x, y = point coordinates = float scalars

        GOTTA:
            - coordinates of a point are added to the buffer if
            set buffer size greater than 1, or new point
            added directly to the graph if buffer size is 1

        :param x:  x point coordinate
        :param y:  y point coordinate
        """

        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise ParamsScalarTypeError

        if len(self.xdata) == self.numpoint:
            self._add_colon()

        self.xdata[self.numpoint] = x
        self.ydata[self.numpoint] = y
        self.numpoint += 1

        if self.bufsize == 1:
            self.draw_enable_at_bufsize_equal_1 = 'on'
            self.draw()
            self.draw_enable_at_bufsize_equal_1 = 'off'

    def transform(self, f=None, *args):
        """
        Perform the conversion of point coordinates in the buffer according to a given law

        SYNTAX:
            obj.transform( f )
            obj.transform( f, p1,..., pn )

        GIVEN:
            - obj = scalar object of Pero class
            - set internal buffer size greater than 1
            - f = LINK to function that dehumidifies
            convert the coordinate plane and having the header:
            x2, y2 = F( x1, y1 )
            or
            x2, y2  = F( x1, y1, p1,..., pn )
            respectively, where x1, y1 are Cartesian coordinates of the prototype of some
            (arbitrary) points of the plane, x2, y2 - Cartesian coordinates of its image at
            display F ( the name of the transform function can be anything, but if,
            as in the example, it is F, then the input parameter f = @F is a REFERENCE to the function F )
            - p1,..., pn - a set of additional parameters for the function f
            (the number of additional parameters and their types can be any)

        GOTTA:
            - coordinates of all points contained in the internal buffer
            obj, converted using the f function
        :param f: - link to function that dehumidifies transformation
        :param args:
        """

        if self.bufsize == 1:
            raise TransformBufsizeError

        for i in range(self.numpoint):
            self.xdata[i], self.ydata[i] = f(self.xdata[i], self.ydata[i], *args)

    def print(self, mode=None):
        """
        Display a Pero class object in the command window

        SYNTAX:
            obj.print() - displays the Pero class object in the command window ( the main method of use )
            obj.print('prime') - displays only basic information and only about the SCALAR object

        GIVEN:
            - obj = Pero class object ( not necessarily scalar )
            - [mode] = 'prime' - optional flag parameter;
            in this case, obj - must be a scalar

        :param mode:
        """

        if mode is not None:
            if mode == 'prime':
                self._print_prime()
                return
            else:
                raise ParamsValueError

        print('The object of the Pero class:')
        print(' - class methods: punct, vector, draw, transform, set, print')

    def _print_prime(self):
        """ Display only basic information """

        print(' - coordinates of the last point  = ', [self.xdata[self.numpoint - 1], self.ydata[self.numpoint - 1]])
        print(' - number of all points in the buffer   = ', str(self.numpoint))
        print(' - buffer size               = ', str(self.bufsize))

        if isinstance(self.linecolor, str):
            color = '\'' + self.linecolor + '\''
        else:
            color = str(self.linecolor)

        print(' - line color      = ', color)

        if isinstance(self.patchcolor, str):
            color = '\'' + self.patchcolor + '\''
        else:
            color = str(self.patchcolor)

        print(' - patch color    = ', color)

        print(' - line width   = ', str(self.linewidth))
        print(' - line style     = \'' + self.linestyle + '\'')
        print(' - marker style  = \'' + self.marker + '\'')
        print(' - marker size  = ', str(self.markersize))
        print(' - animation delay = ', str(self.delay))

    def _add_colon(self):
        """ Increase each buffer array by 1 more column """
        self.xdata = np.append(self.xdata, 0)
        self.ydata = np.append(self.ydata, 0)
