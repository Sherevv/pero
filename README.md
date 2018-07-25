# Pero

Graphic pen based on matplotlib. Also include Turtle class (see below).

[Описание на русском](README.ru.md)

# Requirements

- Python 3.6.x
- numpy
- matplotlib


# Installation
You should use command line terminal.

First variant. Clone repo and go to the package dir

```commandline
git clone https://github.com/Sherevv/pero.git pero

cd pero
```

and execute command:
```
python setup.py install
```
or
```
pip install .
```

Second variant. Remote using pip:

```
pip install git+https://github.com/Sherevv/pero.git
```

# Pero class

    obj = Pero( x, y )
    obj = Pero( p1,...,pn ) 
    
`x, y` - initial position coordinates of the pen

or
 
`p1, ..., pn` - references to Pero class objects


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

## Methods of Pero
**punct()** - move the pen to a point with specified coordinates

    obj.punct( x, y )

**vector()** - move the pen to the specified vector from the last point of the line under construction to the new one 
    
    obj.vector( dx, dy )
    
**set(params)** - set the property values of the Pero class object

    obj.set( 'lineColor' , color )    # set line color 
    obj.set( 'patchColor', color )    # set patch color
    obj.set( 'lineStyle' , style )    # set line style                
    obj.set( 'lineWidth' , width )    # set line width
    obj.set( 'marker'    , marker )   # set marker type
    obj.set( 'markerSize' , size )    # set marker size   
    obj.set( 'bufsize'   , bufSize )  # set buffer size                        
    obj.set( 'delay'     , delay )    # set the value of the artificial delay

any set of properties from this number can also be set at the same time:   
    
    obj.set( 'lineColor', color,..., 'delay', delay ) 
    
(property-value pairs can follow in any order)        

Parameters:
`color` = `'b' | 'r' | 'g' | 'y' | 'k' | 'w' | 'm' | вектор из 3-х чисел`  
(initially the color is set to`'b'`)  or other [values](https://matplotlib.org/api/colors_api.html)

`style` = `'solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':', 'None', ' ', ''` 
(initially the line style is set to `'-'`)

`width` - (initially the line thickness is set to  `0.5`)

`marker` = `'.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8',
'*', '+', '|', '_', 's', 'h', 'H', 'D', 'd', 'p', 'P', 'x', 'X', 'None', ' ', ''`
(initially set to `'None'` )

`size` (initially set to  `6`)

`bufSize` - buffer size (initially set to `200`)   
                     
`delay` -the duration of the artificial delay (sec.)
(initially set to  `0` )

**draw()** - draw a line or paints over a section whose point coordinates are contained in the internal buffer

    obj.draw()
    obj.draw( type )            
    h = obj.draw()   
    h = obj.draw( type )           
    obj.draw( type, dx, dy )            
    h = obj.draw( type, dx, dy )

`type` = `'line' | 'patch'`  (default type = `'line'`)

`dx, dy` - coordinates of the pen displacement vector (default dx = dy = `0`)

`h` - constructed line object

**flip()** - flip the contents of the object's internal buffer backwards
    
    obj2  = obj1.flip()

**transform(f, args)** - perform the conversion of point coordinates in the buffer according to a given law

    obj.transform( f )
    obj.transform( f, p1,...,pn )

`f` - function that dehumidifies convert the coordinate plane and having the semantic:

    x2, y2 = F( x1, y1 ) 

**print()** - display a Pero class object info in the command window

    obj.print()           # displays the Pero class object in the command window
    obj.print( 'prime' )  # displays only basic information  


# Turtle class

The Turtle class is a wrapper over the Pero class.
It has two properties (in addition to pen properties): step size and rotation angle.
`step` is specified by a complex number, method `forward()` moves the turtle along the vector `(Re(step), Im(step))`.

    obj = Turtle( x, y )
            
`x, y` - coordinates of the initial position of the turtle 

## Methods of Turtle

**forward()** - move the turtle along the set direction by the set step
 
    obj.forward()
    
**rot(side)** - turn the turtle at a fixed angle in a given direction

    obj.rot( side )
    
`side` - direction of turn, left = `'L' | 'LEFT'` or right = `'R' | 'RIGHT'` (case-insensitive)

**set(params)** - Set the property values of the Turtle class object like Pero method `set` 

    obj.set( 'angle'     , angle )    # sets the absolute value of the turtle's turning angle         
    obj.set( 'step'      , step )     # set the turtle step value            
    obj.set( 'lineColor' , color )    # set line color   
    ...
        
`angle` - the absolute value of the turtle's turning angle into rad. (initially set to `pi/2` )

`step`  - step size of the turtle (initially set to `1+i` ) 

Methods **draw()**, **transform()**, **print()** - correspond to the Pero class methods

# Basic usage

Create script, example start.py
```python
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
```

then execute script
```commandline
python start.py
```


# Usage with python command line
Prepare script with function (myfunc.py):
```python
def draw_cube(p):
    p.vector(0, 1)
    p.vector(1, 0)
    p.vector(0, -1)
    p.vector(-1, 0)
    p.draw()
    
```

then run python command line
```commandline
python
```


```
>>> from pero import Pero
>>> from myfunc import draw_cube
>>> p = Pero(1, 1)
>>> draw_cube(p)
```

[Code examples](pero/examples)