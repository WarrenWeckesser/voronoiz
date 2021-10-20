# Copyright © 2021 Warren Weckesser


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as PolygonPatch
from matplotlib.collections import PatchCollection
from shapely.geometry import Polygon

from voronoiz import voronoi_l1
from voronoiz import voronoi_grid


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Some utilities for plotting the results of voronoi_l1 and
# voronoi_grid with a small set of distinct colors.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _create_adjacency_matrix_from_grid(img):
    n = img.max() + 1
    A = np.zeros((n, n), dtype=int)
    for row in range(img.shape[0]-1):
        for col in range(img.shape[1]-1):
            v = img[row, col]
            v10 = img[row+1, col]
            v01 = img[row, col+1]
            v11 = img[row+1, col+1]
            if v != v10:
                A[v, v10] = 1
                A[v10, v] = 1
            if v != v01:
                A[v, v01] = 1
                A[v01, v] = 1
            if v != v11:
                A[v, v11] = 1
                A[v11, v] = 1
    return A


def _create_adjacency_matrix(cells):
    polys = [Polygon(cell) for cell in cells]
    n = len(polys)
    A = np.zeros((n, n), dtype=int)  # dtype=bool would also work.
    for i, pi in enumerate(polys[:-1]):
        for j, pj in enumerate(polys[i+1:]):
            bnds = pi.intersection(pj).bounds
            if (len(bnds) > 0 and
                    not (bnds[0] == bnds[1] == bnds[2] == bnds[3])):
                A[i, i+j+1] = 1
                A[i+j+1, i] = 1
    return A


def _color(A):
    # Color the graph of adjacencies using a greedy algorithm.
    n = len(A)
    colors = np.zeros(n, dtype=int)
    used_colors = {0}
    for k in range(1, n):
        adj = A[k, :k].nonzero()
        adj_colors = set(colors[adj])
        available_colors = used_colors - adj_colors
        if len(available_colors) > 0:
            colors[k] = available_colors.pop()
        else:
            new_color = max(used_colors) + 1
            colors[k] = new_color
            used_colors.add(new_color)
    return colors


def _color_grid(img):
    A = _create_adjacency_matrix_from_grid(img)
    return _color(A)


def _color_cells(cells):
    A = _create_adjacency_matrix(cells)
    return _color(A)


# For matplotlib PNG output.
DPI = 125

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Create some demo data.
rng = np.random.default_rng(0xb34871f189237a45e445ffb3790c3e1b)
points = rng.multivariate_normal([0, 0], np.diag([5, 1]), size=20)

# Compute values for the bounding box around the points.
# The excess size beyond the data minima and maxima was
# chosen for appearance only.  It can be smaller.
delta = (1/5)*np.ptp(points, axis=0)
xmin, ymin = points.min(axis=0) - delta
xmax, ymax = points.max(axis=0) + delta

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Figure 1: "Exact" Voronoi regions.
# Compute the Voronoi L1 polygons around each point, and plot
# the result with lines and colored patches.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cells = voronoi_l1(points, xmin, xmax, ymin, ymax)

# Plot parameters
cmap = 'cividis'
alpha = 0.55
figsize = (6, 6*(ymax - ymin)/(xmax - xmin) + 0.8)

plt.figure(1, figsize=figsize)
plt.plot(points[:, 0], points[:, 1], 'k.', markersize=4)

# Plot the outline of each Voronoi cell, and create a list of
# matplotlib Polygons (here called PolygonPatch because Polygon
# refers to the shapely Polygon class).
patches = []
for vpoly in cells:
    plt.plot(vpoly[:, 0], vpoly[:, 1], 'k', alpha=0.6, linewidth=0.5)
    patch = PolygonPatch(vpoly)
    patches.append(patch)

p = PatchCollection(patches, alpha=alpha)

# If use_few_colors is False, the colors used in figure 1 (for the
# plot of the result of voronoi_l1) will be the same as those used
# in figure 2.  If it is True, a greedy algorithm is used to color
# the adjacency graph so that no two neighbors have the same color.
use_few_colors = True
if use_few_colors:
    colors = _color_cells(cells)
    ncolors = colors.max() + 1
    clrs = plt.get_cmap(cmap)(np.linspace(0, 1, ncolors))
    p.set_color(clrs[colors])
else:
    clrs = plt.get_cmap(cmap)(np.linspace(0, 1, len(points)))
    p.set_color(clrs)

ax = plt.gca()
ax.add_collection(p)
ax.set_xlim((xmin, xmax))
ax.set_ylim((ymin, ymax))
ax.set_aspect('equal', adjustable='box')
plt.title("$L^1$ Voronoi Diagram\n"
          "(computed with $\\mathtt{\\bf voronoi\\_l1}$)")
plt.grid(True, color='k', alpha=0.1)

plt.savefig('demo_fig1.png', dpi=DPI)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Figure 2: Use `voronoi_grid` to create an image of the Voronoi
# diagram with the L1 metric.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

img = voronoi_grid(points, xmin, xmax, ymin, ymax,
                   gridsize=(1500, 1500),
                   metric='cityblock')

colors = _color_grid(img)
img2 = colors[img]  # Recolor the image.
plt.figure(2, figsize=figsize)
plt.imshow(img2[::-1, :], extent=(xmin, xmax, ymin, ymax), alpha=alpha,
           cmap=cmap)
plt.plot(points[:, 0], points[:, 1], 'k.', markersize=4)
plt.grid(True, color='k', alpha=0.1)
plt.title("$L^1$ Voronoi Diagram\n"
          "(computed with $\\mathtt{\\bf voronoi\\_grid}$)")

plt.savefig('demo_fig2.png', dpi=DPI)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Figure 3: Use `voronoi_grid` to create an image of the Voronoi
# diagram with the L3 metric.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

img = voronoi_grid(points, xmin, xmax, ymin, ymax,
                   gridsize=(1500, 1500),
                   metric='minkowski', p=4)

colors = _color_grid(img)
img2 = colors[img]  # Recolor the image.
plt.figure(3, figsize=figsize)
plt.imshow(img2[::-1, :], extent=(xmin, xmax, ymin, ymax), alpha=alpha,
           cmap=cmap)
plt.plot(points[:, 0], points[:, 1], 'k.', markersize=4)
plt.grid(True, color='k', alpha=0.1)
plt.title("$L^4$ Voronoi Diagram\n"
          "(computed with $\\mathtt{\\bf voronoi\\_grid}$)")

plt.savefig('demo_fig3.png', dpi=DPI)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

plt.show()
