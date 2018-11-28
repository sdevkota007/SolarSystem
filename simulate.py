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
        cam.process_keyboard("FORWARD", 0.05)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.05)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.05)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.05)


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

    sun_tex = TextureLoader.load_texture("objects/sun/sun.jpg")
    earth_tex = TextureLoader.load_texture("objects/earth/earth.jpg")
    mercury_tex = TextureLoader.load_texture("objects/mercury/mercury.jpg")
    venus_tex = TextureLoader.load_texture("objects/venus/venus.jpg")
    mars_tex = TextureLoader.load_texture("objects/mars/mars.jpg")
    jupiter_tex = TextureLoader.load_texture("objects/jupiter/jupiter.jpg")
    saturn_tex = TextureLoader.load_texture("objects/saturn/saturn.jpg")
    uranus_tex = TextureLoader.load_texture("objects/uranus/uranus.jpg")
    neptune_tex = TextureLoader.load_texture("objects/neptune/neptune.jpg")

    glEnable(GL_TEXTURE_2D)
    glUseProgram(shader)

    glClearColor(0.0, 0.2, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)



    # view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, -10.0, -60.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(65.0, w_width / w_height, 0.1, 1000.0)
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
    glUniform3f(Light_location_loc, 0, 5, 8)
    glUniform4f(Material_ambient_loc, 0.4, 0.4, 0.4, 1.0)
    glUniform4f(Material_diffuse_loc, 0.15, 0.15, 0.15, 1.0)
    glUniform4f(Material_specular_loc, 1.0, 1.0, 1.0, 1.0)
    glUniform1f(Material_shininess_loc, .95)

    theta = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()

        do_movement()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        time = glfw.get_time()

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


        #************************************SUN****************************************
        glBindTexture(GL_TEXTURE_2D, sun_tex)
        # scale up the size of sun
        size_ratio_relative_to_earth = 2.0
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
        # rotation
        rotation_speed = time * 0.002
        model_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
        rot_x = matrix44.create_from_y_rotation(rotation_speed)
        model = matrix44.multiply(rot_x, model_pos)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        #----create normalMatrix-----
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        #*******************************************************************************



        #********************************EARTH******************************************
        glBindTexture(GL_TEXTURE_2D, earth_tex)

        revolution_speed = time * 0.1
        rotation_speed = time * 1
        # scale planet
        size_ratio_relative_to_earth = 1.0
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([10.0, 0.0, 0.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta+0.1

        # ********************************Mercury******************************************
        glBindTexture(GL_TEXTURE_2D, mercury_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        # scale planet
        size_ratio_relative_to_earth = 0.38
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth,
                                                                size_ratio_relative_to_earth]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([5.0, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Venus******************************************
        glBindTexture(GL_TEXTURE_2D, venus_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 7
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Mars******************************************
        glBindTexture(GL_TEXTURE_2D, mars_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 12
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Jupiter******************************************
        glBindTexture(GL_TEXTURE_2D, jupiter_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 15
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Saturn******************************************
        glBindTexture(GL_TEXTURE_2D, saturn_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 18
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Uranus******************************************
        glBindTexture(GL_TEXTURE_2D, uranus_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 21
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1

        # ********************************Neptune******************************************
        glBindTexture(GL_TEXTURE_2D, neptune_tex)

        revolution_speed = time * 0.4
        rotation_speed = time * 1.5
        distance_from_sun = 24
        # scale down planet
        scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
        glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)

        # translation
        model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
        revolution = matrix44.create_from_y_rotation(revolution_speed)
        rotation = matrix44.create_from_y_rotation(rotation_speed)
        # revolution about z axis
        model = matrix44.multiply(model, revolution)
        # rotation about own axis
        model = matrix44.multiply(rotation, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        # ----create normalMatrix--
        modelView = numpy.matmul(view, model)
        modelView33 = modelView[0:-1, 0:-1]
        normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
        # -----------------
        glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
        theta = theta + 0.1


        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()