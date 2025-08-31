from typing import Tuple

import numpy as np
import trimesh

from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_center
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_y


def create_axis_mesh(size: float = 100) -> trimesh.Trimesh:
    """Creates a 3D axis mesh.

    Args:
        size: The length of the axis. Defaults to 100.

    Returns:
        The axis mesh.
    """
    return concatenate_meshes(
        _create_arrow_x(size=size, color=(255, 0, 0, 255)),
        _create_arrow_y(size=size, color=(0, 255, 0, 255)),
        _create_arrow_z(size=size, color=(0, 0, 255, 255)),
    )


def _create_arrow_z(size: float, color: Tuple[int, int, int, int]) -> trimesh.Trimesh:
    """Creates a 3D arrow mesh for the z-axis.

    Args:
        size: The length of the arrow. Defaults to 100.
        color: The color of the arrow. Defaults to (255, 0, 0, 255).

    Returns:
        The arrow mesh.
    """
    cylinder_height = size
    cylinder_radius = 0.1
    cone_height = 2
    cone_radius = 0.3

    cylinder = trimesh.creation.cylinder(radius=cylinder_radius, height=cylinder_height)
    cylinder.apply_transform(create_rotation_matrix_for_x(np.radians(90)))
    cylinder.apply_translation([0, 0, -cylinder_height/2+cone_height/2])

    cone = trimesh.creation.cone(radius=cone_radius, height=cone_height)
    cone.apply_transform(create_rotation_matrix_for_x(np.radians(90)))
    cone.apply_translation([0, -cylinder_height/2, -cylinder_height/2+cone_height/2])

    arrow_mesh = concatenate_meshes(cylinder, cone)
    arrow_mesh.visual.face_colors = color
    arrow_mesh = arrow_mesh.apply_transform(create_rotation_matrix_for_x(np.radians(-90)))

    arrow_mesh = move_to_center(arrow_mesh)
    arrow_mesh.apply_translation([0, 0, -arrow_mesh.bounds[:, 2][0]])

    return arrow_mesh


def _create_arrow_y(size: float, color: Tuple[int, int, int, int]) -> trimesh.Trimesh:
    """Creates a 3D arrow mesh for the y-axis.

    Args:
        size: The length of the arrow. Defaults to 100.
        color: The color of the arrow. Defaults to (0, 255, 0, 255).

    Returns:
        The arrow mesh.
    """
    z_arrow = _create_arrow_z(size=size, color=color)
    x_arrow = z_arrow.apply_transform(create_rotation_matrix_for_x(np.radians(-90)))
    return x_arrow


def _create_arrow_x(size: float, color: Tuple[int, int, int, int]) -> trimesh.Trimesh:
    """Creates a 3D arrow mesh for the x-axis.

    Args:
        size: The length of the arrow. Defaults to 100.
        color: The color of the arrow. Defaults to (0, 255, 0, 255).

    Returns:
        The arrow mesh.
    """
    z_arrow = _create_arrow_z(size=size, color=color)
    y_arrow = z_arrow.apply_transform(create_rotation_matrix_for_y(np.radians(-90)))
    return y_arrow
