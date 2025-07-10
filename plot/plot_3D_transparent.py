import numpy as np
import plotly.graph_objects as go

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

# Generate nicely looking random 3D-field
np.random.seed(0)
l = 30
X, Y, Z = np.mgrid[:l, :l, :l]
vol = np.zeros((l, l, l))
pts = (l * np.random.rand(3, 15)).astype(int)
vol[tuple(indices for indices in pts)] = 1
from scipy import ndimage
vol = ndimage.gaussian_filter(vol, 4)

# normalise between 0 and 1
vol /= vol.max()

fig = go.Figure(data=go.Volume(
    x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
    value=vol.flatten(),
    isomin=0.2,
    isomax=0.7,
    opacity=0.1,
    opacityscale=[[0,0], [0.2, 0], [0.5, 1]],
    surface_count = 25,
    ))
fig.update_layout(scene_xaxis_showticklabels=False,
                  scene_yaxis_showticklabels=False,
                  scene_zaxis_showticklabels=False)
fig.show()