from typing import Callable, List, Tuple, Union

import trimesh
import numpy as np
from scipy.spatial import Delaunay

from trimeshtools.utils import fix_all


class Surface(trimesh.Trimesh):
    """
    Surface class that represents a mesh with triangular faces.
    Extends the Trimesh class from the Trimesh library.
    """
    def __init__(self, *args, **kwargs):
        """Initializes a new instance of the Surface class.

        Args:
            *args: Variable length argument list that is passed to the parent class (Trimesh).
            **kwargs: Arbitrary keyword arguments that are passed to the parent class (Trimesh).
        """
        super().__init__(*args, **kwargs)
        self.fix_all()

    @classmethod
    def from_vertices(cls, vertices: np.ndarray) -> "Surface":
        """Initializes a new instance of the Surface class from vertices.

        Args:
            vertices: Array of shape (N, 3) representing the vertices of the mesh.

        Returns:
            A Surface object representing the mesh.

        Raises:
            ValueError: If the input is not a numpy array of shape (N, 3).
        """
        if not isinstance(vertices, np.ndarray) or vertices.shape[1] != 3:
            raise ValueError("Input must be a numpy array of shape (N, 3)")

        # Delaunay triangulation (works in 2D or 3D, but for 3D points it returns a concave hull)
        tri = Delaunay(vertices[:, :2])  # Project onto 2D for triangulation (if points are not in a plane, possible artifacts)

        # Get faces (indices of triangle vertices)
        faces = tri.simplices

        return cls(vertices=vertices, faces=faces)

    @classmethod
    def from_paths(cls, paths: np.ndarray) -> "Surface":
        """Initializes a new instance of the Surface class from paths.

        Args:
            paths: Array of shape (M, N, 3) representing the paths of the mesh.

        Returns:
            A Surface object representing the mesh.

        Raises:
            AssertionError: If the input is not a numpy array of shape (M, N, 3).
        """
        assert len(paths.shape) == 3
        assert paths.shape[0] > 1
        assert paths.shape[1] > 0
        assert paths.shape[2] == 3

        X, Y, Z = np.empty(0), np.empty(0), np.empty(0)

        for i in range(paths.shape[0]):
            x, y, z = paths[i, :, 0], paths[i, :, 1], paths[i, :, 2]
            X = np.concatenate((X, x))
            Y = np.concatenate((Y, y))
            Z = np.concatenate((Z, z))

        N = paths.shape[1]
        M = paths.shape[0]

        vertices = np.vstack((X, Y, Z)).T

        faces = []
        for i in range(M - 1):
            for j in range(N - 1):
                faces.append([i * N + j, i * N + (j + 1), (i + 1) * N + (j + 1)])
                faces.append([i * N + j, (i + 1) * N + (j + 1), (i + 1) * N + j])

        faces = np.array(faces)

        return Surface(vertices=vertices, faces=faces)

    @classmethod
    def from_z_function(
        cls,
        function: Callable[[np.ndarray, np.ndarray], np.ndarray],
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        steps_count: int,
        vertices_mask_function: Union[Callable[[np.ndarray], np.ndarray], None] = None,
    ) -> "Surface":
        """
        Initializes a new instance of the Surface class from a z-function.

        Args:
            function : A function that takes two arrays X and Y and returns an array Z.
            x_range: A tuple of two floats representing the range of X values.
            y_range: A tuple of two floats representing the range of Y values.
            steps_count: An integer representing the number of steps to take in each direction.
            vertices_mask_function: A function that takes an array of vertices and returns a boolean mask indicating which vertices should be included. Defaults to None.

        Returns:
            A Surface object representing the mesh.
        """
        # Generate points on the XY plane
        x = np.linspace(*x_range, steps_count)
        y = np.linspace(*y_range, steps_count)
        X, Y = np.meshgrid(x, y)
        Z = function(X, Y)
        N = steps_count

        # Convert to array of vertices
        vertices = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T

        if vertices_mask_function is not None:
            return cls.from_vertices(vertices[vertices_mask_function(vertices)])

        # Check for NaN or infinite values in Z
        nan_mask = np.isnan(vertices[:, 2])
        inf_mask = np.isinf(vertices[:, 2])
        if nan_mask.any() or inf_mask.any():
            return cls.from_vertices(vertices[~nan_mask & ~inf_mask])

        # Build faces
        faces = []
        for i in range(N - 1):
            for j in range(N - 1):
                faces.append([i * N + j, i * N + (j + 1), (i + 1) * N + (j + 1)])
                faces.append([i * N + j, (i + 1) * N + (j + 1), (i + 1) * N + j])

        faces = np.array(faces)

        return Surface(vertices=vertices, faces=faces)

    @classmethod
    def from_parametric_path_functions(
        cls,
        functions: List[Callable[[np.ndarray], Tuple[np.ndarray, np.ndarray, np.ndarray]]],
        parameter_values: np.ndarray,
    ) -> "Surface":
        """Initializes a new instance of the Surface class from parametric path functions.

        Args:
            functions: A list of functions that take a parameter value and return a tuple of arrays representing the path.
            parameter_values: An array of parameter values.

        Returns:
            A Surface object representing the mesh.
        """
        assert len(functions) > 1

        T = parameter_values
        paths = []

        for path_function in functions:
            paths.append(np.array([*path_function(T)]).T)

        paths = np.array(paths)

        return cls(paths)

    def thicken(self, thickness: float) -> trimesh.Trimesh:
        """Thickens the surface by the given thickness.

        Args:
            thickness: The thickness to apply.

        Returns:
            A Trimesh object representing the thickened mesh.
        """
        n_vertices = len(self.vertices)

        if not hasattr(self, 'vertex_normals'):
            self.fix_normals()

        # Create offset vertices and faces
        inflated_vertices = self.vertices + thickness * getattr(self, 'vertex_normals')
        inflated_faces = self.faces[:, ::-1] + n_vertices  # Reverse vertex order for correct normals

        # Find boundary edges (only those that belong to one face)
        boundary_edges = trimesh.grouping.group_rows(self.edges_sorted, require_count=1)

        # Build side surfaces (quads and triangulation)
        side_faces = []
        for edge in self.edges[boundary_edges]:
            v0, v1 = edge
            v0_offset = v0 + n_vertices
            v1_offset = v1 + n_vertices

            # Add two triangles for each boundary edge
            side_faces.append([v0, v1, v1_offset])
            side_faces.append([v0, v1_offset, v0_offset])

        # Combine all components
        all_vertices = np.vstack((self.vertices, inflated_vertices))
        all_faces = np.vstack((
            self.faces,
            inflated_faces,
            np.array(side_faces)
        ))

        # Create the final mesh
        final_mesh = trimesh.Trimesh(vertices=all_vertices, faces=all_faces)

        # Optimize and check
        fix_all(final_mesh)

        return final_mesh

    def fix_all(self) -> None:
        """Fixes all the mesh issues."""
        fix_all(self)
