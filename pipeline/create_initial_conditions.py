import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def create_initial_conditions_3d(data_idx, output_directory, params, plot = True):

    x_min = params['x_min']
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']
    z_min = params['z_min']
    z_max = params['z_max']

    dx = params['dx']
    dy = params['dy']
    dz = params['dz']

    r = params['radius']
    curvature = params['curvature']
    u0_lower, u0_upper = params['states']
    a = u0_upper - u0_lower

    nx = int((x_max - x_min) / dx + 1)
    ny = int((y_max - y_min) / dy + 1)
    nz = int((z_max - z_min) / dz + 1)

    # initialise component fields
    U_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)
    V_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)
    W_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)

    scale_factor = nx / (x_max - x_min)
    w = 4 * r
    w_idx = int(w * scale_factor)
    r_idx = r * scale_factor

    # create 3D perturbation block
    P = np.zeros((w_idx, w_idx, w_idx), dtype=np.float32)
    cx = cy = cz = w_idx // 2
    for i in range(w_idx):
        for j in range(w_idx):
            for k in range(w_idx):
                dist = np.sqrt((i - cx) ** 2 + (j - cy) ** 2 + (k - cz) ** 2)
                P[i, j, k] = a / 2 * (1 + np.tanh((r_idx - dist) / curvature))

    # apply perturbations to U
    for (x_idx, y_idx, z_idx) in data_idx:
        i0 = max(int(x_idx - w_idx // 2), 0)
        j0 = max(int(y_idx - w_idx // 2), 0)
        k0 = max(int(z_idx - w_idx // 2), 0)

        i1 = min(i0 + w_idx, nx)
        j1 = min(j0 + w_idx, ny)
        k1 = min(k0 + w_idx, nz)

        P_crop = P[:i1 - i0, :j1 - j0, :k1 - k0]
        U_init[i0:i1, j0:j1, k0:k1] += P_crop

    # clamp U to upper state
    np.clip(U_init, None, u0_upper, out=U_init)

    # write binary file
    output_path = Path(output_directory) / 'binary/initial_conditions.bin'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        U_init.flatten(order='C').astype('<f4').tofile(f)
        V_init.flatten(order='C').astype('<f4').tofile(f)
        W_init.flatten(order='C').astype('<f4').tofile(f)

    # plotting
    if plot:
        fig = plt.figure(figsize=(18, 6), constrained_layout=True)
        gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1])

        # Plot 1: Perturbation surface
        ax1 = fig.add_subplot(gs[0], projection='3d')
        xp = np.linspace(0.0, w, w_idx)
        yp = np.linspace(0.0, w, w_idx)
        XP, YP = np.meshgrid(xp, yp)
        P_slice = P[:, :, w_idx // 2]

        ax1.plot_surface(XP, YP, P_slice, cmap='viridis', edgecolor='none')
        ax1.set_title('3D perturbation (mid z-slice)', pad=10)
        ax1.set_xlabel('$x$', labelpad=8)
        ax1.set_ylabel('$y$', labelpad=8)
        ax1.set_zlabel('$u$', labelpad=8)
        ax1.set_zlim(-0.3, a + 0.3)

        # Plot 2: Max projection
        ax2 = fig.add_subplot(gs[1])
        max_proj = np.max(U_init, axis=2).T
        img = ax2.imshow(max_proj, cmap='viridis', origin='lower')
        ax2.set_title('Initial $u$ field (max projection)', pad=10)
        ax2.set_xlabel('$x$')
        ax2.set_ylabel('$y$')
        cbar = fig.colorbar(img, ax=ax2, shrink=0.8, pad=0.02)
        cbar.set_label('$u$')

        # Plot 3: Mid-z slice of full field
        ax3 = fig.add_subplot(gs[2], projection='3d')
        z_mid = nz // 2
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        X, Y = np.meshgrid(x, y)
        U_slice = U_init[:, :, z_mid].T

        ax3.plot_surface(X, Y, U_slice, cmap='viridis', edgecolor='none')
        ax3.set_title('Initial $u$ field (mid z-slice)', pad=10)
        ax3.set_xlabel('$x$', labelpad=8)
        ax3.set_ylabel('$y$', labelpad=8)
        ax3.set_zlabel('$u$', labelpad=8)
        ax3.set_zlim(u0_lower - 0.3, u0_upper + 0.5)

        plt.savefig(Path(output_directory) / 'plots/initial_conditions_plot.png', dpi=300, bbox_inches='tight')



