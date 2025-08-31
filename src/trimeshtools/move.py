from contextlib import contextmanager
from typing import Union

import numpy as np
import trimesh


def move_to_center(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Moves the mesh to the center of the bounding box.

    Args:
        mesh: The mesh to be moved.

    Returns:
        The moved mesh.
    """
    return mesh.apply_translation(-mesh.centroid)


def move_to_floor(mesh: trimesh.Trimesh, offset: float = 0) -> trimesh.Trimesh:
    """Moves the mesh to the floor of the bounding box.

    Args:
        mesh: The mesh to be moved.
        offset: The distance to move the mesh below the floor. Default is 0.

    Returns:
        The moved mesh.
    """
    return mesh.apply_translation(_get_to_floor_offsets(mesh, offset))


def move_to_bound(
    mesh: trimesh.Trimesh,
    x: Union[float, None] = None,
    y: Union[float, None] = None,
    z: Union[float, None] = None,
) -> trimesh.Trimesh:
    """Moves the mesh to the specified boundary.

    Args:
        mesh (trimesh.Trimesh): The mesh to be moved.
        x: The distance to move the mesh along the x-axis. If None, the mesh is not moved along the x-axis.
            Default is None.
        y: The distance to move the mesh along the y-axis. If None, the mesh is not moved along the y-axis.
            Default is None.
        z: The distance to move the mesh along the z-axis. If None, the mesh is not moved along the z-axis.
            Default is None.

    Returns:
        The moved mesh.
    """
    return mesh.apply_translation(_get_to_bound_offsets(mesh, x, y, z))


@contextmanager
def moved_to_center(mesh: trimesh.Trimesh):
    """Context manager that moves the mesh to the center of its bounding box.

    The mesh is moved back to its original position after the context is exited.

    Args:
        mesh: The mesh to be moved.

    Yields:
        None
    """
    center = mesh.centroid
    try:
        to_center = trimesh.transformations.translation_matrix(-center)
        mesh = mesh.apply_transform(to_center)
        yield
    finally:
        back_to_origin = trimesh.transformations.translation_matrix(center)
        mesh.apply_transform(back_to_origin)


@contextmanager
def moved_to_floor(mesh: trimesh.Trimesh, offset: float = 0):
    """Context manager that moves the mesh to the floor of its bounding box.

    The mesh is moved back to its original position after the context is exited.

    Args:
        mesh: The mesh to be moved.
        offset: The distance to move the mesh below the floor. Default is 0.

    Yields:
        None
    """
    floor = _get_to_floor_offsets(mesh, offset)
    try:
        to_floor = trimesh.transformations.translation_matrix([0, 0, floor])
        mesh = mesh.apply_transform(to_floor)
        yield
    finally:
        back_to_origin = trimesh.transformations.translation_matrix([0, 0, -floor])
        mesh.apply_transform(back_to_origin)


@contextmanager
def moved_to_bound(
    mesh: trimesh.Trimesh,
    x: Union[float, None] = None,
    y: Union[float, None] = None,
    z: Union[float, None] = None,
):
    """Context manager that moves the mesh to the specified boundary.

    The mesh is moved back to its original position after the context is exited.

    Args:
        mesh: The mesh to be moved.
        x: The distance to move the mesh along the x-axis. If None, the mesh is not moved along the x-axis.
            Default is None.
        y: The distance to move the mesh along the y-axis. If None, the mesh is not moved along the y-axis.
            Default is None.
        z: The distance to move the mesh along the z-axis. If None, the mesh is not moved along the z-axis.
            Default is None.

    Yields:
        None
    """
    bound = _get_to_bound_offsets(mesh, x, y, z)
    try:
        to_bound = trimesh.transformations.translation_matrix(bound)
        mesh = mesh.apply_transform(to_bound)
        yield
    finally:
        back_to_origin = trimesh.transformations.translation_matrix(-bound)
        mesh.apply_transform(back_to_origin)


def _get_to_bound_offsets(
    mesh: trimesh.Trimesh,
    x: Union[float, None] = None,
    y: Union[float, None] = None,
    z: Union[float, None] = None,
) -> np.ndarray:
    """Get the offset to move the mesh to the specified boundary.

    Args:
        mesh: The mesh to be moved.
        x: The distance to move the mesh along the x-axis. If None, the mesh is not moved along the x-axis.
            Default is None.
        y: The distance to move the mesh along the y-axis. If None, the mesh is not moved along the y-axis.
            Default is None.
        z: The distance to move the mesh along the z-axis. If None, the mesh is not moved along the z-axis.
            Default is None.

    Returns:
        The offset to move the mesh to the specified boundary.
    """
    def get_offset(direction: Union[float, None], axis_index: int = 0) -> float:
        if direction is None:
            return 0

        middle = (mesh.bounds[:, axis_index][1] + mesh.bounds[:, axis_index][0])/2
        half_size = (mesh.bounds[:, axis_index][1] - mesh.bounds[:, axis_index][0])/2

        return -middle + half_size*direction

    return np.array([get_offset(x, 0), get_offset(y, 1), get_offset(z, 2)])


def _get_to_floor_offsets(mesh: trimesh.Trimesh, offset: float) -> np.ndarray:
    """Get the offset to move the mesh to the floor of its bounding box.

    Args:
        mesh: The mesh to be moved.
        offset: The distance to move the mesh below the floor.

    Returns:
        The offset to move the mesh to the floor of its bounding box.
    """
    return np.array([0, 0, -mesh.bounds[:, 2][0] + offset])
