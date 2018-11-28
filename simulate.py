import glfw
from OpenGL.GLUT import *
from OpenGL.GL import *
import ShaderLoader
import numpy
import pyrr
from pyrr import matrix44, vector3
import TextureLoader
from Camera import Camera
from PIL import Image
from ObjLoader import *
from properties import planets
import random
import math

cam = Camera()
keys = [False] * 1024
lastX, lastY = 640, 360
first_mouse = True



def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False


def do_movement():
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.5)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.5)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.5)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.5)


def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)



def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():

    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1280, 720
    aspect_ratio = w_width / w_height


    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    obj = ObjLoader()
    obj.load_model("objects/sphere.obj")

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


    for planet in planets:
        texture = TextureLoader.load_texture(planets[planet]['image_path'])
        planets[planet]['texture'] = texture

        #initial position
        if planet == 'sun':
            distance_from_sun = planets[planet]['distance_from_sun']
            planets[planet]['initial_position'] = [distance_from_sun, 0.0, distance_from_sun]
        else:
            distance_from_sun = 30.0 + planets[planet]['distance_from_sun']
            x = round(random.uniform(-distance_from_sun, distance_from_sun), 3)
            z = round(math.sqrt((distance_from_sun ** 2) - (x ** 2)), 3)
            planets[planet]['initial_position'] = [x, 0.0, z]


    glEnable(GL_TEXTURE_2D)
    glUseProgram(shader)

    glClearColor(0.0, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)


    projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 10000.0)
    scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))
    # # ---------------create normalMatrix-----------------
    # modelView = numpy.matmul(view, model)
    # modelView33 = modelView[0:-1, 0:-1]
    # normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
    # #-----------------------------------------------------------

    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    model_loc = glGetUniformLocation(shader, "model")
    normal_loc = glGetUniformLocation(shader, "normalMatrix")
    scale_loc = glGetUniformLocation(shader, "scale")
    scale_planet_loc = glGetUniformLocation(shader, "scale_planet")


    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(scale_loc, 1, GL_FALSE, scale)


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
    glUniform3f(Light_location_loc, 0, 0, 0)
    glUniform4f(Material_ambient_loc, 0.4, 0.4, 0.4, 1.0)
    glUniform4f(Material_diffuse_loc, 0.15, 0.15, 0.15, 1.0)
    glUniform4f(Material_specular_loc, 1.0, 1.0, 1.0, 1.0)
    glUniform1f(Material_shininess_loc, .95)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        do_movement()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        time = glfw.get_time()

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        # **********************************planets****************************************
        for planet in planets:
            glBindTexture(GL_TEXTURE_2D, planets[planet]['texture'])

            revolution_speed = time * planets[planet]['revolution_ratio_relative_to_earth']
            rotation_speed = time * planets[planet]['rotation_ratio_relative_to_earth']
            # scale planet
            scale_factor = planets[planet]['size_ratio_relative_to_earth']
            scale_planet = matrix44.create_from_scale(pyrr.Vector3([scale_factor,scale_factor,scale_factor]))
            glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

            # translation
            model = matrix44.create_from_translation(pyrr.Vector3(planets[planet]['initial_position']))
            revolution = matrix44.create_from_y_rotation(revolution_speed)
            rotation = matrix44.create_from_y_rotation(rotation_speed)
            # revolution about z axis
            model = matrix44.multiply(model, revolution)
            # rotation about own axis
            model = matrix44.multiply(rotation, model)

            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

            # ----create normalMatrix--
            modelView = numpy.matmul(view, model)
            modelView = numpy.matmul(modelView, scale_planet)
            modelView = numpy.matmul(modelView, scale)
            modelView33 = modelView[0:-1, 0:-1]
            normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
            # -----------------
            glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

            glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))

        # *******************************************************************************






        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()