from typing import List, Tuple

import numpy as np
import trimesh


def subdivide_shape(mesh: trimesh.Trimesh, iterations: int) -> trimesh.Trimesh:
    """Subdivides a mesh by the given number of iterations.

    Args:
        mesh: The mesh to be subdivided.
        iterations: The number of iterations to subdivide the mesh.

    Returns:
        The subdivided mesh.
    """
    for i in range(iterations):
        mesh = mesh.subdivide()
    return mesh


def cut_mesh(mesh: trimesh.Trimesh, plane_origin: List[float], plane_normal: List[float]) -> Tuple[trimesh.Trimesh, trimesh.Trimesh]:
    """Cuts a mesh by the given plane.

    Args:
        mesh: The mesh to be cut.
        plane_origin: The origin of the plane.
        plane_normal: The normal of the plane.

    Returns:
        The positive and negative parts of the mesh.
    """
    # Use slice_plane for positive part of the normal
    mesh_above = mesh.slice_plane(plane_origin=np.array(plane_origin), plane_normal=np.array(plane_normal), cap=True)

    # Invert the normal and repeat to get the negative part of the mesh
    mesh_below = mesh.slice_plane(plane_origin=np.array(plane_origin), plane_normal=-np.array(plane_normal), cap=True)

    return mesh_above, mesh_below
