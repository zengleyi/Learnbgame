# ManuelbastioniLAB - Copyright (C) 2015-2018 Manuel Bastioni
# Official site: www.manuelbastioni.com
# MB-Lab fork website : https://github.com/animate1978/MB-Lab
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import numpy as np
import os
import time

import bpy
from . import algorithms


logger = logging.getLogger(__name__)


class MaterialEngine:
    generated_disp_modifier_ID = "mbastlab_displacement"
    generated_disp_texture_name = "mbastlab_displ_texture"
    subdivision_modifier_name = "mbastlab_subdvision"
    parameter_identifiers = ("skin_", "eyes_")

    def __init__(self, obj_name, character_config):

        data_path = algorithms.get_data_path()
        self.obj_name = obj_name

        image_file_names = {
            "displ_data": character_config["texture_displacement"],
            "body_derm": character_config["texture_albedo"],
            "body_displ": character_config["name"]+"_displ.png",
            "body_spec": character_config["texture_specular"],
            "body_rough": character_config["texture_roughness"],
            "eyes_albedo": character_config["texture_eyes"],
            "body_bump": character_config["texture_bump"],
            "body_subd": character_config["texture_subdermal"],
        }

        image_file_paths = {}

        for img_id, value in image_file_names.items():
            image_file_paths[img_id] = os.path.join(
                os.path.join(data_path, "textures"),
                value
            )

        self.image_file_paths = image_file_paths
        self.image_file_names = image_file_names
        self.load_data_images()
        self.generate_displacement_image()

    def load_data_images(self):
        for img_path in self.image_file_paths.values():
            algorithms.load_image(img_path)

    def load_texture(self, img_path, shader_target):
        algorithms.load_image(img_path)
        self.image_file_names[shader_target] = os.path.basename(img_path)
        self.update_shaders()

    @property
    def texture_dermal_exist(self):
        return os.path.isfile(self.image_file_paths["body_derm"])

    @property
    def texture_spec_exist(self):
        return os.path.isfile(self.image_file_paths["body_spec"])

    @property
    def texture_rough_exist(self):
        return os.path.isfile(self.image_file_paths["body_rough"])

    @property
    def texture_subd_exist(self):
        return os.path.isfile(self.image_file_paths["body_subd"])

    @property
    def texture_eyes_exist(self):
        return os.path.isfile(self.image_file_paths["eyes_albedo"])

    @property
    def texture_bump_exist(self):
        return os.path.isfile(self.image_file_paths["body_bump"])

    @property
    def texture_displace_exist(self):
        return os.path.isfile(self.image_file_paths["displ_data"])

    @staticmethod
    def calculate_disp_pixels(blender_image, age_factor, tone_factor, mass_factor):
        logger.info('start: calculate_disp_pixels %s', blender_image.name)
        tone_f = tone_factor if tone_factor > 0.0 else 0.0

        ajustments = np.array([0.0, 0.5, 0.5, 0.5], dtype='float32')
        factors = np.fmax(np.array([1, age_factor, tone_f, (1.0 - tone_f) * mass_factor], dtype='float32'), 0.0)
        np_image = np.array(blender_image.pixels, dtype='float32').reshape(-1, 4)
        # add_result = r + age_f * (g - 0.5) + tone_f * (b - 0.5) + mass_f * (a - 0.5)
        add_result = np.sum((np_image - ajustments) * factors, axis=1)
        result_image = np.insert(np.repeat(np.fmin(add_result, 1.0), 3).reshape(-1, 3), 3, 1.0, axis=1)
        logger.info('finish: calculate_disp_pixels %s', blender_image.name)
        return result_image.flatten()

    @staticmethod
    def multiply_images(image1, image2, result_name, blending_factor=0.5):
        logger.info('multiply_images %s', result_name)
        if images_scale(image1, image2):
            np_img1, np_img2 = np.array(image1.pixels, dtype='float32'), np.array(image2.pixels, dtype='float32')

            result_img = new_image(result_name, image2.size)
            result_img.pixels = np_img1 * np_img2 * blending_factor + (np_img1 * (1.0 - blending_factor))
        logger.info('finish: multiply_images %s', result_name)

    @staticmethod
    def assign_image_to_node(material_name, node_name, image_name):
        logger.info("Assigning the image %s to node %s", image_name, node_name)
        mat_node = algorithms.get_material_node(material_name, node_name)
        mat_image = algorithms.get_image(image_name)
        if mat_image:
            algorithms.set_node_image(mat_node, mat_image)
        else:
            logger.warning("Node assignment failed. Image not found: %s", image_name)

    def get_material_parameters(self):

        material_parameters = {}

        obj = self.get_object()
        for material in algorithms.get_object_materials(obj):
            if material.node_tree:
                for node in algorithms.get_material_nodes(material):
                    is_parameter = False
                    for param_identifier in self.parameter_identifiers:
                        if param_identifier in node.name:
                            is_parameter = True
                            break
                    if is_parameter:
                        node_output_val = algorithms.get_node_output_value(node, 0)
                        material_parameters[node.name] = node_output_val
        return material_parameters

    def update_shaders(self, material_parameters=[], update_textures_nodes=True):

        obj = self.get_object()
        for material in algorithms.get_object_materials(obj):
            nodes = algorithms.get_material_nodes(material)
            if not nodes:
                continue

            for node in nodes:
                if node.name in material_parameters:
                    value = material_parameters[node.name]
                    algorithms.set_node_output_value(node, 0, value)
                elif update_textures_nodes:
                    if "_skn_albedo" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_derm"])
                    if "_skn_specular" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_spec"])
                    if "_skn_roughness" in node.name:
                        self.assign_image_to_node(material.name, node.name,
                                                  self.image_file_names["body_rough"])
                    if "_skn_subdermal" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_subd"])
                    if "_eys_albedo" in node.name:
                        self.assign_image_to_node(material.name, node.name,
                                                  self.image_file_names["eyes_albedo"])
                    if "_eylsh_albedo" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_derm"])
                    if "_tth_albedo" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_derm"])
                    if "_skn_bump" in node.name:
                        self.assign_image_to_node(material.name, node.name, self.image_file_names["body_bump"])
                    if "_skn_disp" in node.name:
                        self.assign_image_to_node(material.name, node.name,
                                                  self.image_file_names["body_displ"])

    def rename_skin_shaders(self, prefix):
        obj = self.get_object()
        for material in algorithms.get_object_materials(obj):
            if prefix != "":
                material.name = prefix + "_" + material.name
            else:
                material.name = material.name+str(time.time())

    def get_object(self):
        return algorithms.get_object_by_name(self.obj_name)

    def generate_displacement_image(self):
        disp_data_image_name = self.image_file_names["displ_data"]
        if disp_data_image_name != "":
            disp_data_image = algorithms.get_image(disp_data_image_name)
            if disp_data_image:
                disp_size = disp_data_image.size
                logger.info(
                    "Creating the displacement image from data image %s with size %sx%s",
                    disp_data_image.name, disp_size[0], disp_size[1])
                new_image(self.image_file_names["body_displ"], disp_size)
            else:
                logger.warning(
                    "Cannot create the displacement modifier: data image not found: %s",
                    algorithms.simple_path(self.image_file_paths["displ_data"]))

    def calculate_displacement_texture(self, age_factor, tone_factor, mass_factor):
        time1 = time.time()
        disp_data_image_name = self.image_file_names["displ_data"]

        if disp_data_image_name != "":
            disp_data_image = algorithms.get_image(disp_data_image_name)

            if disp_data_image:

                if self.image_file_names["body_displ"] in bpy.data.images:
                    disp_img = bpy.data.images[self.image_file_names["body_displ"]]
                else:
                    logger.warning("Displace image not found: %s", self.image_file_names["body_displ"])
                    return

                if self.generated_disp_modifier_ID in bpy.data.textures:
                    disp_tex = bpy.data.textures[self.generated_disp_modifier_ID]
                else:
                    logger.warning("Displace texture not found: %s", self.generated_disp_modifier_ID)
                    return

                if images_scale(disp_data_image, disp_img):
                    disp_img.pixels = self.calculate_disp_pixels(disp_data_image, age_factor, tone_factor, mass_factor)
                    disp_tex.image = disp_img
                    logger.info("Displacement calculated in %s seconds", time.time()-time1)
            else:
                logger.error("Displace data image not found: %s",
                             algorithms.simple_path(self.image_file_paths["displ_data"]))

    def save_texture(self, filepath, shader_target):
        img_name = self.image_file_names[shader_target]
        logger.info("Saving image %s in %s", img_name, algorithms.simple_path(filepath))
        algorithms.save_image(img_name, filepath)
        algorithms.load_image(filepath)  # Load the just saved image to replace the current one
        self.image_file_names[shader_target] = os.path.basename(filepath)
        self.update_shaders()


def new_image(name, img_size, color=(0.5, 0.5, 0.5, 1)):
    logger.info("Creating new image %s with size %sx%s", name, *img_size)
    try:
        bpy.data.images.remove(bpy.data.images[name], do_unlink=True)
        logger.info("Previous existing image %s replaced with the new one", name)
    except KeyError:
        pass

    new_img = bpy.data.images.new(name, *img_size)
    new_img.generated_color = color
    logger.info("created new image %s", name)
    return new_img


def images_scale(image1, image2):
    try:
        if image1.size[0] == image1.size[1] and image2.size[0] == image2.size[1]:
            if image1.size[0] > image2.size[0]:
                image2.scale(*image1.size)
            elif image1.size[0] < image2.size[0]:
                image1.scale(*image2.size)
            return True
        return False
    except (AttributeError, KeyError):
        return False
