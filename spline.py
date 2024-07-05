import matplotlib.pyplot as plt
import numpy as np
import pygame


def bezier_curve(points, num_points=10000):
    curve = []
    t = np.linspace(0, 1, num_points)
    for i in range(num_points):
        p0 = points[0]
        p1 = points[1]
        p2 = points[2]
        p3 = points[3]
        x = (
            (1.0 - t[i]) ** 3 * p0[0]
            + 3 * (1.0 - t[i]) ** 2 * t[i] * p1[0]
            + 3 * (1.0 - t[i]) * t[i] ** 2 * p2[0]
            + t[i] ** 3 * p3[0]
        )
        y = (
            (1.0 - t[i]) ** 3 * p0[1]
            + 3 * (1.0 - t[i]) ** 2 * t[i] * p1[1]
            + 3 * (1.0 - t[i]) * t[i] ** 2 * p2[1]
            + t[i] ** 3 * p3[1]
        )
        curve.append([x, y])
    return curve


def get_curve_control_points(knots):
    n = len(knots) - 1
    if n == 1:  # Bezier curve should be a straight line
        # 3P1 = 2K0 + K3
        first_ctrl_points = [
            (2 * knots[0][0] + knots[1][0]) / 3,
            (2 * knots[0][1] + knots[1][1]) / 3,
        ]
        # P2 = 2P1 – K0
        second_ctrl_points = [
            2 * first_ctrl_points[0] - knots[0][0],
            2 * first_ctrl_points[1] - knots[0][1],
        ]
        return [first_ctrl_points], [second_ctrl_points]

    # calculate first Bezier control points
    # right hand side vector
    rhs = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)

    # set right hand side X values
    for i in range(1, n - 1):
        rhs[i] = 4 * knots[i][0] + 2 * knots[i + 1][0]
    rhs[0] = knots[0][0] + 2 * knots[1][0]
    rhs[n - 1] = (8 * knots[n - 1][0] + knots[n][0]) / 2.0
    # get first control points X-values
    x = get_first_control_points(rhs)

    # set right hand side Y values
    for i in range(1, n - 1):
        rhs[i] = 4 * knots[i][1] + 2 * knots[i + 1][1]
    rhs[0] = knots[0][1] + 2 * knots[1][1]
    rhs[n - 1] = (8 * knots[n - 1][1] + knots[n][1]) / 2.0
    # get first control points Y-values
    y = get_first_control_points(rhs)

    # fill output arrays
    first_ctrl_points = []
    second_ctrl_points = []
    for i in range(n):
        # first control point
        first_ctrl_points.append([x[i], y[i]])
        # second control point
        if i < n - 1:
            second_ctrl_points.append(
                [2 * knots[i + 1][0] - x[i + 1], 2 * knots[i + 1][1] - y[i + 1]]
            )
        else:
            second_ctrl_points.append(
                [(knots[n][0] + x[n - 1]) / 2, (knots[n][1] + y[n - 1]) / 2]
            )

    return first_ctrl_points, second_ctrl_points


# Solves a tridiagonal system for one of coordinates (x or y)
# of first Bezier control points.
def get_first_control_points(rhs):
    n = len(rhs)
    x = np.zeros(n)  # solution vector
    tmp = np.zeros(n)

    b = 2.0
    x[0] = rhs[0] / b
    # decomposition and forward substitution
    for i in range(1, n):
        tmp[i] = 1 / b
        b = (4.0 if i < n - 1 else 3.5) - tmp[i]
        x[i] = (rhs[i] - x[i - 1]) / b
    # backsubstitution
    for i in range(1, n):
        x[n - i - 1] -= tmp[n - i] * x[n - i]

    return x


def get_bezier_spline_points(knots):
    first_ctrl_points, second_ctrl_points = get_curve_control_points(knots)
    ctrl_points = []
    spline_points = []
    for i in range(0, len(knots) - 1):
        curve_points = [
            knots[i],
            first_ctrl_points[i],
            second_ctrl_points[i],
            knots[i + 1],
        ]
        spline_points += bezier_curve(curve_points)
        ctrl_points += curve_points
    return spline_points, ctrl_points


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
points = []
ctrl_points = []
spline_points = []

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                points.append(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if len(points) > 1:
                    spline_points, ctrl_points = get_bezier_spline_points(points)
                    break
    screen.fill(WHITE)
    if ctrl_points:
        pygame.draw.aalines(screen, GRAY, False, ctrl_points)
        for point in ctrl_points:
            pygame.draw.circle(screen, GRAY, point, 5, 1)

    for point in points:
        pygame.draw.circle(screen, RED, point, 3)

    for point in spline_points:
        pygame.draw.circle(screen, BLACK, point, 1)

    pygame.display.flip()
    clock.tick(30)
