import pygame
import numpy as np

def de_casteljau(curve, points, t):
    if len(points) == 1:
        pygame.draw.circle(screen, BLACK, points[0], 2)
        curve.append(points[0])
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i+1][0]
            y = (1 - t) * points[i][1] + t * points[i+1][1]
            new_points.append((x, y))
        de_casteljau(curve, new_points, t)

def draw_de_casteljau(curve, points, num_points = 10000):
    t = np.linspace(0, 1, num_points)
    for i in range(num_points):
        de_casteljau(curve, points, t[i])


BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180, 180, 180)
points = []
ctrl_points = []
curve = []
curves = []
press = 0

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                points = []
                curve = []
                press = 0
            if event.key == pygame.K_a: 
                curves.append(curve)
                ctrl_points.append(points)
                points = [] 
                curve = [] 
                press = 0   
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if press == 0:
                    press = 1
                    points = [event.pos, event.pos, event.pos, event.pos]
                elif press == 1:
                    press = 2
                elif press == 2:
                    press = 3
                elif press == 3:
                    press = -1
        if event.type == pygame.MOUSEMOTION:
            if press == 1:
                points[3] = event.pos
            elif press == 2:
                points[2] = event.pos
            elif press == 3:
                points[1] = event.pos

    screen.fill(WHITE)
    if points:
        pygame.draw.aalines(screen, GRAY, False, points)
        for point in points:
            pygame.draw.circle(screen, GRAY, point, 5, 1)
        curve=[]
        draw_de_casteljau(curve, points)


    for ps in ctrl_points:
        pygame.draw.aalines(screen, GRAY, False, ps)
        for point in ps: 
            pygame.draw.circle(screen, GRAY, point, 5, 1)

    for crv in curves:
        for point in crv:
            pygame.draw.circle(screen, BLACK, point, 2)

    pygame.display.flip()
    clock.tick(30)

