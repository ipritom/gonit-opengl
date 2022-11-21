#OpenGL packages
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

#other packages
import glfw
import glm
import numpy as np

#python packages 
import math
import time
import tkinter as tk

#gonit packages
from .gonit_text import *
from .shader import *
from .structure import *


def key_input_callback(window, key, scancode, action, mode):
    '''
    Key Input Callback Function to Detect Key Press and
    follow predefined action.
    '''
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
       glfw.terminate()

def clear_screen(background):
    '''
    This function clear the color buffers and blend the
    computed fragment color values with the values in 
    the color buffers.

    Parameters:
    backgroud : <type : typle> OpenGL background color. 
    '''
    R,G,B = background
    glClearColor(R/255, G/255, B/255, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_MULTISAMPLE)

def display_loop():
    '''
    Run Display Loop both for Screen and Controller
    '''
    raise NotImplementedError

def add_data_buffer(shaderProgram,vertex_array,VBO):
    '''
    Add data to buffer
    '''
    #using shaderProgram
    glUseProgram(shaderProgram)
    #add data to buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertex_array.nbytes, vertex_array, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)


class Screen(Window, EventListener):
    '''
    * Create Main Screen for Display
    * How Screen Functions:
    Create Screen -> Display -> Display Settings -> 
    -> (display loop) -> Clear Screen -> Render

    Attributes
    -----------
    height : <type : int>
    width :  <type : int> 
    title : <type : str> - window title
    background : (tupple) - background color (R,G,B):
    
    For Example:
    >>> w = Screen(900,900,'TEST PROGRAM')
    >>> w.display()
    '''
    def __init__(self, height, width, title, background=(0,0,0)):
        super().__init__(height, width, title, background)
        EventListener.__init__(self)
  
    def display(self,draw_objs=[]):
        '''
        This Method Create a Display on the Screen
        
        It calls display_settings() to initiate a GLFW 
        window. Then it runs the display loop. 
        
        In display loop it runs render() to render 
        objects on the screen. The display loop also 
        sense the key_input_callback and 
        control_listener().
        '''
        self.draw_objs = draw_objs
        self.display_settings()
        
        #display loop
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            clear_screen(self.background)
            #render objects
            self.render(self.draw_objs)
            #trace key press
            glfw.set_key_callback(self.window, key_input_callback)

            # event handling
            if self.EVENT_FLAG:
                self.listen()
            
        glfw.terminate()
 
    def render(self,draw_objs=None):
        '''
        Render Objects to Screen
 
        '''
        #render objects
        if draw_objs != None:
            for obj in draw_objs:
                obj.draw(self.shaderProgram,self.obj_VBO)
        
        glfw.swap_buffers(self.window)
        #vertical synchronization(vsync) to reduce the load on GPU
        glfw.swap_interval(1)


    def display_settings(self):
        #setting up screen display 
        glfw.init()
        glfw.window_hint(glfw.SAMPLES,4) #to use MSAA in OpenGL
        glfw.window_hint(glfw.RESIZABLE, True)   
        self.window = glfw.create_window(self.height, self.width,self.title,None,None) #glfw window
        glfw.make_context_current(self.window)
        
        #initialize shader programs
        self.shaderProgram = get_shaderProgram()
        self.text_shaderProgram = get_text_shaderProgram()
        
        #creating buffers program
        self.obj_VBO = glGenBuffers(1)
        self.text_VAO = glGenVertexArrays(1)
        self.text_VBO = glGenBuffers(1)


class Triangle(Shape):
    def __init__(self,vertex_array,color,fill=True,alpha=1,line_width=1):
        super().__init__(vertex_array,color,alpha)
        self.line_width = line_width
        self.fill = fill

    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)

        #transform matrix
        #self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                      self.Y,
                                                      self.Z))
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
        
        
        self._draw(GT_TRIANGLE,properties={'fill':self.fill,
                                            'line_width':self.line_width})


class Rectangle(Shape):
    def __init__(self,vertex_array,color,fill=True,alpha=1,line_width=1):
        super().__init__(vertex_array,color,alpha)
        self.line_width = line_width
        self.fill = fill

    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)

        #transform matrix
        #self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                      self.Y,
                                                      self.Z))
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
        
        
        self._draw(GT_RECT, properties={'fill':self.fill,
                                            'line_width':self.line_width})

class Line(Shape):
    def __init__(self,vertex_array,color,alpha=1,line_width=1):
        super().__init__(vertex_array,color,alpha)
        self.line_width = line_width

    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)
        
        #transform matrix
        # self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                      self.Y,
                                                      self.Z))
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))

        #draw process
        count = len(self.vertex_array)//3

        if count==2:
            self._draw(GT_LINE,properties={'line_width':self.line_width})

        else:
            self._draw(GT_LINES,properties={'line_width':self.line_width,
                                            'count':count})

       
   
        

class Circle(Shape):
    def __init__(self,color,fill=False,center=(0,0,0),radius=1,line_width=2,alpha=1):
        self.center = center
        self.radius = radius
        self.fill = fill
        self.line_width = line_width
        #generating vertex array for circle
        vertex_array = []
        X,Y,Z = self.center 
        for t in np.arange(-math.pi,math.pi,0.1):
            x = self.radius*math.cos(t)+X
            y = self.radius*math.sin(t)+Y
            vertex_array.append(x)
            vertex_array.append(y)
            vertex_array.append(Z)
        super().__init__(vertex_array,color,alpha)
        
    
    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)
        
        #transform matrix
        #self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
       
            
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                      self.Y,
                                                      self.Z))
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
        
        
        count = len(self.vertex_array)//3
        self._draw(GT_CIRCLE,properties={'fill':self.fill,
                                         'line_width':self.line_width,
                                         'count':count})
   

class Arrow(Shape):
    def __init__(self,color,alpha=1,point_size=1):
        vertex_array = [-0.3, 0.0, 0.0,
                         0.0, 0.3, 0.0,
                         0.3, 0.0, 0.0,
                         0.1, 0.0, 0.0,
                         0.1,-0.5, 0.0,
                        -0.1,-0.5, 0.0,
                        -0.1, 0.0, 0.0,
                        -0.1,-0.5, 0.0,
                         0.1, 0.0, 0.0
                        ]
        super().__init__(vertex_array,color,alpha)

    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)
        
        #transform matrix
        self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                 self.Y,
                                                 self.Z))
                                                 
        #transform = glm.perspective(self.X,self.Y,1,1)
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))

        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
            
        glLineWidth(1.5)
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertex_array)/3))
        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)     
        

class Points(Shape): 
    def __init__(self,vertex_array,color,alpha=1,point_size=1):
        super().__init__(vertex_array,color,alpha)
        self.point_size = point_size
    
    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)
        
        #transform matrix
        #self.X,self.Y,self.Z,self.rot_X = self.controller_scale()
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(self.X,
                                                      self.Y,
                                                      self.Z))
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))

        count = len(self.vertex_array)//3    
        self._draw(GT_POINTS,properties={'point_size':self.point_size,
                                         'count':count})
        
      
        

class Text:
    def __init__(self,text,x,y,scale=1,font_size=18,color=(170,250,255),fontfile="font\Vera.ttf"):
        self.text = text
        self.x = x
        self.y = y
        self.scale = scale
        self.font_size = font_size
        self.color = color
        self.fontfile = fontfile
        self.Characters = None 

    def draw(self,window,shaderProgram,VAO,VBO):
        render_text(window,shaderProgram,
                    self.text,
                    self.x,self.y,
                    self.scale,
                    self.Characters,
                    VAO,VBO,
                    self.color)

class Axis:
    def __init__(self,color=(200,190,250),alpha=1,line_width=1):
        #set draw object parameters
        vertex_array = [-1.0,0.0,0.0,
                         1.0,0.0,0.0,
                         0.0,1.0,0.0,
                         0.0,-1.0,0.0,]
        
        self.vertex_array = np.array(vertex_array, dtype=np.float32)
        self.line_width = line_width
        self.color = color
        self.alpha = alpha
        
    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    self.alpha)
        
        #transform matrix
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(0,
                                                      0,
                                                      0))
        transform = glm.rotate(transform, 0,glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))

        #Draw Axis
        glLineWidth(self.line_width)
        glDrawArrays(GL_LINES, 0, 4)
        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
              

class Grid:
    def __init__(self,color=(200,190,250),alpha=0.5,res=0.1,line_width=1):
        #set draw object parameters
        self.vertex_array = []
        
        #generating vertices for grid lines
        for i in np.arange(-1,1,res):
            self.vertex_array = self.vertex_array+[i,1,0]
            self.vertex_array = self.vertex_array+[i,-1,0]

        for i in np.arange(-1,1,res):
            self.vertex_array = self.vertex_array+[1,i,0]
            self.vertex_array = self.vertex_array+[-1,i,0]
            
        self.vertex_array = np.array(self.vertex_array, dtype=np.float32) 
        self.line_width = line_width
        self.color = color
        
    def draw(self, shaderProgram,VBO):
        #add vertex_array to shader
        add_data_buffer(shaderProgram,self.vertex_array,VBO)
        #accessing ourColor and MVP variable from shaderProgram
        vertexColorLoc = glGetUniformLocation(shaderProgram, "ourColor")
        MVPLoc = glGetUniformLocation(shaderProgram, "MVP")
        
        #changing Color
        r,g,b = self.color
        glUniform4f(vertexColorLoc,
                    r/255.0,
                    g/255.0,
                    b/255.0,
                    0.5)
        
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(0,0,0))
        transform = glm.rotate(transform, 0,glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
        #Draw Axis
        glLineWidth(self.line_width)
        glDrawArrays(GL_LINES, 0, int(len(self.vertex_array)/3))
        glUseProgram(0)

        #UNBIND and VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


        