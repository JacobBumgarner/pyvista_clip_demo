from math import sqrt, pi
import numpy as np
import pyvista as pv
from pyvista import examples
from scipy.ndimage import uniform_filter

def load_tube():
    theta = np.linspace(-4*np.pi, 4*np.pi, 100, endpoint=True)
    x = np.cos(theta)
    y = np.sin(theta)
    z = np.linspace(0, 8, 100, endpoint=True)
    tube_coords = np.vstack([x, y, z]).T
    tube_coords += np.abs(tube_coords.min())
    
    # Example tube radius variation
    r = np.log10(np.linspace(2, 10, 50)) / 2
    tube_radius = np.append(r, np.flip(r))
    radius_factor = np.max(tube_radius) / np.min(tube_radius)

    # Create tube
    spline = pv.Spline(tube_coords)
    spline['radius'] = tube_radius
    tube = spline.tube(radius=np.min(tube_radius), scalars='radius',
                    radius_factor=radius_factor)
    return tube

def load_grid():
    points_outer = np.random.normal(0, 20, 10000).reshape(100, 100, 1)
    points_outer[points_outer < 5] = 0
    points_inner = np.random.normal(0, 50, 10000).reshape(100, 100, 1)
    points_inner[points_inner < 15] = 0
    points_inner *= np.pad(np.ones((40, 40, 1)), ((30, 30), (30, 30), (0,0)))
    points = points_outer + points_inner
    points = uniform_filter(points, size=3)

    grid = pv.UniformGrid(dims=points.shape)
    grid['elevation'] = points.ravel()

    grid = grid.warp_by_scalar('elevation')    
    
    return grid

def load_foot():
    foot = examples.download_foot_bones()
    return foot

def load_brain():
    gears = examples.download_brain()
    return gears

def load_st_helens():
    helens = examples.download_st_helens().warp_by_scalar()
    return helens

def load_Laurent_lattice():

    T = 1
    G = -1


    def f(ρ, θ, ϕ):
        x = ρ * np.cos(θ) * np.sin(ϕ)
        y = ρ * np.sin(θ) * np.sin(ϕ)
        z = ρ * np.cos(ϕ)
        sin_x = np.sin(x)
        sin_y = np.sin(y)
        sin_z = np.sin(z)
        cos_x = np.cos(x)
        cos_y = np.cos(y)
        cos_z = np.cos(z)
        return (
            (
                np.cos(
                    x
                    - (-sin_x * sin_y + cos_x * cos_z)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    y
                    - (-sin_y * sin_z + cos_y * cos_x)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                + np.cos(
                    y
                    - (-sin_y * sin_z + cos_y * cos_x)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    z
                    - (-sin_z * sin_x + cos_z * cos_y)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                + np.cos(
                    z
                    - (-sin_z * sin_x + cos_z * cos_y)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    x
                    - (-sin_x * sin_y + cos_x * cos_z)
                    * T
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
            )
        ) * (
            (
                np.cos(
                    x
                    - (-sin_x * sin_y + cos_x * cos_z)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    y
                    - (-sin_y * sin_z + cos_y * cos_x)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                + np.cos(
                    y
                    - (-sin_y * sin_z + cos_y * cos_x)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    z
                    - (-sin_z * sin_x + cos_z * cos_y)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                + np.cos(
                    z
                    - (-sin_z * sin_x + cos_z * cos_y)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
                * np.sin(
                    x
                    - (-sin_x * sin_y + cos_x * cos_z)
                    * G
                    / np.sqrt(
                        (-sin_x * sin_y + cos_x * cos_z) ** 2
                        + (-sin_y * sin_z + cos_y * cos_x) ** 2
                        + (-sin_z * sin_x + cos_z * cos_y) ** 2
                    )
                )
            )
        )


    def sph2cart(sph):
        ρ = sph[:, 0]
        θ = sph[:, 1]
        ϕ = sph[:, 2]
        return np.array([
            ρ * np.cos(θ) * np.sin(ϕ),
            ρ * np.sin(θ) * np.sin(ϕ),
            ρ * np.cos(ϕ)
        ])


    # generate data grid for computing the values
    Rho, Theta, Phi = np.mgrid[0:8:200j, 0:(pi):200j, 0 : (2 * pi) : 200j]
    # create a structured grid
    grid = pv.StructuredGrid(Rho, Theta, Phi)
    # grid.points = np.transpose(sph2cart(grid.points))


    values = f(Rho, Theta, Phi)
    grid.point_data["values"] = values.ravel(order="F")
    # compute one isosurface
    isosurf = grid.contour(isosurfaces=[0])
    mesh = isosurf.extract_geometry()
    mesh.points = np.transpose(sph2cart(mesh.points))
    mesh.point_data["distance"] = np.linalg.norm(mesh.points, axis=1)
    return mesh