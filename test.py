import matplotlib.pyplot as plt
import numpy as np

def de_casteljau(p0, p1, p2, p3, t):
    # Вычисляем промежуточные точки
    q0 = (1 - t) * p0 + t * p1
    q1 = (1 - t) * p1 + t * p2
    q2 = (1 - t) * p2 + t * p3
    
    r0 = (1 - t) * q0 + t * q1
    r1 = (1 - t) * q1 + t * q2
    
    # Итоговая точка на кривой Безье
    b = (1 - t) * r0 + t * r1
    
    return b

# Задаем 4 точки
p0 = np.array([0, 0])
p1 = np.array([1, 3])
p2 = np.array([2, -1])
p3 = np.array([3, 2])

# Создаем список точек на кривой Безье
points = []
for t in np.linspace(0, 1, 100):
    b = de_casteljau(p0, p1, p2, p3, t)
    points.append(b)

points = np.array(points)

# Рисуем кривую Безье и точки
plt.plot(points[:, 0], points[:, 1], label='Bezier Curve')
plt.scatter([p0[0], p1[0], p2[0], p3[0]], [p0[1], p1[1], p2[1], p3[1]], color='red', label='Control Points')
plt.legend()
plt.show()
