from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

import glfw
import freetype
import glm

import numpy as np
from PIL import Image
import math

from .shader import *

class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')

def _get_rendering_buffer(xpos, ypos, w, h, zfix=0.0):
    return np.asarray([
        xpos,     ypos + h, 0, 0,
        xpos,     ypos,     0, 1,
        xpos + w, ypos,     1, 1,
        xpos,     ypos + h, 0, 0,
        xpos + w, ypos,     1, 1,
        xpos + w, ypos + h, 1, 0
    ], np.float32)


def init_chars(shaderProgram,window_height,window_width,fontfile,font_size=24):
    glUseProgram(shaderProgram)
    
    #get projection
    shader_projection = glGetUniformLocation(shaderProgram, "projection")
    W = window_width
    H = window_height
    projection = glm.ortho(-W/2, W/2, -H/2, H/2)
    glUniformMatrix4fv(shader_projection, 1, GL_FALSE, glm.value_ptr(projection))
    
    #disable byte-alignment restriction
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    face = freetype.Face(fontfile)
    face.set_char_size(font_size*64 )

    #load first 128 characters of ASCII set
    Characters = dict()
    for i in range(0,128):
        face.load_char(chr(i))
        glyph = face.glyph
        
        #generate texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                     GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

        #texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #now store character for later use
        Characters[chr(i)] = CharacterSlot(texture,glyph)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(0)
    
    return Characters
    
def render_text(window,shaderProgram,text,x,y,scale,Characters,VAO,VBO,color):
    r,g,b = color
    
    glUseProgram(shaderProgram)

    #configure VAO/VBO for texture quads
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),r/255,g/255,b/255) 
    glActiveTexture(GL_TEXTURE0)
    glBindVertexArray(VAO)
    
    for c in text:
        ch = Characters[c]
        w, h = ch.textureSize
        w = w*scale
        h = h*scale
        vertices = _get_rendering_buffer(x,y,w,h)

        #render glyph texture over quad
        glBindTexture(GL_TEXTURE_2D, ch.texture)
        #update content of VBO memory
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        #render quad
        glDrawArrays(GL_TRIANGLES, 0, 6)
        #now advance cursors for next glyph (note that advance is number of 1/64 pixels)
        x += (ch.advance>>6)*scale
    glBindTexture(GL_TEXTURE_2D, 0);
    glUseProgram(0)

    #UNBIND and DELETE VAO/VBO
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDeleteBuffers(1, id(VBO))
    glDeleteBuffers(1, id(VAO))

        
        
