import numpy as np
import matplotlib.pyplot as plt
from parameters import *

cmap = params['cmap']

"""
plotting code that takes a snapshot and 'scans' through it, plotting at certain slices
and also plotting the projection of maximum displacement

"""

def read_snapshot(filename):
    with open(filename, "rb") as f:
        # read header
        header = np.frombuffer(f.read(16), dtype=np.int32)
        t_idx, nx, ny, nz = header

        print(f"time index: {t_idx}, shape: ({nx}, {ny}, {nz})")

        # read the flat data
        data = np.frombuffer(f.read(), dtype=np.float64)
        expected_size = nx * ny * nz
        if data.size != expected_size:
            raise ValueError(f"expected {expected_size} elements, got {data.size}")

        # reshape to (nx, ny, nz)
        array = data.reshape((nx, ny, nz))

    return t_idx, nx, ny, nz, array


def plot_slices(array, t_idx, component ="u", z_slice_fraction = 0.5, cmap = cmap):
    """
    plot a 1x2 grid with:
    - left: max projection along z
    - right: slice through z at a given fraction
    both plots use the same color scale
    """
    nx, ny, nz = array.shape
    z_index = int(nz * z_slice_fraction)
    z_index = max(0, min(nz - 1, z_index))

    # compute global min and max for consistent color scale
    vmin = np.min(array)
    vmax = np.max(array)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # left: max projection along z
    projection = np.max(array, axis=2)
    im0 = axs[0].imshow(projection.T, origin="lower", aspect="equal",
                        cmap=cmap, vmin=vmin, vmax=vmax)
    axs[0].set_title(f"max projection of ${component}$ (z-axis) at $t_{{idx}}$ = {t_idx}")
    axs[0].set_xlabel("$x$")
    axs[0].set_ylabel("$y$")
    fig.colorbar(im0, ax=axs[0], shrink=0.8)

    # right: slice through z
    slice_z = array[:, :, z_index]
    im1 = axs[1].imshow(slice_z.T, origin="lower", aspect="equal",
                        cmap=cmap, vmin=vmin, vmax=vmax)
    axs[1].set_title(f"z-slice of ${component}$ at {z_index}/{nz}, $t_{{idx}}$ = {t_idx}")
    axs[1].set_xlabel("$x$")
    axs[1].set_ylabel("$y$")
    fig.colorbar(im1, ax=axs[1], shrink=0.8)

    plt.tight_layout()
    plt.show()


def save_csv(array, filename, spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0), field_name="u", step=4):
    """
    Save a downsampled 3D numpy array to CSV as (x, y, z, value) format.
    Only writes every `step`th point in each dimension.
    """
    nx, ny, nz = array.shape
    dx, dy, dz = spacing
    ox, oy, oz = origin

    with open(filename, "w") as f:
        f.write("x,y,z," + field_name + "\n")
        for i in range(0, nx, step):
            for j in range(0, ny, step):
                for k in range(0, nz, step):
                    x = ox + i * dx
                    y = oy + j * dy
                    z = oz + k * dz
                    value = array[i, j, k]
                    f.write(f"{x},{y},{z},{value}\n")
    print(f"Saved downsampled CSV to {filename} (step={step})")

if __name__ == "__main__":

    filename = "/home/jgre668/3K3D-solver/binaries/3K3D/u_t00000.bin"

    t_idx, nx, ny, nz, data = read_snapshot(filename)

    for z_slice_fraction in np.arange(0.3, 0.6, 0.1):
        plot_slices(data, t_idx = t_idx,
                    component = "u",
                    z_slice_fraction = z_slice_fraction)

    # SAVE TO VTK FOR PARAVIEW
    # save_csv(data, f"temperature_t{t_idx:05d}.csv", field_name="u")