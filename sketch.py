import math
from typing import List, Tuple
import numpy as np


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.theta1 = 0
        self.theta2 = np.pi / 2

    def find_intersection(self, other_circle) -> List[Tuple[float, float]]:
        # Calculate the distance between the centers of the circles
        d = math.sqrt((other_circle.x - self.x) ** 2 + (other_circle.y - self.y) ** 2)

        # Check if the circles are too far apart to intersect
        if d > self.radius + other_circle.radius:
            return None  # No intersection, circles are separate

        # Check if one circle is completely inside the other
        if d < abs(self.radius - other_circle.radius):
            return None  # No intersection, one circle is inside the other

        # Calculate the intersection points
        a = (self.radius**2 - other_circle.radius**2 + d**2) / (2 * d)
        h = math.sqrt(self.radius**2 - a**2)
        x3 = self.x + a * (other_circle.x - self.x) / d
        y3 = self.y + a * (other_circle.y - self.y) / d

        # Calculate the intersection points
        intersection_x1 = x3 + h * (other_circle.y - self.y) / d
        intersection_y1 = y3 - h * (other_circle.x - self.x) / d
        intersection_x2 = x3 - h * (other_circle.y - self.y) / d
        intersection_y2 = y3 + h * (other_circle.x - self.x) / d

        return [(intersection_x1, intersection_y1), (intersection_x2, intersection_y2)]

    def plot_circle(self, color):
        plt.plot(*self.get_pts(100), color)

    def get_theta(self, point):
        return math.atan2(point[1] - self.y, point[0] - self.x)

    def is_tangent(self, other_circle, tolerance=1e-9):
        d = math.sqrt((other_circle.x - self.x) ** 2 + (other_circle.y - self.y) ** 2)
        return within_tolerance(
            abs(self.radius - other_circle.radius) - d, 0
        ) or within_tolerance(self.radius + other_circle.radius - d, 0)

    def get_pts(self, num_pts):
        thetas = np.linspace(self.theta1, self.theta2, num_pts)
        return self.x + self.radius * np.cos(thetas), self.y + self.radius * np.sin(
            thetas
        )


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def plot_line(self, color):
        plt.plot([self.x1, self.x2], [self.y1, self.y2], color + "-")

    def get_pts(self, num_pts):
        return [self.x1, self.x2], [self.y1, self.y2]
        return np.linspace(self.x1, self.x2, num_pts), np.linspace(
            self.y1, self.y2, num_pts
        )


def within_tolerance(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance


def get_pts(drawing,fn=100):
    x, y = drawing[0].get_pts(fn)
    for each in drawing[1:]:
        x2, y2 = each.get_pts(fn)
        if not within_tolerance(x2[0],x[-1]) or not within_tolerance(y2[0],y[-1]):
            x2 = x2[::-1]
            y2 = y2[::-1]
        x = np.concatenate([x, x2])
        y = np.concatenate([y, y2])
    return x,y
def mirror_pts_y(x,y):
    return np.concatenate([x,-x[::-1]]),np.concatenate([y,y[::-1]])

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Example usage:
    pld = 0.254
    h = 0.75
    b = 0.4
    r1 = 0.15
    r2 = 1
    r3 = 0.555
    i = 0.63
    pitch = 2
    thickness = 1
    circle1 = Circle(0, 0, r3)
    circle2 = Circle(b, -(h - r3), r2)
    circle3 = Circle(-r2 - r1 + b, (-h - pld + r3) + r1, r1)
    circle1.theta1 = circle1.get_theta(circle1.find_intersection(circle2)[0])
    circle1.theta2 = np.pi / 2
    circle2.theta1 = circle2.get_theta(circle1.find_intersection(circle2)[0])
    circle2.theta2 = np.pi
    circle3.theta1 = 0
    circle3.theta2 = -np.pi / 2
    line1 = Line(-pitch / 2, -h - pld + r3, circle3.x, -h - pld + r3)
    line2 = Line(circle3.x + r1, circle3.y, circle2.x - r2, circle2.y)
    line3 = Line(-pitch / 2, -h - pld + r3-thickness,-pitch / 2, -h - pld + r3)
    line4 = Line(0, -h - pld + r3-thickness,-pitch / 2, -h - pld + r3-thickness)
    drawing = [line4,line3, line1, circle3, line2, circle2, circle1]
    plt.plot(*mirror_pts_y(*get_pts(drawing)))
    plt.show()
