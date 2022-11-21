from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

import numpy as np
import glm

#GT_HINTS for draw process
GT_LINE = 'GT_LINE'
GT_LINES = 'GT_LINES'
GT_TRIANGLE= 'GT_TRIANGLE'
GT_CIRCLE = 'GT_CIRCLE' 
GT_POINTS = 'GT_POINTS'
GT_RECT = "GT_RECT"


class Window:
    '''
    Window Class for Creating Window Objects

    Attributes
    -----------
    height : (integer)
    width : (integer) 
    title : (string) - window title
    background : (tupple) - background color (R,G,B)
    '''
    def __init__(self, height, width, title, background=(0,0,0)):
        #main window parameters
        self.height = height
        self.width = width
        self.title = title
        self.background = background

 
class Shape:
    def __init__(self,vertex_array,color,alpha=1):
        #set draw object parameters
        self.vertex_array = np.array(vertex_array, dtype=np.float32)
        self.color = color
        self.alpha = alpha

        #translation parameters
        self.X = 0
        self.Y = 0
        self.Z = 0

        #rotation parameters
        self.rot_X = 0


    def _draw(self,gtHint,properties=dict()):
        '''
        This method finilize the draw process on the
        screen.

        Parameters
        ------------
        gtHint : <type : str> This hints the method
                what to draw.
                Hits are: 
                GT_LINE : draw single line
                GT_TRIANGLE : draw triangle
                GT_CIRCLE : draw circle
                GT_LINES : draw lines by connecting
                            given points
                GT_POINTS : draw points

        properties : hold given properties to the method.
        '''
        if gtHint == GT_LINE:
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glLineWidth(properties['line_width'])
            glDrawArrays(GL_LINES, 0, 2)

        elif gtHint == GT_LINES:
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            glLineWidth(properties['line_width'])
            glDrawArrays(GL_LINE_STRIP, 0, properties['count'])

        elif gtHint == GT_TRIANGLE:
            if properties['fill'] == True:
                glDrawArrays(GL_TRIANGLES, 0, 3)
            else:
                glDrawArrays(GL_LINE_LOOP, 0, 3)
        
        elif gtHint == GT_CIRCLE:
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            if properties['fill'] == True:
                glDrawArrays(GL_TRIANGLE_FAN, 0, properties['count'])
            else:
                glLineWidth(properties['line_width'])
                glDrawArrays(GL_LINE_LOOP, 0, properties['count'])
                
        elif gtHint == GT_POINTS:
            glPointSize(properties['point_size'])
            glDrawArrays(GL_POINTS, 0, properties['count'])

        elif gtHint == GT_RECT:
            if properties['fill'] == True:
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            else:
                glDrawArrays(GL_LINE_LOOP, 0, 4)
        #shader reset, UNBIND and DELETE VAO/VBO
        glUseProgram(0),
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class EventListener:
    '''
    Interface between Screen and User Defined Function.

    This class handles event function that is given to
    screen object. It basically runs the given fucntion
    in display loop.

    To connect the EventListener listener() method 
    needs to be called with Screen object.

    GT_CONTROL flag is need to be passed with the 
    listener() method to tell the EventListener to run
    eventProcess() method.

    For Example: 
    >>> screen = Screen(700,700,'Test Program')
    >>> screen.listener() # to set the EVENT_FLAG = True
    '''
    def __init__(self):
        self.EVENT_FLAG = False

    def listen(self):
        if self.events == []:
            self.EVENT_FLAG = False # to stop listening from Display loop
            print("Warning : No Event Function passed.")
        else:
            if self.EVENT_FLAG==True:
                for func in self.events:
                    self.eventProcess(func)

    def listener(self):
        self.events = []
        self.EVENT_FLAG = True

    def event(self,func):
        # event will handle more than one function passed by user
        self.events.append(func)

    def eventProcess(self,func):
        func()



class Communicator:
    '''
    Interface Between Screen and Controller
    '''
    def __init__(self) -> None:
        raise NotImplementedError


        