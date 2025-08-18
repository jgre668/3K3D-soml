import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def create_initial_conditions_3d(data_idx, output_directory, params, plot = True):

    cmap = params['cmap']

    x_min = params['x_min'] # domain boundaries
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']
    z_min = params['z_min']
    z_max = params['z_max']

    dx = params['dx'] # spatial resolution
    dy = params['dy']
    dz = params['dz']

    radius = params['radius']  # radius of each perturbation

    u0_lower, u0_upper = params['states']
    a = u0_upper - u0_lower  # perturbation amplitude

    output_directory = params['output_directory']

    boundary_condition = params['boundary_condition']

    # number of steps in grid
    nx = int((x_max - x_min) / dx + 1)
    ny = int((y_max - y_min) / dy + 1)
    nz = int((z_max - z_min) / dz + 1)

    # initialise fields
    U_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)
    V_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)
    W_init = np.full((nx, ny, nz), u0_lower, dtype=np.float32)

    scale_factor = nx / (x_max - x_min)

    r_idx = radius * scale_factor

    # this is the width of the perturbation block
    # (number of discretised points, equivalent to 2*diameter)
    width = 4 * radius
    w_idx = int(width * scale_factor)

    curvature = radius / 5
    c_idx = curvature * scale_factor

    # initialise perturbation block
    P = np.zeros((w_idx, w_idx, w_idx), dtype=np.float32)

    # loop through perturbation block
    cx = cy = cz = w_idx // 2
    for i in range(w_idx):
        for j in range(w_idx):
            for k in range(w_idx):
                dist = np.sqrt((i - cx) ** 2 + (j - cy) ** 2 + (k - cz) ** 2)
                P[i, j, k] = a / 2 * (1 + np.tanh((r_idx - dist) / c_idx))

    # apply perturbations
    for x_idx, y_idx, z_idx in data_idx:

        # Neumann
        if boundary_condition == 0:
            # top-left-front corner in main grid
            start_i = int(x_idx - w_idx // 2)
            start_j = int(y_idx - w_idx // 2)
            start_k = int(z_idx - w_idx // 2)

            # bounds in main grid
            end_i = min(start_i + w_idx, U_init.shape[0])
            end_j = min(start_j + w_idx, U_init.shape[1])
            end_k = min(start_k + w_idx, U_init.shape[2])

            # bounds in perturbation block
            P_i0 = max(0, -start_i)
            P_j0 = max(0, -start_j)
            P_k0 = max(0, -start_k)

            P_i1 = P_i0 + (end_i - max(start_i, 0))
            P_j1 = P_j0 + (end_j - max(start_j, 0))
            P_k1 = P_k0 + (end_k - max(start_k, 0))

            # slices for main grid
            gi0, gj0, gk0 = max(start_i, 0), max(start_j, 0), max(start_k, 0)
            gi1, gj1, gk1 = end_i, end_j, end_k

            # apply clipped perturbation
            U_init[gi0:gi1, gj0:gj1, gk0:gk1] += P[P_i0:P_i1, P_j0:P_j1, P_k0:P_k1]
            # V_init[gi0:gi1, gj0:gj1, gk0:gk1] += P[P_i0:P_i1, P_j0:P_j1, P_k0:P_k1]
            # W_init[gi0:gi1, gj0:gj1, gk0:gk1] += P[P_i0:P_i1, P_j0:P_j1, P_k0:P_k1]

        # cyclic
        elif boundary_condition == 1:

            # base indices for perturbation block (wrapped per axis)
            is_ = (np.arange(w_idx) + x_idx - w_idx // 2) % U_init.shape[0]
            js_ = (np.arange(w_idx) + y_idx - w_idx // 2) % U_init.shape[1]
            ks_ = (np.arange(w_idx) + z_idx - w_idx // 2) % U_init.shape[2]

            # apply using broadcasting via np.ix_ to each component
            U_init[np.ix_(is_, js_, ks_)] += P
            V_init[np.ix_(is_, js_, ks_)] += P
            W_init[np.ix_(is_, js_, ks_)] += P

    # cut off any bits that are above the upper stationary state
    np.clip(U_init, None, u0_upper, out=U_init)
    # np.clip(V_init, None, u0_upper, out=V_init)
    # np.clip(W_init, None, u0_upper, out=W_init)


    # write binary file
    with open(Path(output_directory) / 'binary/initial_conditions.bin', 'wb') as f:
        U_init.flatten(order='C').astype('<f4').tofile(f)
        V_init.flatten(order='C').astype('<f4').tofile(f)
        W_init.flatten(order='C').astype('<f4').tofile(f)

    # plotting
    if plot:
        
        fig = plt.figure(figsize=(18, 6), constrained_layout=True)
        gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1])

        # PERTURBATION SURFACE
        ax1 = fig.add_subplot(gs[0], projection='3d')
        xp = np.linspace(0.0, width, w_idx)
        yp = np.linspace(0.0, width, w_idx)
        XP, YP = np.meshgrid(xp, yp)
        P_slice = P[:, :, w_idx // 2]

        ax1.plot_surface(XP, YP, P_slice, cmap=cmap, edgecolor='none')
        ax1.set_title('3D perturbation (mid z-slice)', pad=10)
        ax1.set_xlabel('$x$', labelpad=8)
        ax1.set_ylabel('$y$', labelpad=8)
        ax1.set_zlabel('$u$', labelpad=8)
        ax1.set_zlim(-0.3, a + 0.3)

        # MAX PROJECTION
        ax2 = fig.add_subplot(gs[1])
        max_proj = np.max(U_init, axis=2).T
        img = ax2.imshow(max_proj, cmap=cmap, origin='lower')
        ax2.set_title('Initial $u$ field (max projection)', pad=10)
        ax2.set_xlabel('$x$')
        ax2.set_ylabel('$y$')
        cbar = fig.colorbar(img, ax=ax2, shrink=0.8, pad=0.02)
        cbar.set_label('$u$')

        # MID Z SLICE OF U-FIELD
        ax3 = fig.add_subplot(gs[2], projection='3d')
        z_mid = nz // 2
        x = np.linspace(x_min, x_max, nx)
        y = np.linspace(y_min, y_max, ny)
        X, Y = np.meshgrid(x, y)
        U_slice = U_init[:, :, z_mid].T

        ax3.plot_surface(X, Y, U_slice, cmap=cmap, edgecolor='none')
        ax3.set_title('Initial $u$ field (mid z-slice)', pad=10)
        ax3.set_xlabel('$x$', labelpad=8)
        ax3.set_ylabel('$y$', labelpad=8)
        ax3.set_zlabel('$u$', labelpad=8)
        ax3.set_zlim(u0_lower - 0.3, u0_upper + 0.5)

        plt.savefig(Path(output_directory) / 'plots/initial_conditions_plot.png', dpi=300, bbox_inches='tight')



