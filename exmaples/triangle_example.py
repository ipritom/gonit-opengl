'''
Drawing Triangle in Gonit Screen

*** If does not work please report.
'''

from gonit import *

screen = Screen(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

draw_objects = [Grid(), t1] # you can also add Axis()

screen.display(draw_objects)
