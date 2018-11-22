import glfw
from OpenGL.GLUT import *
from OpenGL.GL import *
import ShaderLoader
import numpy
import pyrr

from PIL import Image
from ObjLoader import *

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():

    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 800, 600


    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    obj = ObjLoader()
    obj.load_model("objects/earth.obj")

    texture_offset = len(obj.vertex_index)*12
    normal_offset = (texture_offset + len(obj.texture_index)*8)

    shader = ShaderLoader.compile_shader("shaders/cruise_with_lighting.vs", "shaders/cruise_with_lighting.fs")

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

    #positions
    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #textures
    texCoords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(texCoords, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))
    glEnableVertexAttribArray(texCoords)
    #normals
    normals = glGetAttribLocation(shader, "vertNormal")
    glVertexAttribPointer(normals, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(normal_offset))
    glEnableVertexAttribArray(normals)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("objects/earth.jpg")
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)

    glUseProgram(shader)

    glClearColor(0.0, 0.4, 0.5, 1.0)
    glEnable(GL_DEPTH_TEST)


    # view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -900.0]))
    # projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 1000.0)
    # model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))

    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -4.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 1000.0)
    model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
    # # ---------------create normalMatrix-----------------
    # modelView = numpy.matmul(view, model)
    # modelView33 = modelView[0:-1, 0:-1]
    # normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
    # #-----------------------------------------------------------

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    normal_loc = glGetUniformLocation(shader, "normalMatrix")

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    transform_loc = glGetUniformLocation(shader, "transform")

    Global_ambient_loc = glGetUniformLocation(shader, "Global_ambient")
    Light_ambient_loc = glGetUniformLocation(shader, "Light_ambient")
    Light_diffuse_loc = glGetUniformLocation(shader, "Light_diffuse")
    Light_specular_loc = glGetUniformLocation(shader, "Light_specular")
    Light_location_loc = glGetUniformLocation(shader, "Light_location")
    Material_ambient_loc = glGetUniformLocation(shader, "Material_ambient")
    Material_diffuse_loc = glGetUniformLocation(shader, "Material_diffuse")
    Material_specular_loc = glGetUniformLocation(shader, "Material_specular")
    Material_shininess_loc = glGetUniformLocation(shader, "Material_shininess")

    glUniform4f(Global_ambient_loc, 0.8, 0.8, 0.9, 0.1)
    glUniform4f(Light_ambient_loc, 0.3, 0.3, 0.3, 1.0)
    glUniform4f(Light_diffuse_loc, 0.25, 0.25, 0.25, 1.0)
    glUniform4f(Light_specular_loc, 0.9, 0.9, 0.9, 1.0)
    glUniform3f(Light_location_loc, 0, 5, 8)
    glUniform4f(Material_ambient_loc, 0.4, 0.4, 0.4, 1.0)
    glUniform4f(Material_diffuse_loc, 0.15, 0.15, 0.15, 1.0)
    glUniform4f(Material_specular_loc, 1.0, 1.0, 1.0, 1.0)
    glUniform1f(Material_shininess_loc, .95)


    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time() )
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time() )

        # identity_mat = numpy.identity(4)
        # rot_x = identity_mat
        # rot_y = identity_mat
        transform_mat = rot_x*rot_y
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, transform_mat)

        # ---------------create normalMatrix-----------------
        modelView = numpy.matmul(transform_mat, view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------------------------------------------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))



        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()