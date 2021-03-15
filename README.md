# Gonit
This is an simple mathematical visualization Package for python.

### Features
* Super Easy to Use
* Geomatric Shapes
* Text
* Opacity Control
* Shape Controller (Experimental)

### Quick Start Guide
Creating Window
```
from gonit import *

screen = window(700,700,"Example: Gonit Screen")
screen.display()
```
This will create a 700x700 black/white screen. The screen will be empty. *Display()* function takes a list of shapes to be drawn on the screen.

Drawing a simple Triangle.

```
from gonit import *


screen = window(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

screen.display([t1])
```
