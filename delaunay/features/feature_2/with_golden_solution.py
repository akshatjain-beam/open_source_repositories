# Simplest case
if a == b:
    return True

# Order doesn't matter; triangles are the same if they have the same vertices
if a[0] in b and a[1] in b and a[2] in b:
    return True

# Try reversing edges for edge-defined triangles
if a[0][::-1] in b and a[1][::-1] in b and a[2][::-1] in b:
    return True

return False