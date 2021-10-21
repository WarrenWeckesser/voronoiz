
import numpy as np
from voronoiz import voronoi_grid
from numpngw import write_apng


xmin = 0
xmax = 5
ymin = 0
ymax = 5

points = np.array([[0.00, 0.00],
                   [1.00, 4.51],
                   [1.20, 0.30],
                   [2.50, 2.60],
                   [2.40, 0.80],
                   [4.40, 3.30],
                   [1.95, 3.00],
                   [3.71, 1.90],
                   [4.50, 3.66],
                   [4.67, 0.21]])

gridsize = 299

for kwargs in [dict(metric='cityblock'),
               dict(metric='minkowski', p=2),
               dict(metric='minkowski', p=4)]:
    imgs = []
    for theta in np.linspace(0, 2*np.pi, 250, endpoint=False):
        # points[0] will travel about a circle.
        points[0] = 2.5 + 1.5*np.array([np.cos(theta), np.sin(theta)])
        img = voronoi_grid(points, xmin, xmax, ymin, ymax,
                           gridsize=(gridsize, gridsize),
                           **kwargs)
        img = (160//(len(points)+1)*img + 64).astype(np.uint8)
        img[img == 64] = 0
        for x, y in points:
            i = int(gridsize*(x - xmin)/(xmax - xmin))
            j = int(gridsize*(y - ymin)/(ymax - ymin))
            img[j-1:j+2, i-1:i+2] = 255
        img = np.pad(img, pad_width=1, mode='constant', constant_values=255)
        imgs.append(img)

    tag = '_'.join(f"{key}_{value}" for key, value in kwargs.items())
    write_apng(f'animation_{tag}.png', imgs, delay=100)
