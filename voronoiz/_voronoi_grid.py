# Copyright © 2021 Warren Weckesser

"""
`voronoi_grid` is for displaying a Voronoi diagram of points in
the plane as an image.
It samples a grid of points and generates an array of integers
that indicate the index in the given `points` array that is
closest to the grid point.  It uses `scipy.spatial.distance.cdist`
to compute the distance, so any metric provided by that function
can be used.  `voronoi_grid` requires SciPy.
"""

import numpy as np


def voronoi_grid(points, xmin, xmax, ymin, ymax,
                 gridsize=(1000, 1000), **kwds):
    """
    Voronoi diagram visualization grid.

    Create a grid in the bounding box defined by (xmin, xmax, ymin, ymax),
    and for each point in the grid, determine the closest point in `points`.

    The return value is the 2-d array of indices into `points`.

    Additional keyword arguments are passed to scipy.spatial.distance.cdist.

    """
    from scipy.spatial.distance import cdist

    nx, ny = gridsize
    X, Y = np.meshgrid(np.linspace(xmin, xmax, ny),
                       np.linspace(ymin, ymax, ny), indexing='xy')
    z = np.column_stack((X.ravel(), Y.ravel()))

    dists = cdist(points, z, **kwds)

    lbl = np.argmin(dists, axis=0).reshape(X.shape)
    return lbl
