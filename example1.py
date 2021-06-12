'''
Drawing Triangle gonit window
'''
# import os, sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

from gonit.gonit import *


screen = window(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

screen.display([t1])
