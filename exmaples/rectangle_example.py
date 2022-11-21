'''
Drawing Rectangle in Gonit Screen

*** If does not work please report.
'''



from gonit import *

screen = Screen(700,700,"Example: Rectangle")

# Triangle vertices 
# vertex_array = [-0.5, -0.5, 0.0,
#                  -0.5, 0.5, 0.0,
#                  0.5, 0.5, 0.0,
#                  0.5, -0.5, 0.0,
#                  -0.5, -0.5, 0.0,
#                  0.5, 0.5, 0.0,]
vertex_array1 = [-0.6, 0.6, 0.0,
                 -0.1, 0.6, 0.0,
                 -0.1, 0.1, 0.0,
                  -0.6, 0.1, 0.0,]

vertex_array2 = [0.6, 0.6, 0.0,
                 0.1, 0.6, 0.0,
                 0.1, 0.1, 0.0,
                 0.6, 0.1, 0.0,]


vertex_array3 = [0.6, -0.6, 0.0,
                 0.1, -0.6, 0.0,
                 0.1, -0.1, 0.0,
                 0.6, -0.1, 0.0,]

vertex_array4 = [-0.6, -0.6, 0.0,
                 -0.6, -0.1, 0.0,
                 -0.1, -0.1, 0.0,
                  -0.1, -0.6, 0.0,]

rect1 = Rectangle(vertex_array1,(192,156,200), fill=True)

rect2 = Rectangle(vertex_array2,(192,156,200), fill=True)

rect3 = Rectangle(vertex_array3,(192,156,255), fill=True)

rect4 = Rectangle(vertex_array4,(192,156,255), fill=True)

draw_objects = [Axis(), Grid(), rect1, rect2, rect3, rect4] # you can also add Axis()

screen.display(draw_objects)
