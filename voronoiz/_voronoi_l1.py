# Copyright © 2021 Warren Weckesser

"""
`voronoi_l1` creates Voronoi cells (polygons) for a set of points
in the plane using the L1 metric (also known as the city-block metric,
the Manhattan metric, or the taxicab metrix). The function
requires the Shapely library (https://pypi.org/project/Shapely/).
"""

import math
import numpy as np


def _l1_closest(p0, p1, xmin, xmax, ymin, ymax):
    """
    Return the vertices of a polygon bounding the set of points where
    the L1 distance to p0 is less than the L1 distance to p1.  The
    region is clipped to the bounding box defined by (xmin, xmax,
    ymin, ymax).

    An error is raised if p0 == p1, and an error is raised if p0 and
    p1 lie on a +-45 degree line.

    Examples
    --------
    >>> _l1_closest(p0=[0, 0], p1=[4, 2], xmin=-1, xmax=5, ymin=-1, ymax=3)
    array([[ 3.,  0.],
           [ 1.,  2.],
           [ 1.,  3.],
           [-1.,  3.],
           [-1., -1.],
           [ 3., -1.],
           [ 3.,  0.]])
    """
    x0, y0 = p0
    x1, y1 = p1
    width = abs(x1 - x0)
    height = abs(y1 - y0)
    if width == height == 0:
        raise ValueError('points must not be equal')
    if width == height:
        raise RuntimeError('points on a 45 degree line')

    flip = False
    if width > height:
        xmin, xmax, ymin, ymax = ymin, ymax, xmin, xmax
        x0, y0, x1, y1 = y0, x0, y1, x1
        width, height = height, width
        flip = True

    if width == 0:
        mid = 0.5*(y0 + y1)
        if y0 < y1:
            p = np.array([[xmin, mid],
                          [xmax, mid],
                          [xmax, ymin],
                          [xmin, ymin],
                          [xmin, mid]])
        else:
            p = np.array([[xmin, mid],
                          [xmin, ymax],
                          [xmax, ymax],
                          [xmax, mid],
                          [xmin, mid]])
    else:
        distance = width + height
        s = math.copysign(1, y1 - y0)
        pa = np.array([x0, y0 + s*0.5*(distance)])
        pb = np.array([x1, y1 - s*0.5*(distance)])
        if x0 < x1 and y0 < y1:
            p = np.array([pa,
                          pb,
                          [xmax, pb[1]],
                          [xmax, ymin],
                          [xmin, ymin],
                          [xmin, pa[1]],
                          pa])
        elif x0 < x1 and y0 > y1:
            p = np.array([pa,
                          pb,
                          [xmax, pb[1]],
                          [xmax, ymax],
                          [xmin, ymax],
                          [xmin, pa[1]],
                          pa])
        elif x0 > x1 and y0 < y1:
            p = np.array([pa,
                          pb,
                          [xmin, pb[1]],
                          [xmin, ymin],
                          [xmax, ymin],
                          [xmax, pa[1]],
                          pa])
        else:
            # x0 > x1 and y0 > y1
            p = np.array([pa,
                          pb,
                          [xmin, pb[1]],
                          [xmin, ymax],
                          [xmax, ymax],
                          [xmax, pa[1]],
                          pa])
    if flip:
        p = p[:, ::-1]
    return p


def voronoi_l1(points, xmin, xmax, ymin, ymax):
    """
    Compute Voronoi cells using the L1 metric.

    The L1 metric is also known as the "city block" metric, the
    taxicab metric, or the Manhattan metric.

    The cells (polygons represented as arrays of 2-d points) are clipped
    to the bounding box defined by `xmin`, `xmax`, `ymin`, `ymax`.

    The return value is a list of numpy arrays.  The i-th list
    has shape (n[i], 2), where n[i] is the number of vertices
    in the Voronoi cell around `points[i]`.

    There must be no duplicate points, and there must not be any points
    that lie on a common 45 or -45 degree line.  The Voronoi cell is
    degenerate in that case, and there are open regions in the plane that
    are equidistant to the two points on the 45 degree line.
    """
    from shapely.geometry import Polygon

    cells = []
    for i0 in range(len(points)):
        p0 = points[i0]
        poly = []
        for i1 in range(len(points)):
            if i1 == i0:
                continue
            p1 = points[i1]
            p = _l1_closest(p0, p1, xmin, xmax, ymin, ymax)
            poly.append(Polygon(p))

        region = poly[0]
        for r in poly[1:]:
            region = region.intersection(r)

        cells.append(np.column_stack(region.exterior.xy))
    return cells
