'''
Animation Example Created with Gonit

*** If does not work please report.
'''
import math
from gonit import *


def animate():
    global draw_list
    index = 3
    r,g,b = draw_list[index].color
    t = draw_list[index].X
    draw_list[index].Y = 0.7*math.sin(2*math.pi*2*t)
    draw_list[index].X += 0.005
    draw_list[3].color = (r,g,b)
    #print(draw_list[2].X,draw_list[2].Y)
    if draw_list[index].X > 2:
        draw_list[index].X = 0
        draw_list[index].Y = 0

def sine_wave(a=1,f=1):
    vertex_array = []
    
    for x in np.arange(-1,1,0.01):
        y = a*math.sin(2*math.pi*f*x)
        vertex_array = vertex_array + [x,y,0]
    return vertex_array


#creating screen
screen = Screen(700,600,"Testing Screen",(33,33,33))
#creating Cricle object
circle1 = Circle((25,217,253),center=(-1,0,0),fill=True,radius=0.02,alpha=0.7)
#creating a sine line : Line Object
sine_line_vertex_array = sine_wave(0.7,2)
sine_line = Line(sine_line_vertex_array,(190,87,34),line_width=2)

#creating event and event listener and passing animation() function
screen.event(animate)
screen.listener(GT_CONTROL)

#all drawing objects in draw_list
draw_list = [Grid(),Axis(),sine_line,circle1]
#run display 
screen.display(draw_list)