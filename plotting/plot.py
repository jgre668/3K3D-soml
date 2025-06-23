import numpy as np
import matplotlib.pyplot as plt

def plot(u_data_path, v_data_path, dn=10):

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

    # load both u and v
    nt, nx, ny, nz, u = read_binary_3K3D(u_data_path)
    _, _, _, _, v = read_binary_3K3D(v_data_path)

    z_slice = nz // 2  # Middle of z-axis
    y_slice = ny // 2  # Middle of y-axis for line plot

    # consistent color scaling for the heatmap
    global_min = np.min(u[:, :, :, z_slice])
    global_max = np.max(u[:, :, :, z_slice])

    # consistent y-axis scaling for line plots
    u_line_min = np.min(u[:, :, y_slice, z_slice])
    u_line_max = np.max(u[:, :, y_slice, z_slice])
    v_line_min = np.min(v[:, :, y_slice, z_slice])
    v_line_max = np.max(v[:, :, y_slice, z_slice])

    line_global_min = min(u_line_min, v_line_min)
    line_global_max = max(u_line_max, v_line_max)

    for t in np.arange(0, nt, dn):
        fig, axs = plt.subplots(2, 1, figsize=(6, 8))

        # 2D heatmap of u slice
        im = axs[0].imshow(u[t, :, :, z_slice].T, cmap='viridis', vmin=global_min, vmax=global_max)
        axs[0].set_title(rf'u[t={np.round(t*0.1,1)}, $z_{{idx}}$ = {z_slice}]')
        axs[0].set_xlabel('x')
        axs[0].set_ylabel('y')
        fig.colorbar(im, ax=axs[0])

        # line slice through the middle of y for both u and v
        u_line = u[t, :, y_slice, z_slice]
        v_line = v[t, :, y_slice, z_slice]

        axs[1].plot(np.arange(nx), u_line, label=f'$u$')
        axs[1].plot(np.arange(nx), v_line, label=f'$v, w$')
        axs[1].set_ylim(1.1 * line_global_min, 1.1 * line_global_max)
        axs[1].set_xlim(0, nx - 1)
        axs[1].set_title(rf'slice at $y_{{idx}}$ = {y_slice}, $z_{{idx}}$ = {z_slice}, t = {np.round(t*0.1,1)}s')
        axs[1].set_xlabel('x')
        axs[1].set_ylabel('value')
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()

# usage
plot(
    "/home/jgre668/3K3D-soml/outputs/SOML25tNf_merge_investigation/binary/3K3D_u.bin",
    "/home/jgre668/3K3D-soml/outputs/SOML25tNf_merge_investigation/binary/3K3D_v.bin",
    dn = 20
)