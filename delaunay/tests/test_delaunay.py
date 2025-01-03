import os
import sys

lib_path = os.path.abspath('..')
sys.path.append(lib_path)
from geometry import Point, Triangle
from delaunay import color_from_gradient, Color, Gradient, calculate_color, tri_centroid

import unittest
from math import sqrt



class TestColorFromGradient(unittest.TestCase):

    def setUp(self):
        # Create a dummy gradient for testing
        self.gradient = Gradient(Color(255, 248, 9), Color(255, 65, 9))
        # Create a sample image size
        self.image_size = (100, 100)

    def test_single_triangle(self):
        """
        Test a single triangle to check if the color is correctly calculated based on the gradient.
        Evaluates the basic functionality of color_from_gradient with a simple input.
        """
        triangle = Triangle(Point(10, 10), Point(20, 10), Point(15, 20))
        centroid_x, centroid_y = 15, 13.33
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(centroid_x**2 + centroid_y**2) / s
        expected_color = calculate_color(self.gradient, frac)

        colors = color_from_gradient(
            self.gradient, self.image_size, [triangle])
        self.assertEqual(
            len(colors), 1, "The number of colors returned is incorrect.")
        self.assertEqual(
            colors[0], expected_color, f"Expected color: {expected_color}, but got: {colors[0]}")

    def test_multiple_triangles(self):
        """
        Test multiple triangles to ensure each is assigned the correct color from the gradient.
        Evaluates the function's ability to handle and correctly process a list of triangles.
        """
        triangles = [
            Triangle(Point(10, 10), Point(20, 10), Point(15, 20)),
            Triangle(Point(30, 30), Point(40, 30), Point(35, 40)),
            Triangle(Point(50, 50), Point(60, 50), Point(55, 60))
        ]

        colors = color_from_gradient(self.gradient, self.image_size, triangles)

        for t in triangles:
            centroid_x, centroid_y = tri_centroid(t)
            s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
            frac = sqrt(centroid_x**2 + centroid_y**2) / s
            expected_color = calculate_color(self.gradient, frac)
            self.assertIn(expected_color, colors,
                          "Colors do not match the expected values.")

    def test_triangle_at_image_boundary(self):
        """
        Test a triangle with vertices on the image boundary to ensure correct color calculation.
        Evaluates how the function handles triangles that lie exactly on the boundaries of the image.
        """
        triangle = Triangle(Point(0, 0), Point(100, 0), Point(0, 100))
        centroid_x, centroid_y = (0 + 100 + 0) / 3, (0 + 0 + 100) / 3
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(centroid_x**2 + centroid_y**2) / s
        expected_color = calculate_color(self.gradient, frac)

        colors = color_from_gradient(
            self.gradient, self.image_size, [triangle])
        self.assertEqual(len(colors), 1)
        self.assertEqual(colors[0], expected_color)

    def test_empty_triangle_list(self):
        """
        Test with an empty list of triangles to ensure the function returns an empty list.
        Validates that the function can handle empty inputs gracefully.
        """
        colors = color_from_gradient(self.gradient, self.image_size, [])
        self.assertEqual(
            colors, [], "The function should return an empty list for an empty triangle list.")

    def test_triangle_with_vertices_at_edges(self):
        """
        Test a triangle with vertices exactly at the edges of the image.
        Evaluates how the function handles triangles that lie exactly on different edge positions.
        """
        triangle = Triangle(Point(0, 0), Point(100, 0), Point(0, 100))
        centroid_x, centroid_y = (0 + 100 + 0) / 3, (0 + 0 + 100) / 3
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(centroid_x**2 + centroid_y**2) / s
        expected_color = calculate_color(self.gradient, frac)

        colors = color_from_gradient(
            self.gradient, self.image_size, [triangle])
        self.assertEqual(len(colors), 1)
        self.assertEqual(colors[0], expected_color)

    def test_gradient_with_identical_colors(self):
        """
        Test a gradient where the start and end colors are identical to ensure consistent output.
        Checks if the function can handle gradients where the color does not change.
        """
        gradient = Gradient(Color(100, 100, 100), Color(100, 100, 100))
        triangle = Triangle(Point(10, 10), Point(20, 10), Point(15, 20))
        centroid_x, centroid_y = 15, 13.33
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(centroid_x**2 + centroid_y**2) / s
        expected_color = calculate_color(gradient, frac)

        colors = color_from_gradient(gradient, self.image_size, [triangle])
        self.assertEqual(len(colors), 1)
        self.assertEqual(colors[0], expected_color)

    def test_clamped_centroid_outside_image(self):
        """
        Test a triangle with a centroid outside the image boundaries to ensure proper clamping and color calculation.
        Validates that centroids outside the image are correctly clamped within the image boundaries.
        """
        # Triangle with centroid outside the image boundaries
        triangle = Triangle(Point(150, 150), Point(160, 150), Point(155, 160))
        # Calculate the centroid
        centroid_x, centroid_y = tri_centroid(triangle)
        # Bound centroid to boundaries of the image
        c_x = min(max(0, centroid_x), self.image_size[0])
        c_y = min(max(0, centroid_y), self.image_size[1])
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(c_x**2 + c_y**2) / s
        expected_color = calculate_color(self.gradient, frac)

        colors = color_from_gradient(
            self.gradient, self.image_size, [triangle])
        self.assertEqual(len(colors), 1)
        self.assertEqual(
            colors[0], expected_color, f"Expected color: {expected_color}, but got: {colors[0]}")

    def test_clamped_centroid_on_edge(self):
        """
        Test a triangle with a centroid exactly on the image boundary to ensure proper clamping and color calculation.
        Evaluates if the function can handle centroids that lie precisely on the edge.
        """
        # Triangle with centroid exactly on the image boundary
        triangle = Triangle(Point(100, 100), Point(100, 0), Point(0, 100))
        # Calculate the centroid
        centroid_x, centroid_y = tri_centroid(triangle)
        # Bound centroid to boundaries of the image
        c_x = min(max(0, centroid_x), self.image_size[0])
        c_y = min(max(0, centroid_y), self.image_size[1])
        s = sqrt(self.image_size[0]**2 + self.image_size[1]**2)
        frac = sqrt(c_x**2 + c_y**2) / s
        expected_color = calculate_color(self.gradient, frac)

        colors = color_from_gradient(
            self.gradient, self.image_size, [triangle])
        self.assertEqual(len(colors), 1)
        self.assertEqual(
            colors[0], expected_color, f"Expected color: {expected_color}, but got: {colors[0]}")


if __name__ == '__main__':
    unittest.main()
