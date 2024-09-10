# Error within 1ppm is acceptable
epsilon = 1e-6
# Calcula1te the barycentric coordinates of p
p1 = t.a
p2 = t.b
p3 = t.c
# Make sure the point isn't a vertex
if p == p1 or p == p2 or p == p3:
    return True
denom = (p2.y - p3.y)*(p1.x - p3.x) + (p3.x - p2.x)*(p1.y - p3.y)
if denom != 0:
    alpha = ((p2.y - p3.y)*(p.x - p3.x) + (p3.x - p2.x)*(p.y - p3.y))/denom
    beta = ((p3.y - p1.y)*(p.x - p3.x) + (p1.x - p3.x)*(p.y - p3.y))/denom
    gamma = 1.0 - alpha - beta
    # If all three coordinates are positive, p lies within t
    return alpha+epsilon >= 0 and beta+epsilon >= 0 and gamma+epsilon >= 0
# Invalid triangle
else:
    return False