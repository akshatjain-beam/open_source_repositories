    epsilon = 1e-6
    # Calculate the area of the triangle
    area_t = 0.5 * abs((t.b.x * t.c.y - t.c.x * t.b.y) - (t.a.x * t.c.y - t.c.x * t.a.y) + (t.a.x * t.b.y - t.b.x * t.a.y))
    if area_t == 0:
        raise ValueError("Degenerate triangle (area is zero)")
    # Calculate barycentric coordinates
    lambda1 = ((t.b.y - t.c.y) * (p.x - t.c.x) + (t.c.x - t.b.x) * (p.y - t.c.y)) / (2 * area_t)
    lambda2 = ((t.c.y - t.a.y) * (p.x - t.c.x) + (t.a.x - t.c.x) * (p.y - t.c.y)) / (2 * area_t)
    lambda3 = 1 - lambda1 - lambda2
    # Check if the point is inside the triangle
    return 0 - epsilon <= lambda1 <= 1 + epsilon and 0 - epsilon <= lambda2 <= 1 + epsilon and 0 - epsilon <= lambda3 <= 1 + epsilon