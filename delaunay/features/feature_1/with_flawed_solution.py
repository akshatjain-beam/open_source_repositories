```
    colors = []
    # Calculate the diagonal length of the image
    diagonal_length = sqrt(image_size[0]**2 + image_size[1]**2) 

    for triangle in triangles:
        # Find the center point (centroid) of the triangle
        centroid = tri_centroid(triangle)
        
        # Ensure the centroid is within the image boundaries
        centroid = (max(0, centroid[0]), max(0, centroid[1]))
        centroid = (min(image_size[0]-1, centroid[0]), min(image_size[1]-1, centroid[1]))
        
        # Calculate the distance of the centroid from the origin (0,0)
        distance_from_origin = sqrt(centroid[0]**2 + centroid[1]**2)
        
        # Normalize the distance to be a value between 0 and 1
        val = distance_from_origin / diagonal_length
        
        # Get the color corresponding to this distance on the gradient
        colors.append(calculate_color(gradient, val))

    return colors
```