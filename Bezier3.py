import pygame
import numpy as np

def draw_Bezier3(curve, points, num_points = 10000):
    t = np.linspace(0, 1, num_points)
    for i in range(num_points):
        p0 = points[0]
        p1 = points[1]
        p2 = points[2]
        p3 = points[3]
        x = (1.0-t[i])**3*p0[0] + 3*(1.0-t[i])**2*t[i]*p1[0] + 3*(1.0-t[i])*t[i]**2*p2[0] + t[i]**3*p3[0]
        y = (1.0-t[i])**3*p0[1] + 3*(1.0-t[i])**2*t[i]*p1[1] + 3*(1.0-t[i])*t[i]**2*p2[1] + t[i]**3*p3[1]
        curve.append([x, y])
    pygame.draw.lines(screen, BLACK, False, curve, 3)
    
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (180, 180, 180)
points = []
curve = []
curves = [] 
press = 0

pygame.init()
screen = pygame.display.set_mode((1000, 600))
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
        draw_Bezier3(curve, points)
        
    for crv in curves:
        pygame.draw.lines(screen, BLACK, False, crv, 3)

    pygame.display.flip()
    clock.tick(30)
