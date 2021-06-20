'''
Drawing Triangle in Gonit Screen

*** If does not work please report.
'''

# #setting directory
# import os, sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)


from gonit import *

screen = Screen(700,700,"Example: Triangle")

#Triangle vertices 
vertex_array = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]

t1 = Triangle(vertex_array,(255,0,0))

draw_objects = [t1] # you can also add Axis() and Grid()
screen.display()
