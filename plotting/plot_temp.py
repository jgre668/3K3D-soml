import numpy as np
import matplotlib.pyplot as plt

def plot_temp(data_file, dn = 10):

    def read_binary_3K3D(filepath):
        with open(filepath, 'rb') as f:
            nt = np.frombuffer(f.read(4), dtype=np.int32).item()
            nx = np.frombuffer(f.read(4), dtype=np.int32).item()
            ny = np.frombuffer(f.read(4), dtype=np.int32).item()
            nz = np.frombuffer(f.read(4), dtype=np.int32).item()

            total_values = nt * nx * ny * nz
            data = np.frombuffer(f.read(total_values * 8), dtype=np.float64)
            array = data.reshape((nt, nx, ny, nz))

        return nt, nx, ny, nz, array

    nt, nx, ny, nz, u = read_binary_3K3D(data_file)

    z_slice = nz // 2  # Middle of z-axis
    y_slice = ny // 2  # Middle of y-axis for line plot

    # compute global min and max for consistent color scaling
    global_min = np.min(u[:, :, :, z_slice])
    global_max = np.max(u[:, :, :, z_slice])

    # compute global min and max for consistent line plot y-axis
    line_global_min = np.min(u[:, :, y_slice, z_slice])
    line_global_max = np.max(u[:, :, y_slice, z_slice])

    for t in np.arange(0, nt, dn):
        fig, axs = plt.subplots(2, 1, figsize=(6, 8))

        # heatmap of the 2D slice
        im = axs[0].imshow(u[t, :, :, z_slice], cmap='viridis', vmin=global_min, vmax=global_max)
        axs[0].set_title(f'u[t={t}, z={z_slice}]')
        fig.colorbar(im, ax=axs[0])

        # line plot through the middle y slice of that 2D plane
        line_data = u[t, :, y_slice, z_slice]
        axs[1].plot(np.arange(nx), line_data)
        axs[1].set_ylim(1.1 * line_global_min, 1.1 * line_global_max)
        axs[1].set_xlim(0, nx - 1)
        axs[1].set_title(f'u[t={t}, y={y_slice}, z={z_slice}]')
        axs[1].set_xlabel('x')
        axs[1].set_ylabel('u value')

        plt.tight_layout()
        plt.show()

plot_temp("/home/jgre668/3K3D-soml/outputs/SOML25tCc/binary/3K2D_u.bin", 1)
plot_temp("/home/jgre668/3K3D-soml/outputs/SOML25tCc/binary/3K2D_v.bin", 1)
plot_temp("/home/jgre668/3K3D-soml/outputs/SOML25tCc/binary/3K2D_w.bin", 1)


