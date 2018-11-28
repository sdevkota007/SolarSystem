# planets = ['sun', 'earth', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

planets = {
    'sun': {
                'image_path':'objects/sun/sun.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':30.0,
                'rotation_ratio_relative_to_earth': 0.0,
                'revolution_ratio_relative_to_earth': 0.0,
                'distance_from_sun':0.0,
                'initial_position': 0
                },
    'mercury': {
                'image_path':'objects/mercury/mercury.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':0.38,
                'rotation_ratio_relative_to_earth': 1.0,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':35.98
                },
    'venus': {
                'image_path':'objects/venus/venus.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':0.95,
                'rotation_ratio_relative_to_earth': 1,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':67.24
                },
    'earth': {
                'image_path':'objects/earth/earth.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':1.0,
                'rotation_ratio_relative_to_earth': 1,
                'revolution_ratio_relative_to_earth': 0.01,
                'distance_from_sun':92.96,
                'initial_position': 0
                },
    'mars': {
                'image_path':'objects/mars/mars.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':0.53,
                'rotation_ratio_relative_to_earth': 0.2,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':141.6
                },
    'jupiter': {
                'image_path':'objects/jupiter/jupiter.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':11.2,
                'rotation_ratio_relative_to_earth': 0.002,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':483.8,
                },
    'saturn': {
                'image_path':'objects/saturn/saturn.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':9.45,
                'rotation_ratio_relative_to_earth': 0.2,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':890.8,
                },
    'uranus': {
                'image_path':'objects/uranus/uranus.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':4.0,
                'rotation_ratio_relative_to_earth': 0.2,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':1784.0,
                },
    'neptune': {
                'image_path':'objects/neptune/neptune.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':3.88,
                'rotation_ratio_relative_to_earth': 0.002,
                'revolution_ratio_relative_to_earth': 0.1,
                'distance_from_sun':2793,
                }
            }

#
#
#
# #************************************SUN****************************************
# glBindTexture(GL_TEXTURE_2D, sun_tex)
# # scale up the size of sun
# size_ratio_relative_to_earth = 2.0
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
# # rotation
# rotation_speed = time * 0.002
# model_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
# rot_x = matrix44.create_from_y_rotation(rotation_speed)
# model = matrix44.multiply(rot_x, model_pos)
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# #----create normalMatrix-----
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# #*******************************************************************************
#
#
#
# #********************************EARTH******************************************
# glBindTexture(GL_TEXTURE_2D, earth_tex)
#
# revolution_speed = time * 0.1
# rotation_speed = time * 1
# # scale planet
# size_ratio_relative_to_earth = 1.0
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([10.0, 0.0, 0.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta+0.1
#
# # ********************************Mercury******************************************
# glBindTexture(GL_TEXTURE_2D, mercury_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# # scale planet
# size_ratio_relative_to_earth = 0.38
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth,
#                                                         size_ratio_relative_to_earth]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([5.0, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Venus******************************************
# glBindTexture(GL_TEXTURE_2D, venus_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 7
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Mars******************************************
# glBindTexture(GL_TEXTURE_2D, mars_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 12
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Jupiter******************************************
# glBindTexture(GL_TEXTURE_2D, jupiter_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 15
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Saturn******************************************
# glBindTexture(GL_TEXTURE_2D, saturn_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 18
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Uranus******************************************
# glBindTexture(GL_TEXTURE_2D, uranus_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 21
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1
#
# # ********************************Neptune******************************************
# glBindTexture(GL_TEXTURE_2D, neptune_tex)
#
# revolution_speed = time * 0.4
# rotation_speed = time * 1.5
# distance_from_sun = 24
# # scale down planet
# scale_planet = matrix44.create_from_scale(pyrr.Vector3([0.08, 0.08, 0.08]))
# glUniformMatrix4fv(scale_planet_loc, 1, GL_FALSE, scale_planet)
#
# # translation
# model = matrix44.create_from_translation(pyrr.Vector3([distance_from_sun, 0.0, 5.0]))
# revolution = matrix44.create_from_y_rotation(revolution_speed)
# rotation = matrix44.create_from_y_rotation(rotation_speed)
# # revolution about z axis
# model = matrix44.multiply(model, revolution)
# # rotation about own axis
# model = matrix44.multiply(rotation, model)
#
# glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
#
# # ----create normalMatrix--
# modelView = numpy.matmul(view, model)
# modelView33 = modelView[0:-1, 0:-1]
# normalMatrix = numpy.transpose(numpy.linalg.inv(modelView33))
# # -----------------
# glUniformMatrix3fv(normal_loc, 1, GL_FALSE, normalMatrix)
#
# glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))
# theta = theta + 0.1