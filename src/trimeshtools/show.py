import numpy as np
import trimesh

from trimeshtools.axis import create_axis_mesh
from trimeshtools.combine import concatenate_meshes


def show_mesh(mesh: trimesh.Trimesh, with_axis: bool = True) -> None:
    """Show a mesh in a 3D viewer.

    Args:
        mesh: The mesh to be shown.
        with_axis: Whether to show the axis. Defaults to True.
    """
    if with_axis:
        mesh = concatenate_meshes(mesh, create_axis_mesh(size=np.max(mesh.bounds[1] - mesh.bounds[0])*1.1))
    scene = mesh.scene()
    scene.show()
