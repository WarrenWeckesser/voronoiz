voronoiz
--------

Some functions for computing Voronoi diagrams for points in the
plane for metrics other than the Euclidean metric.

* `voronoi_l1` creates Voronoi cells (polygons) for a set of points
  using the L1 metric (also known as the city-block metric,
  the Manhattan metric, or the taxicab metric). The function
  requires the Shapely library (https://pypi.org/project/Shapely/).
* `voronoi_grid` is for displaying a Voronoi diagram as an image.
  It samples a grid of points and generates an array of integers
  that indicate the index in the given `points` array that is
  closest to the grid point.  It uses `scipy.spatial.distance.cdist`
  to compute the distance, so any metric provided by that function
  can be used.  `voronoi_grid` requires SciPy.

Demonstration code is in `examples/voronoi_demo.py`.  When that file
is run, it generates these plots of the result of `voronoi_l1` and
`voronoi_grid` applied to a random  set of points:


![](https://github.com/WarrenWeckesser/voronoiz/blob/main/examples/demo_fig1.png)

![](https://github.com/WarrenWeckesser/voronoiz/blob/main/examples/demo_fig2.png)

![](https://github.com/WarrenWeckesser/voronoiz/blob/main/examples/demo_fig3.png)
