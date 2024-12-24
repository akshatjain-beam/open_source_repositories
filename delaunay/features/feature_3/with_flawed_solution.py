```
def tri_contains_point(t, p):
    """
    Determine whether the given triangle contains the given point using Barycentric Coordinates.

    Arguments:
    t is a Triangle object
    p is a Point object

    Returns:
    True if t contains p and False otherwise.

    Note:
    Epsilon is used to handle floating-point precision errors and is set to a small value (e.g., 1e-6).
    """
    epsilon = 1e-6
    # Calculate Barycentric Coordinates
    AreaT = 1/2 * ((t.b.x * t.c.y - t.c.x * t.b.y) - (t.a.x * t.c.y - t.c.x * t.a.y) + (t.a.x * t.b.y - t.b.x * t.a.y))
    lambda1 = 1/2 * ((p.x * t.c.y - t.c.x * p.y) - (t.b.x * t.c.y - t.c.x * t.b.y) + (t.b.x * p.y - p.x * t.b.y)) / AreaT
    lambda2 = 1/2 * ((t.a.x * p.y - p.x * t.a.y) - (t.a.x * t.c.y - t.c.x * t.a.y) + (p.x * t.c.y - t.c.x * p.y)) / AreaT
    lambda3 = 1 - lambda1 - lambda2

    # Check if point is inside the triangle
    return 0 - epsilon <= lambda1 <= 1 + epsilon and 0 - epsilon <= lambda2 <= 1 + epsilon and 0 - epsilon <= lambda3 <= 1 + epsilon
```