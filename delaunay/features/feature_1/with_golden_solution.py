colors = []
# The size of the screen
s = sqrt(image_size[0]**2+image_size[1]**2)
for t in triangles:
    # The color is determined by the location of the centroid
    tc = tri_centroid(t)
    # Bound centroid to boundaries of the image
    c = (min(max(0, tc[0]), image_size[0]),
            min(max(0, tc[1]), image_size[1]))
    frac = sqrt(c[0]**2+c[1]**2)/s
    colors.append(calculate_color(gradient, frac))
return colors