# Gonit
This is a simple mathematical visualization package for python.


<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="https://drive.google.com/uc?export=view&id=1Ad_qZYUwAmgHxGMw_JnT8I4efLBb8Nuf" 
alt="IMAGE ALT TEXT HERE" style="display: block;
  margin-left: auto;
  margin-right: auto;
  width: 398px;
  height:166" /></a>

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
* Should have [Git](https://git-scm.com/) installed on your system.
* Python Version 3.8

### Creating Window
```python
from gonit import *

screen = Screen(700,700,"Example: Gonit Screen")
screen.display()
```
This will create a 700x700 black/white screen. The screen will be empty. *Display()* function takes a list of shapes to be drawn on the screen.

### Drawing a simple Triangle

```python
from gonit import *


screen = Screen(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

screen.display([t1])
```
### Other Draw Functionalities
```python
Rectangle(vertex_array,(r,g,b), fill=False)
```

```python
Line(vertex_array, color=(r,g,b), alpha=1, line_width=1))
```
```python
Circle(color=(r,g,b), fill=False, center=(0, 0, 0), radius=1, line_width=2, alpha=1)
```
```python
Points(vertex_array, color, alpha=1, point_size=1)
```
```python
Grid(color=(200, 190, 250), alpha=0.5, res=0.1, line_width=1)
```
```python
Axis(color=(200, 190, 250), alpha=1, line_width=1)
```



## Executing Callback Functions (Events)
Callback functions can be executed when the screen is in display. To do that first we have to activate the listener.
```
screen.listener()
```
Then we can add one or multiple callback functions by `event()` method.

```
def animate():
  pass

screen.listener()
screen.event(animate)
```
See the [example](/exmaples/animation_example.py).

## Important Information
* OpenGL coordinate system is by default set to normalised device coordinator (NDC). That means all the X, Y, or Z components will be between -1 to 1.
  
* Current implementation of this package is consistent with 2D drawings. However, Z components also need to be passed (can be set to 0). The 3D feature will be implemented in future version.
