from numpy import array as np_array
from numpy.linalg import norm


def euclidean_distance(vector_a: tuple[float, ...], vector_b: tuple[float, ...]) -> float:
    """
    Computes the euclidean distance between two vectors
    """
    assert len(vector_a) == len(vector_b)
    point_1 = np_array(vector_a)
    point_2 = np_array(vector_b)
    return float(norm(point_1 - point_2))
