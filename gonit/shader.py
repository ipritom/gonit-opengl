'''
Shader Program for Gonit
September, 2020
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

VERTEX_SHADER = """

#version 330

    layout (location = 0) in vec4 position;
    uniform mat4 MVP;
    
    void main() {
    gl_Position = MVP*position;
}

"""

FRAGMENT_SHADER = """
#version 330
    out vec4 FragColor;
    uniform vec4 ourColor;
    void main() {
    FragColor = ourColor;
    }
"""
textVERTEX_SHADER = """
        #version 330 core
        layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
        out vec2 TexCoords;

        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
            TexCoords = vertex.zw;
        }
       """

textFRAGMENT_SHADER = """
        #version 330 core
        in vec2 TexCoords;
        out vec4 color;

        uniform sampler2D text;
        uniform vec3 textColor;

        void main()
        {    
            vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
            color = vec4(textColor, 1.0) * sampled;
        }
        """

def get_shaderProgram():
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)

    return shaderProgram

def get_text_shaderProgram():
    vertexshader = shaders.compileShader(textVERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(textFRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    
    return shaderProgram
