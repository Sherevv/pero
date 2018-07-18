import numpy as np
from .pero import Pero


class Turtle:
    """
    class Turtle

    Methods:
        forward, rot, draw, transform, set, print ( + методы суперкласса handle )
    """

    def __init__(self, x=None, y=None):
        """
        #Turtle - конструктор класса
        #
        #СИНТАКСИС:
        #           obj = Turtle( x, y );
        #
        #ДАНО:
        # - x, y = координаты начального положения черепахи = скаляры double 
        #
        # Первоначально внутренний буфер содержит только одну точку, в дальнейшем  
        # его содержимое может меняться при выполнении методов forward, draw
        #
        #НАДО:
        # - obj = ссылка ( < handle ) на объект класса Turtle
        # - внутренний буфер объекта obj содержит координаты начального 
        # положения черепахи
        #--------------------------------------------------------------
        #
        # Объект Turtle имеет внутренний буфер.
        # При размере буфера, равном 1, пермещения пера
        # автоматически приводят к построению графика. При этом
        # операции с буфером при помощи методов draw и Transform не
        # доступны ( попытка их выполнения приводит к ошибке ).
        # 
        # При размере буфера, большем 1, при перемещениях пера (с помощью 
        # методов Forvard, Punct, Vector) новые точки графика временно накапливаются
        # в нем, но не отображаются в координатных осях.
        # Для построеия графика, в этом случае, необходимо применять, метод draw
        # ( после этого в буфере сохраняется только последняя точка ).            
        #
        # Также, если размер буфера больше 1, то при переполнении буфера, его размер 
        # автоматически увеличивается ( на величину первоначального
        # размера буфера ) 
        #
        # Изменить размер буфера можно с помощью метода set.
        :param x: 
        :param y: 
        """

        self.pero = Pero(x, y)
        self.ort = 1 + 0j  # = вектор (комплесное число), определяющий направление черепахи
        self.angle = np.pi / 2  # = абсолютная величина угла поворота черепахи

    def rot(self, side=None):
        """
                #rot - разворачивает черепаху на фиксированный угол в заданном направлении
        #
        #СИНТАКСИС:
        #           self.rot( angle )
        #ДАНО:
        # - obj = ссылка на скалярный объект класса Turtle
        # - side = направление поворота = ( L | LEFT ) | ( R | RIGHT ) (регист значения не имеет)
        # 
        #НАДО:
        # - черепаха поверута на фиксированный угол в заданном
        # направлении (величину угла можно установить с помощью метода
        # set, изначально угол равен 90 град.)
        :param side: 
        :return: 
        """

        side = str.upper(side)

        if side in ('L', 'LEFT'):
            self.ort = self.ort * np.exp(1j * self.angle)
        elif side in ('R', 'RIGTH'):
            self.ort = self.ort * np.exp(-1j * self.angle)
        else:
            print('Не предусмотренное значение входного параметра')

    def forward(self):
        """
        #forward - перемещает черепаху вдоль установленного направления на установленный шаг
        #
        #СИНТАКСИC:  
        #           self.forward()
        #ДАНО: 
        # - obj = ссылка на скалярный объект класса Turtle
        #НАДО: 
        # - черепаха "переместилась" вперед на установленный шаг 
        #   (изменить величину шага можно спомощью метода set);
        # - новая точка графика добавлена в буфер ( но не отображена в
        # координатных осях), если установленный размер буфера равен 1,
        # или добавлена непосредственно к графику, если размер буфера
        # равен 1
        
        :return: 
        """

        self.pero.vector(self.ort.real, self.ort.imag)

    def draw(self, draw_type=None):
        """
        #draw - строит линию или закрашивает участок ( или их
        #семейство ), координаты точек которой содержатся во внутреннем буфере
        #
        #СИНТАКСИС:
        #           self.draw()
        #           self.draw( type )
        #       h = self.draw();
        #       h = self.draw( type );
        #
        #ДАНО:            
        # - obj = скалярный объект класса Pero
        # - установлен размер внутреннего буфера больше 1            
        # - внутренний буфер содержит последовательность координат точек линии 
        # - type = 'line' | 'patch'
        # ( по умолчанию type = 'line' )
        #
        #НАДО:
        # - в текущих координатных осях построена линия 
        # с предопределенными свойствами 
        # ( изменение предопределенных свойств может быть осуществлено с помощью метода set )
        # 
        # - h = дескриптор построенной линии
        # - внутренний буфер содержит только последнюю точку из исходной
        # последовательности точек ( = координаты текущего положения пера )
        # - построение линии выполнено с дополнительной искуственной временнОй 
        # задержкой на предустановленную величину
        # ( по умолчанию величина задержки установлена равной 0, изменить
        # эту установку можно с помощью метода Set )
        #
        :param draw_type:
        :return: 
        """

        return self.pero.draw(draw_type)

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
        # - f = ССЫЛКА на функцию (function_handle), осушествляющую
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
        """

        self.pero.transform(f, *args)

    def set(self, *args):
        """
        #set - устанавливает значения свойств объекта класса Turtle
        #
        #СИНТАКСИС:
        #       self.set( 'angle'     , angle )   % - установка абсолютной величины угла поворота черепахи
        #       self.set( 'step'      , step )    % - установка величины шага черепахи
        #       self.set( 'lineColor' , color )   % - установка цвета линии
        #       self.set( 'patchColor', color )   % - установка цвета заливки
        #       self.set( 'lineStyle' , style )   % - установка стиля линии
        #       self.set( 'lineWidth' , width )   % - установка толщины линии
        #       self.set( 'marker'    , marker )  % - установка типа маркера
        #       self.set( 'markerSize , size )    % - установка размера маркера
        #       self.set( 'bufsize'   , bufSize ) % - установка размера буфера
        #       self.set( 'delay'     , delay )   % - установка величины искуственной задержки
        #
        #   также любой набор свойств из этого числа можно устанавливать одновременно:    
        #    
        #       self.set( 'angle', angle, 'step', step, 'lineColor', color,..., 'delay', delay )
        #    
        #   (пары "свойство-значение" могут следовать в любом порядке)        
        #
        #ДАНО:
        # - obj   = скалярный объект класса Turtle
        # - angle = абсолютная величина угла поворота черепахи в рад.
        # ( изначально установлен угол np.pi/2 )
        # - step  = величина шага черепахи ( изначально установлен шаг 1 ) 
        #   -----------------------------------------------------------
        # - color = цвет = 'b' | 'r' | 'g' | 'y' | 'k' | 'w' | 'm' | 3-вектор double  
        #(изначально цвет устанавливается равным 'b')
        # - style = стиль линии = '-' | '--' | ':' | '-.' | 'none'   
        #(изначально стиль линии устанавливается равным '-')
        # - width  = толщина линии = скаляр double
        #(изначально толщина линии устанавливается равной 0.5)
        # - marker = вид маркеров = +' | 'o' | '*' | '.' | 'x' | 'square' | 'diamond' | ...
        #                        'v' | '^' | '>' | '<' | 'pentagram' | 'hexagram' | 'none'
        #( изначально установлено значение 'none' )
        # - size = размер маркеров = скаляр double ( изначально установлено значение 6 )
        #   -----------------------------------------------------------
        # - bufSize = размер буфера ( число вмещаемых в него точек; изначально устан размер 1 )            
        # - delay = длительность искуственной задержки в сек. = скаляр double
        #( изначально установлено значение 0 )
        #
        #НАДО: 
        # - значение свойства (свойств) изменено на соответствующие значения             
        :param args: 
        :return: 
        """

        if np.mod(len(args), 2) == 1:
            print('Число параметров, определяющих пары "свойство-значение", должно быть четным')

        for i in range(0, 2, len(args)):

            param = str.upper(args[i])
            if param == 'ANGLE':

                if isinstance(args[i + 1], (float, int)):
                    self.angle = args[i + 1]
                else:
                    print('Значение свойства \'angle\' должно быть числовым скаляром')

            elif param == 'STEP':

                if isinstance(args[i + 1], (float, int)):
                    self.ort = args[i + 1]
                else:
                    print('Значение свойства \'step\' должно быть числовым скаляром')
            else:
                self.pero.set(args[i:i + 1])

    def print(self):
        """ Displays information about object in console """

        print()
        print('Объект класса Turtle:')
        print(' - аргумент (град.) и модуль вектора направления черепахи = ', str(np.angle(self.ort, deg=True)),
              abs(self.ort))
        print(' - абсолютная величина угла поворота = ', str(self.angle * 180 / np.pi), ' град.')

        self.pero.print('prime')

        print(' - методы класса: rot, forward, draw, set, print')
