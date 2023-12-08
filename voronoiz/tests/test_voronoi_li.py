import numpy as np
from numpy.testing import assert_allclose
from voronoiz import voronoi_l1


def test_basic():
    z = [[1, 1], [3, 2]]
    regions = voronoi_l1(z, 0, 4, 0, 3)
    expected_regions = [
        [[0.0, 0.0],
         [2.5, 0.0],
         [2.5, 1.0],
         [1.5, 2.0],
         [1.5, 3.0],
         [0.0, 3.0]],
        [[4.0, 3.0],
         [1.5, 3.0],
         [1.5, 2.0],
         [2.5, 1.0],
         [2.5, 0.0],
         [4.0, 0.0]],
    ]
    for region, expected_region in zip(regions, expected_regions):
        assert (region[0] == region[-1]).all()
        region1 = region[:-1]
        start = expected_region[0]
        k = np.where((region1 == start).all(axis=1))[0][0]
        if k != 0:
            region1_shifted = np.concatenate((region1[k:], region1[:k]))
        else:
            region1_shifted = region1
        assert_allclose(region1_shifted, expected_region, rtol=1e-14)
