import trimesh


def fix_all(mesh: trimesh.Trimesh, max_iter: int = 10) -> None:
    """Repair the mesh by merging vertices, removing duplicate faces,
    removing degenerate faces, and fixing normals.

    Args:
        mesh: The mesh to be repaired.
        max_iter: The maximum number of iterations to repair the mesh. Default is 10.

    Returns:
        None
    """
    for i in range(max_iter):
        mesh.merge_vertices()
        mesh.update_faces(mesh.nondegenerate_faces())
        mesh.update_faces(mesh.unique_faces())
        mesh.fix_normals()

        if mesh.is_volume and mesh.is_watertight:
            return
