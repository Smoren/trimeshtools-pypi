import trimesh


def union_meshes(*meshes: trimesh.Trimesh) -> trimesh.Trimesh:
    """Perform a boolean union operation on a collection of meshes.

    Args:
        meshes: The meshes to be combined.

    Returns:
        The combined mesh.
    """
    assert len(meshes) > 0
    result = meshes[0]
    for mesh in meshes[1:]:
        result = result.union(mesh)
    return result


def concatenate_meshes(*meshes: trimesh.Trimesh) -> trimesh.Trimesh:
    """Concatenate a collection of meshes along their common axis.

    Args:
        meshes: The meshes to be concatenated.

    Returns:
        The concatenated mesh.
    """
    assert len(meshes) > 0
    result = meshes[0]
    for mesh in meshes[1:]:
        result = trimesh.util.concatenate(result, mesh)
    return result
