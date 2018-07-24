import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, lines
import matplotlib.colors as mclr
from .exceptions import *


class Pero:
    """
    #Pero Class
    #
    #Class method:
    # Pero, punct, vector, draw, flip, transform, set, print
    #
    #-------------------------------------------------------------------------
    #Version: 1.1
    #Date: 24.10.2013

    # % properties( Access = private )
    bufsize = 200; print bufsize# - is the column size of the buffer (1-th size of the arrays xdata, ydata)
    numpoint# - number of line points buffered
    xdata# - buffer
    ydata# - buffer

    daraw_enable_at_bufsize_equal_1 = 'off'; print daraw_enable_at_bufsize_equal_1# - relevant only when bufsize = 1:
    # used to enable invocation of the method draw of the methods punct, vector
    # when bufsize = 1

    #Properties of the graphic object (created by the draw method ) by default:
    linecolor = 'b'; print linecolor
    patchcolor = 'b'; print patchcolor# - fill color
    linewidth = 0.5; print linewidth
    linestyle =' -'; print linestyle
    marker = 'none'; print marker
    markersize = 6; print markersize

    delay = 0; delay print# = added artificial time delay in the execution of the method draw, h
    #end % % properties private
    """

    def __init__(self, *args):
        """
        #Pero-class constructor or class method
        #
        #SYNTAX:
        # obj = Pero( x, y );
        # obj = Pero( p1,..., pn );
        #GIVEN:
        # - x, y = initial position coordinates of the pen = double scalars
        #
        # OR
        # p1,..., pn (n>0) - references (< handle) to Pero class objects
        #
        #GOTTA:
        # - obj = reference to a (NEW) Pero class object
        # - the internal buffer of the obj object contains the coordinates of the initial
        # the position of your pen
        #
        # OR
        # the internal buffer of an obj object contains a concatenation
        # the coordinates of the pen positions contained in p1...,p2
        #-------------------------------------------------------------------------
        #
        # The Pero object has an internal buffer.
        # If buffer size (number of points to fit) is 1,
        # plant of the pen (using the methods punct, vector) automatically lead
        # to build the graph. In this case, operations with the buffer using methods
        # draw and transform are not available ( an attempt to execute them results in an error ).
        #
        # If the buffer size is greater than 1, move the pen (using
        # methods punct, vector) new point graphics temporarily accumulate
        # in it, but not in the coordinate axes.
        # In this case, you need to use the draw method to build the chart
        # (only the last point is then stored in the buffer).
        #
        # Also, if the buffer size is greater than 1, then when the buffer is full, its size
        # automatically increases ( by the value of the original
        # buffer size).
        #
        # You can change the buffer size using the set method.
        """

        self.bufsize = 200  # - размер столбца буфера (1-й размер массивов xdata, ydata)
        self.numpoint = None  # - число точек линии, помещенных в буфер
        self.xdata = None  # - x buffer
        self.ydata = None  # - y buffer

        daraw_enable_at_bufsize_equal_1 = 'off'  # - актуально только при при bufsize = 1:
        # используется для обеспечения возможности вызова метода draw из методов punct, vector
        # в случае, когда bufsize = 1

        # Свойства графического объекта ( создаваемого методом draw ) по умолчанию:
        self.linecolor = 'b'
        self.patchcolor = 'b'  # - цвет заливки
        self.linewidth = 0.5
        self.linestyle = '-'
        self.marker = ''
        self.markersize = 6

        self.delay = 0  # = дополнительная искуственная временная задержка при выполнении метода draw, сек

        f = isinstance(args[0], (float, int))
        if f and len(args) != 2:
            raise CountParamsError

        for i in range(len(args)):
            if f and not isinstance(args[i], (float, int)):
                raise ParamsTypeError

            elif not f and not isinstance(args[i], Pero):
                raise ParamsPeroTypeError

        if f:  # && len(args) == 2 && оба имеют тип double
            x = args[0]
            y = args[1]
            if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
                raise ParamsScalarTypeError

            self.xdata = np.zeros(self.bufsize, dtype=float)
            self.ydata = np.zeros(self.bufsize, dtype=float)

            self.xdata[0] = x
            self.ydata[0] = y
            self.numpoint = 1
        else:  # f == 0 && все элементы args имеют тип Pero

            n = 0
            m = 0
            for i in range(len(args)):
                n = n + len(args[i].xdata)
                m = m + args[i].numpoint

            self.numpoint = m  # - число точек линии, помещенных в буфер

            if m <= 200:
                self.bufsize = 200  # - размер столбца буфера (1-й размер массивов xdata, ydata)
            else:
                self.bufsize = 2 * m

            self.xdata = np.zeros(self.bufsize, dtype=float)  # - буфер
            self.ydata = np.zeros(self.bufsize, dtype=float)  # - буфер
            m = 0
            for i in range(len(args)):
                k = args[i].numpoint
                self.xdata[m:m + k - 1] = args[i].xdata[0:k - 1]
                self.ydata[m:m + k - 1] = args[i].ydata[0:k - 1]
                m = m + k

            self.daraw_enable_at_bufsize_equal_1 = 'off'  # - актуально только при при bufsize = 1:
            # используется для обеспечения возможности вызова метода draw из методов punct, vector
            # в случае, когда bufsize = 1

            # Свойства графического объекта ( создаваемого методом draw ) по умолчанию:
            self.linecolor = 'b'
            self.patchcolor = 'b'  # - цвет заливки
            self.linewidth = 0.5
            self.linestyle = '-'
            self.marker = '.'
            self.markersize = 6

            self.delay = 0  # = дополнительная искуственная временная задержка при выполнении метода draw, сек

        self.hFig = plt.gcf()
        self.hAxes = plt.gca()
        self.hAxes.set_aspect('equal')
        plt.show(block=False)

    def flip(self):
        """
        # flip the contents of the object's internal buffer backwards
        #
        #SYNTAX:
        # obj2 = R. flip()
        :return:
        """

        obj2 = Pero(self)
        obj2.xdata = np.flipud(obj2.xdata)
        obj2.ydata = np.flipud(obj2.ydata)
        return obj2

    def set(self, *args):
        """
        #set-sets the property values of the Pero class object
        #
        #SYNTAX:
        # self.set ('lineColor', color) % - set line color
        # self.set ('patchColor', color) % - set fill color
        # self.set ('lineStyle', style) % - set line style
        # self.set ('lineWidth', width) % - set line thickness
        # self.set ('marker', marker) % - set marker type
        # self.set ('markerSize , size) % - set marker size
        # self.set ('bufsize', bufSize) % - set buffer size
        # self.set ('delay', delay) % - set the value of the artificial delay
        #
        # any set of properties from this number can also be set at the same time:
        #
        # self.set ('lineColor', color,..., 'delay', delay )
        #
        # (property-value pairs can follow in any order)
        #
        #GIVEN:
        # - obj = scalar object of Pero class
        # - color = color = ' b ' | ' r ' | ' g ' | ' y ' | ' k ' | ' w ' | ' m ' / 3-vector double
        #(initially the color is set to 'b')
        # - style = line style= '-' | '--' | ':' | '-.'|'none'
        #(initially the line style is set to' -')
        # - width = line thickness = scalar double
        #(initially the line thickness is set to 0.5)
        # - marker = marker type = + ' | 'o'|'*'/'.'|'x' | 'square' | 'diamond'/...
        # 'v' | '^' | '>' | '<' | 'pentagram' | 'hexagram' | 'none'
        # (originally set to 'none' )
        # - size = marker size = scalar double ( originally set to 6 )
        # - bufSize = buffer size
        # - delay = the duration of the artificial delay a sec. = scalar double
        # (initially set to 0 )
        #
        #GOTTA:
        # - the value of the property (s) has been changed to the corresponding values

        :param args:
        : return:
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

    def draw(self, *args):  # type=None, dx=None, dy=None):
        """
        #draw - строит линию или закрашивает участок ( или их
        #семейство ), координаты точек которой содержатся во внутреннем буфере
        #
        #СИНТАКСИС:
        #           self.draw()
        #           self.draw( type )
        #       h = self.draw();
        #       h = self.draw( type );
        #           self.draw( type, dx, dy )
        #       h = self.draw( type, dx, dy );
        #
        #ДАНО:
        # - obj = скалярный объект класса Pero
        # - установлен размер внутреннего буфера больше 1
        # - внутренний буфер содержит последовательность координат точек линии
        # - type = 'line' | 'patch' | []
        # ( по умолчанию type = 'line'  <=> type = [] )
        # - dx, dy - координаты вектора смещения пера
        # ( по умолчанию dx = dy = 0 )
        #
        #НАДО:
        # - в текущих координатных осях построена линия
        # с предопределенными свойствами
        # ( изменение предопределенных свойств может быть осуществлено с помощью метода set )
        #
        # - h = дескриптор построенной линии
        # - внутренний буфер содержит только последнюю точку из исходной
        # последовательности точек, СМЕЩЕННУЮ на вектор dx,dy
        # ( буфер содержит координаты текущего положения пера )
        # - построение линии выполнено с дополнительной искуственной временнОй
        # задержкой на предустановленную величину
        # ( по умолчанию величина задержки установлена равной 0, изменить
        # эту установку можно с помощью метода Set )
        #
        :param type:
        :param dx:
        :param dy:
        :return:
        """

        if self.bufsize == 1 and self.daraw_enable_at_bufsize_equal_1 == 'off':
            raise DrawBufsizeError

        n = self.numpoint
        h = None

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
        #vector - "перемещает" перо на заданный вектор от последней точки строящейся линии к новой
        #
        #СИНТАКСИС:
        #           self.vector( dx, dy )
        #ДАНО:
        # - obj = скалярный объект класса Pero
        # - внутренний буфер объекта obj содержит не пустую
        # последовательность точек (по крайней мере одну точку)
        # - dx, dy = координаты вектора смещения пера в следующую
        # точку линии = скаляры double
        #
        #НАДО:
        # - кординаты новой точки графика добавлены в буфер, если
        # установленный размер буфера больше 1, или новая точка
        # добавлена непосредственно к графику, если размер буфера равен 1
        :param dx:
        :param dy:
        :return:
        """

        if not isinstance(dx, (float, int)) or not isinstance(dy, (float, int)):
            raise ParamsScalarTypeError

        if len(self.xdata) == self.numpoint:
            self._add_colon()

        self.xdata[self.numpoint] = np.array(self.xdata[self.numpoint - 1]) + dx
        self.ydata[self.numpoint] = np.array(self.ydata[self.numpoint - 1]) + dy
        self.numpoint += 1

        if self.bufsize == 1:
            self.daraw_enable_at_bufsize_equal_1 = 'on'
            self.draw()
            self.daraw_enable_at_bufsize_equal_1 = 'off'

    def punct(self, x=None, y=None):
        """
        #punct - "перемещает" перо в точку с заданными координатами
        #
        #СИНТАКСИС:
        #           self.punct( x, y )
        #ДАНО:
        # - obj = скалярный объект класса Pero
        # - x,y = координаты точки = скаляры double
        #
        #НАДО:
        # - кординаты точки добавлены в буфер, если
        # установленный размер буфера больше 1, или новая точка
        # добавлена непосредственно к графику, если размер буфера равен 1
        :param x:
        :param y:
        :return:
        """

        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise ParamsScalarTypeError

        if len(self.xdata) == self.numpoint:
            self._add_colon()

        self.xdata[self.numpoint] = x
        self.ydata[self.numpoint] = y
        self.numpoint += 1

        if self.bufsize == 1:
            self.daraw_enable_at_bufsize_equal_1 = 'on'
            self.draw()
            self.daraw_enable_at_bufsize_equal_1 = 'off'

    def transform(self, f=None, *args):
        """
         #transform - выполняет преобразование координат точек, нахоящихся в буфере, по заданному закону
        #
        #СИНТАКСИС:
        #           self.transform( f )
        #           self.transform( f, p1,...,pn )
        #
        #ДАНО:
        # - obj = скалярный объект класса Pero
        # - установлен размер внутреннего буфера больше 1
        # - f = ССЫЛКА на функцию  ( function_handle ), осушествляющую
        # преобразование координатной плоскости и имеющую заголовок вида:
        #   function [ x2, y2 ] = F( x1, y1 )
        # или
        #   function [ x2, y2 ] = F( x1, y1, p1,...,pn )
        # соответственно, где x1, y1 - декартовы координаты прообраза некоторой
        # (произвольной) точки плоскости, x2, y2 - декартовы координаты её образа при
        # отображении F ( имя функции-преобразоания может быть каким угодно, но если,
        # как в примере, оно F, то входной параметр f = @F - это ССЫЛКА на функцию F )
        # - p1,...,pn - набор дополнительных параметров для функции f
        # (число дополнительных параметров и их типы могут быть любыми)
        #
        #НАДО:
        # - координаты всех точек, содержащихся во внутреннем буфере
        # obj, преобразованы при помощи функции f
        :param f:
        :param args:
        :return:
        """

        if self.bufsize == 1:
            raise TransformBufsizeError

        for i in range(self.numpoint):
            self.xdata[i], self.ydata[i] = f(self.xdata[i], self.ydata[i], *args)

    def print(self, mode=None):
        """
        Display a Pero class object in the command window
        #
        #SYNTAX:
        # self.print () - displays the Pero class object in the command window ( the main method of use )
        # self.print ('prime') - displays only basic information and only about the SCALAR object
        #
        #GIVEN:
        # - obj = Pero class object ( not necessarily scalar )
        # - [mode] = 'prime' - optional flag parameter;
        # in this case, obj - must be a scalar
        #
        : param mode:
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
