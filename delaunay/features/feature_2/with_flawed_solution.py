```
    # Check if the inputs are valid -- need to be Triangles or 3-tuples
    if not isinstance(a, Triangle) and not isinstance(a, tuple):
        return False
    if not isinstance(b, Triangle) and not isinstance(b, tuple):
        return False
    # If the inputs are edge defined, we need to convert to vertex defined
    if isinstance(a, tuple):
        a = edges_to_vertices(a)
    if isinstance(b, tuple):
        b = edges_to_vertices(b)
    # Check if both triangles have the same vertices
    return (a.a == b.a or a.a == b.b or a.a == b.c) and \
           (a.b == b.a or a.b == b.b or a.b == b.c) and \
           (a.c == b.a or a.c == b.b or a.c == b.c)
```