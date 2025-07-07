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

    # load arrays
    nt, nx, ny, nz, array_u = read_binary_3K3D(u_data_path)
    nt, nx, ny, nz, array_v = read_binary_3K3D(v_data_path)

    # consistent color scale across all imshow plots
    global_min = np.min(array_u)
    global_max = np.max(array_u)

    # consistent y-limits for line plots
    line_global_min = min(np.min(array_u), np.min(array_v))
    line_global_max = max(np.max(array_u), np.max(array_v))

    # slices
    y_idx = ny // 2
    z_idx = nz // 2

    for t in np.arange(0, nt, dn):

        u_snapshot = array_u[t]
        v_snapshot = array_v[t]

        max_disp = np.max(u_snapshot, axis=2)
        slice_disp = u_snapshot[:, :, z_idx]

        # 1D projection line over all y and z
        u_proj_line = np.max(u_snapshot, axis=(1,2))
        v_proj_line = np.max(v_snapshot, axis=(1,2))

        # 1D slice line at fixed y, z
        u_slice_line = u_snapshot[:, y_idx, z_idx]
        v_slice_line = v_snapshot[:, y_idx, z_idx]

        fig, axs = plt.subplots(2, 2, figsize=(12, 12))

        # --- 1) Top-left: Max projection along z (still 2D)
        im0 = axs[0, 0].imshow(
            max_disp.T,
            origin='lower',
            extent=(0, nx, 0, ny),
            aspect='equal',
            cmap='viridis',
            vmin=global_min,
            vmax=global_max
        )
        axs[0, 0].set_title(f"Max projection along z (t = {t})")
        axs[0, 0].set_xlabel("x")
        axs[0, 0].set_ylabel("y")
        fig.colorbar(im0, ax=axs[0, 0], fraction=0.046, pad=0.04, label="Value")

        # --- 2) Top-right: z-slice
        im1 = axs[0, 1].imshow(
            slice_disp.T,
            origin='lower',
            extent=(0, nx, 0, ny),
            aspect='equal',
            cmap='viridis',
            vmin=global_min,
            vmax=global_max
        )
        axs[0, 1].set_title(f"Slice at z={z_idx} (t = {t})")
        axs[0, 1].set_xlabel("x")
        axs[0, 1].set_ylabel("y")
        fig.colorbar(im1, ax=axs[0, 1], fraction=0.046, pad=0.04, label="Value")

        # --- 3) Bottom-left: Line profile of max over y and z
        axs[1, 0].plot(np.arange(nx), u_proj_line, label="u max(y,z)", color="blue")
        axs[1, 0].plot(np.arange(nx), v_proj_line, label="v max(y,z)", color="red")
        axs[1, 0].set_ylim(1.1 * line_global_min, 1.1 * line_global_max)
        axs[1, 0].set_xlim(0, nx - 1)
        axs[1, 0].set_title(f"Max over y,z per x (t={t})")
        axs[1, 0].set_xlabel("x")
        axs[1, 0].set_ylabel("Value")
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        # --- 4) Bottom-right: Line profile of z-slice at fixed y
        axs[1, 1].plot(np.arange(nx), u_slice_line, label="u slice", color="blue")
        axs[1, 1].plot(np.arange(nx), v_slice_line, label="v slice", color="red")
        axs[1, 1].set_ylim(1.1 * line_global_min, 1.1 * line_global_max)
        axs[1, 1].set_xlim(0, nx - 1)
        axs[1, 1].set_title(f"Line profile of z-slice (y={y_idx}, z={z_idx}, t={t})")
        axs[1, 1].set_xlabel("x")
        axs[1, 1].set_ylabel("Value")
        axs[1, 1].legend()
        axs[1, 1].grid(True)

        plt.tight_layout()
        plt.show()