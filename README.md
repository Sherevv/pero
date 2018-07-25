# Pero

Graphic pen based on matplotlib

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

# Pero methods
**punct()**

**vector()**

**set(params)**

# Basic usage

Create script, example start.py
```python
from pero import Pero

p = Pero(0, 1)
p.punct(1,1)
p.punct(0,1)
p.draw()
p.set('linecolor', 'r')
p.vector(1,1)
p.draw()  # your need call draw method before each line parameter change (e.g. color)


input()  # to prevent close robot window
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
>>> from myfunc import draw_line
>>> p = Pero(1, 1)
>>> draw_line(p)
```