import numpy as np
import trimesh


def bend_mesh(mesh: trimesh.Trimesh, radius: float) -> trimesh.Trimesh:
    """Bends the mesh around the Y axis, changing vertex positions.

    Args:
        mesh: A mesh to deform.
        radius: Radius of the cylinder to bend the mesh around.

    Returns:
        A deformed mesh.
    """
    # Vertices of the original shape
    vertices = mesh.vertices

    # Bend the shape around the Y axis
    # Convert X coordinates to angular position on a cylinder
    new_vertices = []
    for x, y, z in vertices:
        theta = x / radius  # Angular offset
        new_x = radius * np.sin(theta)  # Radial position on a cylinder
        new_z = radius * (1 - np.cos(theta)) + z  # Keep vertical offset along Z
        new_vertices.append([new_x, y, new_z])

    # Update vertex coordinates
    mesh.vertices = np.array(new_vertices)

    return mesh


def spiral_bend_mesh(mesh: trimesh.Trimesh, bend_amount: float) -> trimesh.Trimesh:
    """Bends the mesh around the Y axis, changing vertex positions.

    Args:
        mesh: A mesh to deform.
        bend_amount: Amount of bend in radians.

    Returns:
        A deformed mesh.
    """
    # Get vertex positions
    vertices = mesh.vertices.copy()

    # Calculate the minimum and maximum Y values
    y_min = vertices[:, 1].min()
    y_max = vertices[:, 1].max()
    y_range = y_max - y_min

    # Calculate bending angle for each vertex based on its Y coordinate
    # bend_amount - maximum bending angle in radians
    theta = bend_amount * ((vertices[:, 1] - y_min) / y_range)

    # Apply twisting transformation
    x_new = vertices[:, 0] * np.cos(theta) + vertices[:, 2] * np.sin(theta)
    z_new = -vertices[:, 0] * np.sin(theta) + vertices[:, 2] * np.cos(theta)
    vertices[:, 0] = x_new
    vertices[:, 2] = z_new

    # Update mesh vertices
    mesh.vertices = vertices

    return mesh


def twist_mesh(mesh: trimesh.Trimesh, num_rotations: int = 5):
    """Twists the mesh around the Y axis, changing vertex positions.

    Parameters:
        mesh: A mesh to deform.
        num_rotations: Number of full rotations to perform. Default is 5.

    Returns:
        A deformed mesh.
    """
    # Retrieve mesh vertices
    vertices = mesh.vertices

    # Maximum height
    max_y = vertices[:, 1].max()

    # Transform vertices
    for i, vertex in enumerate(vertices):
        # Normalize vertex height (from 0 to 1)
        height_factor = vertex[1] / max_y

        # Determine the rotation angle for the current vertex
        angle = height_factor * num_rotations * 2 * np.pi

        # Calculate new coordinates for spiral rotation
        x = vertex[0] * np.cos(angle) - vertex[2] * np.sin(angle)
        z = vertex[0] * np.sin(angle) + vertex[2] * np.cos(angle)

        # Update vertex (X and Z changed, Y remains unchanged)
        vertices[i] = [x, vertex[1], z]

    # Update mesh vertices
    mesh.vertices = vertices
    return mesh
