# TrimeshTools - collection of tools for 3D modeling with Trimesh

[![PyPI package](https://img.shields.io/badge/pip%20install-trimeshtools-brightgreen)](https://pypi.org/project/trimeshtools/)
[![version number](https://img.shields.io/pypi/v/trimeshtools?color=green&label=version)](https://github.com/Smoren/trimeshtools-pypi/releases)
[![PyPI Downloads](https://static.pepy.tech/badge/trimeshtools)](https://pepy.tech/projects/trimeshtools)
[![Actions Status](https://github.com/Smoren/trimeshtools-pypi/workflows/Test/badge.svg)](https://github.com/Smoren/trimeshtools-pypi/actions)
[![License](https://img.shields.io/github/license/Smoren/trimeshtools-pypi)](https://github.com/Smoren/trimeshtools-pypi/blob/master/LICENSE)

## Overview

`trimeshtools-pypi` is a minimalistic Python library designed to extend the capabilities of the popular `trimesh` library. 
It provides a limited set of tools for basic 3D mesh manipulation, including operations for combining, moving, rotating, 
and visualizing 3D models. This library aims to simplify common mesh processing tasks, making it easier for developers 
and researchers to work with 3D data in Python.

## Key Features

* **Mesh Combination**: Seamlessly perform boolean union operations and concatenate multiple meshes.
* **Advanced Deformation**: Apply various deformation techniques such as bending, spiral bending, and twisting to meshes.
* **Precise Editing**: Subdivide meshes for increased detail and accurately cut meshes using defined planes.
* **Transformations**: Easily move meshes to specific positions (center, floor, custom bounds) and apply rotations or mirroring transformations.
* **Geometric Figure Creation**: Generate complex 3D shapes like Archimedean spirals and rounded boxes.
* **Surface Operations**: Utilize the `Surface` class for advanced operations, including creating surfaces from vertices, paths, Z-functions, and parametric functions, as well as thickening surfaces.
* **Visualization**: Conveniently display meshes in a 3D viewer, with optional axis visualization.
* **Mesh Repair Utilities**: Includes functions to fix common mesh issues such as merging vertices, removing duplicate faces, and correcting normals.

## Installation

To install `trimeshtools-pypi`, you can use pip:
```bash
pip install trimeshtools-pypi
```

## Usage

Here are some basic examples of how to use `trimeshtools-pypi`.

### Combining Meshes

```python
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes

# Create some sample meshes
mesh1 = trimesh.creation.box()
mesh2 = trimesh.creation.sphere()

# Perform a union operation
combined_mesh_union = union_meshes(mesh1, mesh2)

# Concatenate meshes
combined_mesh_concat = concatenate_meshes(mesh1, mesh2)
```

### Deforming Meshes

```python
import trimesh
from trimeshtools.deform import bend_mesh, spiral_bend_mesh, twist_mesh

# Create a sample mesh
mesh = trimesh.creation.box()

# Bend the mesh
bent_mesh = bend_mesh(mesh.copy(), radius=10)

# Spiral bend the mesh
spiral_bent_mesh = spiral_bend_mesh(mesh.copy(), bend_amount=0.5)

# Twist the mesh
twisted_mesh = twist_mesh(mesh.copy(), num_rotations=3)
```

### Editing Meshes

```python
import trimesh
from trimeshtools.edit import subdivide_shape, cut_mesh
import numpy as np

# Create a sample mesh
mesh = trimesh.creation.box()

# Subdivide the mesh
subdivided_mesh = subdivide_shape(mesh.copy(), iterations=1)

# Cut the mesh
plane_origin = [0, 0, 0]
plane_normal = [0, 0, 1]
mesh_above, mesh_below = cut_mesh(mesh.copy(), plane_origin, plane_normal)
```

### Moving Meshes

```python
import trimesh
from trimeshtools.move import move_to_center, move_to_floor, move_to_bound

# Create a sample mesh
mesh = trimesh.creation.box()

# Move to center
centered_mesh = move_to_center(mesh.copy())

# Move to floor
floored_mesh = move_to_floor(mesh.copy())

# Move to specific bound
bound_mesh = move_to_bound(mesh.copy(), x=1, y=-1, z=0)
```

### Rotating Meshes

```python
import trimesh
from trimeshtools.rotate import create_rotation_matrix_for_x, create_mirror_matrix
import numpy as np

# Create a sample mesh
mesh = trimesh.creation.box()

# Create rotation matrix and apply
rotation_matrix = create_rotation_matrix_for_x(np.radians(45))
rotated_mesh = mesh.copy().apply_transform(rotation_matrix)

# Create mirror matrix and apply
mirror_matrix = create_mirror_matrix(x=True)
mirrored_mesh = mesh.copy().apply_transform(mirror_matrix)
```

### Showing Meshes

```python
import trimesh
from trimeshtools.show import show_mesh

# Create a sample mesh
mesh = trimesh.creation.box()

# Show the mesh
show_mesh(mesh)
```

### Surface Operations

```python
import trimesh
import numpy as np
from trimeshtools.surface import Surface

# Create a surface from vertices
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [1, 1, 0]
])
surface_from_vertices = Surface.from_vertices(vertices)

# Create a surface from a z-function
def custom_z_function(X, Y):
    return np.sin(X) + np.cos(Y)

surface_from_function = Surface.from_z_function(
    custom_z_function, x_range=(0, 2*np.pi), y_range=(0, 2*np.pi), steps_count=50
)

# Thicken a surface
thickened_surface = surface_from_vertices.thicken(0.1)
```

## Dependencies

`trimeshtools-pypi` relies on the following core libraries:

* `trimesh`: A powerful Python library for 3D meshes and geometry.
* `numpy`: The fundamental package for scientific computing with Python.
* `scipy`: Scientific computing tools for Python, used for Delaunay triangulation in surface creation.
* `shapely`: A Python library for manipulation and analysis of planar geometric objects, used for creating spiral meshes.

These dependencies will be automatically installed when you install `trimeshtools-pypi` using pip.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
