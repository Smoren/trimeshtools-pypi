import numpy as np


def create_rotation_matrix_for_x(angle: float) -> np.ndarray:
    """Create a rotation matrix for rotation around the X axis.

    Args:
        angle (float): The angle of rotation in radians.

    Returns:
        np.ndarray: The rotation matrix.
    """
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1],
    ])


def create_rotation_matrix_for_y(angle: float) -> np.ndarray:
    """Create a rotation matrix for rotation around the Y axis.

    Args:
        angle (float): The angle of rotation in radians.

    Returns:
        np.ndarray: The rotation matrix.
    """
    return np.array([
        [np.cos(angle), 0, -np.sin(angle), 0],
        [0, 1, 0, 0],
        [np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1],
    ])


def create_rotation_matrix_for_z(angle: float) -> np.ndarray:
    """Create a rotation matrix for rotation around the Z axis.

    Args:
        angle: The angle of rotation in radians.

    Returns:
        The rotation matrix.
    """
    return np.array([
        [np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def create_mirror_matrix(x: bool = False, y: bool = False, z: bool = False) -> np.ndarray:
    """Create a mirror matrix for mirroring around the X, Y, or Z axis.

    Args:
        x: Whether to mirror around the X axis. Defaults to False.
        y: Whether to mirror around the Y axis. Defaults to False.
        z: Whether to mirror around the Z axis. Defaults to False.

    Returns:
        The mirror matrix.
    """
    x_sign = -1 if x else 1
    y_sign = -1 if y else 1
    z_sign = -1 if z else 1
    return np.array([
        [x_sign, 0, 0, 0],
        [0, y_sign, 0, 0],
        [0, 0, z_sign, 0],
        [0, 0, 0, 1]
    ])
