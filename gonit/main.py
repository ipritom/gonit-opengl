from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

import glfw
import glm
import numpy as np

import math
import time
import tkinter as tk

from .gonit_text import *
from .shader import *

class window:
    '''
    * Create Main diplay Window and a Control Panel Window
    * Initialize VERTEX_SHADER and FRAGMENT_SHADER

    Input:
        height,width,title

    For Example:
    >>> w = window(900,900,'TEST PROGRAM')
    >>> w.display()
    '''
    def __init__(self,height,width,title,background=(0,0,0)):
        #main window parameters
        self.height = height
        self.width = width
        self.title = title
        self.background = background

        #Control Panel window 
        self.cPanel = tk.Tk()
        self.cPanel.title('Control Panel')
        self.cPanel.geometry("500x500")
    
    def display(self,draw_objs=[]):
        self.draw_objs = draw_objs

        #creating window and display
        glfw.init()
        glfw.window_hint(glfw.SAMPLES,4) #to use MSAA in OpenGL
        glfw.window_hint(glfw.RESIZABLE, True)   
        self.window = glfw.create_window(self.height, self.width,self.title,None,None)
        glfw.make_context_current(self.window)
        
        #initialize shader programs
        self.shaderProgram = get_shaderProgram()
        self.text_shaderProgram = get_text_shaderProgram()
        
        #creating buffers program
        self.obj_VBO = glGenBuffers(1)

        self.text_VAO = glGenVertexArrays(1)
        self.text_VBO = glGenBuffers(1)

        #load Characters for text rendering 
        for obj in draw_objs:
            if isinstance(obj,Text):
                obj.Characters = init_chars(self.text_shaderProgram,
                                            self.height,
                                            self.width,
                                            obj.fontfile,
                                            obj.font_size,
                                            )
        
        #diplay loop
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.render(self.draw_objs)
            self.cPanel.update()
            
        glfw.terminate()
    
    def render(self,draw_objs=None):
        bg_r,bg_g,bg_b = self.background
        glClearColor(bg_r/255,bg_g/255,bg_b/255, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_MULTISAMPLE)
        
        #render objects
        if draw_objs != None:
            for obj in draw_objs:
                if isinstance(obj,Text):   
                    obj.draw(window,self.text_shaderProgram,self.text_VAO,self.text_VBO)
                else:
                    obj.draw(self.shaderProgram,self.obj_VBO)


        glfw.swap_buffers(self.window)
        #vertical synchronization(vsync) to reduce the load on GPU
        glfw.swap_interval(1) 

class Controller:
    '''
    Create Controller Window as Child to the Main Window.
    The Window is Finally Created in Draw method (if control_flag == True)
    
    Input:
        (main_window,draw_object)
    Output:
        Controller Window
    '''
    def __init__(self,object_name,X,Y,Z,rot_X):
        self.child = tk.Tk()
        
        self.trans_x_scale = tk.Scale(self.child,from_=-1,to=1,
                                length=200,resolution=0.01,
                                orient=tk.HORIZONTAL,
                                label='X Axis')
        self.trans_y_scale = tk.Scale(self.child,from_=-1,to=1,
                                  length=200,resolution=0.01,
                                  orient=tk.HORIZONTAL,
                                  label='Y Axis')
        self.trans_z_scale = tk.Scale(self.child,from_=-1,to=1,
                                  length=200,resolution=0.01,
                                  orient=tk.HORIZONTAL,
                                  label='Z Axis')         
        self.trans_x_scale.set(X)
        self.trans_y_scale.set(Y)
        self.trans_z_scale.set(Z)

        self.trans_x_scale.pack()
        self.trans_y_scale.pack()
        self.trans_z_scale.pack()

        self.rot_X_scale = tk.Scale(self.child,from_=-360,to=360,
                            length=200,resolution=0.1,
                            orient=tk.HORIZONTAL,
                            label='Angle')
        self.rot_X_scale.set(rot_X)
        self.rot_X_scale.pack()

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
        #control and animation Flag
        self.control_flag = False
        self.animation_flag = False

    def add_controller(self,main_window,object_name):
        '''
        Create a Controller Window for a specific object
        '''
        cPanel = main_window.cPanel
        self.object_name = object_name
        self.controller_button = tk.Button(cPanel,text=object_name,command=self.controller_window)
        self.controller_button.pack()

    def controller_window(self):
        self.control_flag = True
        self.controller_button.config(state=tk.DISABLED)
        self.controller = Controller(self.object_name,self.X,self.Y,self.Z,self.rot_X)
        self.controller.child.protocol("WM_DELETE_WINDOW",self.on_close)
        self.controller.child.title('Controller' +' - '+ self.object_name)
        self.controller.child.geometry("400x400")
        self.controller.child.update()
        
    def controller_scale(self):
        if self.control_flag == False:
            return (self.X,self.Y,self.Z,self.rot_X)
        else:
            X = self.controller.trans_x_scale.get()
            Y = self.controller.trans_y_scale.get()
            Z = self.controller.trans_z_scale.get()
            rot_X = self.controller.rot_X_scale.get()

            return (X,Y,Z,rot_X)

    def on_close(self):
        self.controller.child.destroy()
        self.control_flag = False
        self.controller_button.config(state=tk.ACTIVE)

    def animation(self,hint,parameters):
        '''
        hint : ROTATE, MOVE
        paramenters: [(x1,y1),(x2,y2)] or [a1,a2]
        '''
        pass


class Triangle(Shape):

    def draw(self, shaderProgram,VBO):
        glUseProgram(shaderProgram)
        #creating buffer and add data to buffer
        
        glBindBuffer(GL_ARRAY_BUFFER,VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
    
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
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
        
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
       
        

class Line(Shape):
    def __init__(self,vertex_array,color,alpha=1,line_width=1):
        super().__init__(vertex_array,color,alpha)
        self.line_width = line_width

    def draw(self, shaderProgram,VBO):
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
    
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
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(self.line_width)
        glDrawArrays(GL_LINES, 0, 2)

        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
       
   
        

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
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
    
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
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        if self.fill:
            glDrawArrays(GL_TRIANGLE_FAN, 0, int(len(self.vertex_array)/3))
        else:
            glLineWidth(self.line_width)
            glDrawArrays(GL_LINE_LOOP, 0, int(len(self.vertex_array)/3))
        
        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

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
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
    
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
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
    
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
        transform = glm.rotate(transform, math.radians(self.rot_X),glm.vec3(0,0,1))
        glUniformMatrix4fv(MVPLoc, 1, GL_FALSE, glm.value_ptr(transform))
            
        glPointSize(self.point_size)
        glDrawArrays(GL_POINTS, 0, int(len(self.vertex_array)/3))
        glUseProgram(0)

        #UNBIND and DELETE VAO/VBO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
      
        

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
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
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
        glUseProgram(shaderProgram)
        #add data to buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
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
        
        

if __name__ == '__main__':
    ###Example Program

    #Triangle vertices 
    vertex_array = [-0.5, -0.5, 0.0,
                     0.5, -0.5, 0.0,
                     0.0, 0.5, 0.0]

    #setting up window
    w = window(640,640,'example')

    #drawing tirangle and a line
    t1 = Triangle(vertex_array,(255,0,0),0.5)
    l1 = Line([0.5,0.5,0,-0.5,-0.5,0],(255,0,0))
    
    #controller (experimental)
    #l1.add_controller(w,'Line1')
    #t1.add_controller(w,'Triangle 1')
    
    #adding shapes to display
    w.display([Grid(),Axis(),t1,l1])