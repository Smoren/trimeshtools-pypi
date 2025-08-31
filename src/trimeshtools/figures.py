import numpy as np
import shapely
import trimesh

from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x


def create_archimedean_spiral_mesh(
    shape_polygon_path: np.ndarray,
    start_radius: float,
    distance_factor: float,
    num_turns: float,
    num_points: int,
) -> trimesh.Trimesh:
    """Creates a mesh object representing an Archimedean spiral trajectory within a given shape polygon.

    Args:
        shape_polygon_path: The coordinates of the shape's polygon.
        start_radius: The radius of the spiral at the start of the trajectory.
        distance_factor: The factor by which the radius increases with each turn of the spiral.
        num_turns: The number of turns of the spiral.
        num_points: The number of points in the spiral trajectory.

    Returns:
        A mesh object representing the Archimedean spiral trajectory.
    """
    # Define the shape polygon
    shape = shapely.geometry.Polygon(shape_polygon_path*2.2)

    # Generate theta values
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)

    # Calculate radii
    r = start_radius + distance_factor * theta

    # Calculate x, y coordinates for the spiral trajectory
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(theta)  # Spiral in the XY plane

    # Create the spiral trajectory as a sequence of points
    path = np.column_stack((x, y, z))

    # Extrude the cross-section along the spiral trajectory
    spiral_mesh = trimesh.creation.sweep_polygon(shape, path)

    return spiral_mesh


def create_rounded_box_mesh(
    width: float, height: float,
    thickness: float,
    top_round: float = 0,
    bottom_round: float = 0,
    sections: int = 100,
) -> trimesh.Trimesh:
    """Creates a rounded box mesh.

    Args:
        width: The width of the box.
        height: The height of the box.
        thickness: The thickness of the box.
        top_round: The amount of rounding at the top. Defaults to 0.
        bottom_round: The amount of rounding at the bottom. Defaults to 0.
        sections: The number of sections for the cylinder. Defaults to 100.

    Returns:
        The rounded box mesh.
    """
    top_radius = width * top_round / 2
    bottom_radius = width * bottom_round / 2

    final = trimesh.creation.box(extents=[width, thickness, height - top_radius - bottom_radius])

    if top_round > 0:
        top_cylinder = trimesh.creation.cylinder(radius=top_radius, height=thickness, sections=sections)
        top_cylinder = top_cylinder.apply_transform(create_rotation_matrix_for_x(np.radians(90)))

        final = move_to_bound(final, x=-1, y=0, z=-1)
        top_cylinder = move_to_bound(top_cylinder, x=-1, y=0, z=0)
        final = final.union(top_cylinder)

        final = move_to_bound(final, x=1, y=0)
        top_cylinder = move_to_bound(top_cylinder, x=1, y=0, z=0)
        final = final.union(top_cylinder)

        if top_round != 1.0:
            final = move_to_bound(final, x=0, y=0)
            top_middle = trimesh.creation.box(extents=[width - top_radius*2, thickness, top_radius])
            top_middle = move_to_bound(top_middle, x=0, y=0, z=1)
            final = final.union(top_middle)

    if bottom_round > 0:
        bottom_cylinder = trimesh.creation.cylinder(radius=bottom_radius, height=thickness, sections=sections)
        bottom_cylinder = bottom_cylinder.apply_transform(create_rotation_matrix_for_x(np.radians(90)))

        final = move_to_bound(final, x=-1, y=0, z=1)
        bottom_cylinder = move_to_bound(bottom_cylinder, x=-1, y=0, z=0)
        final = final.union(bottom_cylinder)

        final = move_to_bound(final, x=1, y=0)
        bottom_cylinder = move_to_bound(bottom_cylinder, x=1, y=0, z=0)
        final = final.union(bottom_cylinder)

        if bottom_round != 1.0:
            final = move_to_bound(final, x=0, y=0)
            bottom_middle = trimesh.creation.box(extents=[width - bottom_radius * 2, thickness, bottom_radius])
            bottom_middle = move_to_bound(bottom_middle, x=0, y=0, z=-1)
            final = final.union(bottom_middle)

    final = move_to_bound(final, x=0, y=0, z=0)

    return final
