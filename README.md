# Gonit
This is an simple mathematical visualization package for python.

## Features
* Super Easy to Use
* Geomatric Shapes
* Text
* Opacity Control
* Event Handler

## Quick Start Guide
### How to Install:
Windows Command Prompt
```
pip install git+https://github.com/ipritom/gonit-opengl
```
### Creating Window
```python
from gonit import *

screen = window(700,700,"Example: Gonit Screen")
screen.display()
```
This will create a 700x700 black/white screen. The screen will be empty. *Display()* function takes a list of shapes to be drawn on the screen.

### Drawing a simple Triangle

```python
from gonit import *


screen = window(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

screen.display([t1])
```
