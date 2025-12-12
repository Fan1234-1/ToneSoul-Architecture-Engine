
import math
from typing import List

Vector = List[float]


def dot_product(v1: Vector, v2: Vector) -> float:
    """Calculates the dot product of two vectors."""
    if len(v1) != len(v2):
        raise ValueError(f"Vector dimensions mismatch: {len(v1)} vs {len(v2)}")
    return sum(x * y for x, y in zip(v1, v2))


def magnitude(v: Vector) -> float:
    """Calculates the magnitude (Euclidean norm) of a vector."""
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """Calculates the cosine similarity between two vectors."""
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product(v1, v2) / (mag1 * mag2)


def add_vectors(v1: Vector, v2: Vector) -> Vector:
    """Adds two vectors element-wise."""
    if len(v1) != len(v2):
        raise ValueError(f"Vector dimensions mismatch: {len(v1)} vs {len(v2)}")
    return [x + y for x, y in zip(v1, v2)]


def scale_vector(v: Vector, scalar: float) -> Vector:
    """Multiplies a vector by a scalar."""
    return [x * scalar for x in v]


def normalize_vector(v: Vector) -> Vector:
    """Returns the unit vector."""
    mag = magnitude(v)
    if mag == 0:
        return [0.0] * len(v)
    return [x / mag for x in v]
