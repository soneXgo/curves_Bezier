import matplotlib.pyplot as plt
import numpy as np

def bezier_curve(points):
    curve = []
    for i in range(0, 10000 + 1, 1):
        t = i/10000.0
        p0 = points[0]
        p1 = points[1]
        p2 = points[2]
        p3 = points[3]
        x = (1.0-t)**3*p0[0] + 3*(1.0-t)**2*t*p1[0] + 3*(1.0-t)*t**2*p2[0] + t**3*p3[0]
        y = (1.0-t)**3*p0[1] + 3*(1.0-t)**2*t*p1[1] + 3*(1.0-t)*t**2*p2[1] + t**3*p3[1]
        curve.append([x, y])
    return curve

# def bezier_curve(control_points, num_points=100):
#     n = len(control_points)
#     t = np.linspace(0, 1, num_points)
#     curve_points = []
#     for i in range(num_points):
#         x = 0
#         y = 0
#         for j in range(n):
#             blend = np.math.factorial(n-1) / (np.math.factorial(j) * np.math.factorial(n-1-j)) * ((1-t[i])**(n-1-j)) * (t[i]**j)
#             x += blend * control_points[j][0]
#             y += blend * control_points[j][1]
#         curve_points.append([x, y])
#     return curve_points

def get_curve_control_points(knots):
    n = len(knots) - 1
    if n == 1:  #Special case: Bezier curve should be a straight line.
        first_control_points = [(2 * knots[0][0] + knots[1][0]) / 3, (2 * knots[0][1] + knots[1][1]) / 3]
        second_control_points = [2 * first_control_points[0] - knots[0][0], 2 * first_control_points[1] - knots[0][1]]
        return [first_control_points], [second_control_points]

    # Calculate first Bezier control points
	# Right hand side vector
    rhs = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)

    # Set right hand side X values
    for i in range(1, n-1):
        rhs[i] = 4 * knots[i][0] + 2 * knots[i + 1][0]
    rhs[0] = knots[0][0] + 2 * knots[1][0]
    rhs[n-1] = (8 * knots[n-1][0] + knots[n][0]) / 2.0
    x = get_first_control_points(rhs)

    # Set right hand side Y values
    for i in range(1, n-1):
        rhs[i] = 4 * knots[i][1] + 2 * knots[i + 1][1]
    rhs[0] = knots[0][1] + 2 * knots[1][1]
    rhs[n-1] = (8 * knots[n-1][1] + knots[n][1]) / 2.0
    y = get_first_control_points(rhs)

    first_control_points = []
    second_control_points = []
    for i in range(n):
        first_control_points.append([x[i], y[i]])
        if (i < n - 1):
            second_control_points.append([2 * knots[i+1][0] - x[i+1], 2 * knots[i+1][1] - y[i+1]])
        else:
            second_control_points.append([(knots[n][0] + x[n-1]) / 2, (knots[n][1] + y[n-1]) / 2])
            
    return first_control_points, second_control_points

def get_first_control_points(rhs):
    n = len(rhs)
    x = np.zeros(n) # Solution vector
    tmp = np.zeros(n) # Temp workspace

    b = 2.0
    x[0] = rhs[0] / b
    for i in range(1, n): # Decomposition and forward substitution
        tmp[i] = 1 / b
        b = (4.0 if i < n - 1 else 3.5) - tmp[i]
        x[i] = (rhs[i] - x[i - 1]) / b
    for i in range(1, n):
        x[n - i - 1] -= tmp[n - i] * x[n - i]  # Backsubstitution

    return x

# Пример данных точек
# knots = [[0, 0], [2, 1], [4, 4], [7, 7], [10,4], [12,1], [14, 0]]
knots = [[0, 0], [1, 3], [2, 1],[3,2]]

first_control_points, second_control_points = get_curve_control_points(knots)
c_points =[]
cur_points=[]
for i in range(0, len(knots)-1):
    control_points = [knots[i],first_control_points[i], second_control_points[i], knots[i+1]]
    cur_points += bezier_curve(control_points)
    c_points +=control_points


plt.figure()
plt.plot([point[0] for point in cur_points], [point[1] for point in cur_points], 'b-', label='Bezier Curve')
plt.plot([point[0] for point in c_points], [point[1] for point in c_points], 'ro-', label='Control Points')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Bezier Spline')
plt.legend()
plt.grid()
plt.show()

