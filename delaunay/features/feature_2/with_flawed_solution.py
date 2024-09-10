# Check if the inputs are valid
if not isinstance(a, (Triangle, tuple)) or not isinstance(b, (Triangle, tuple)):
    return False
if len(a) != 3 or len(b) != 3:
    return False
# Make sets of the triangle vertices
a_vertices = set(a)
b_vertices = set(b)
# If the sets are equal, the triangles are equal
return a_vertices == b_vertices