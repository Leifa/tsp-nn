import pygame
import math
from pygame.locals import *
import random
from instance import Instance
from nearest_neighbor import NearestNeighbor 
from twoopt import TwoOpt

# Initialize pygame
pygame.display.init()
pygame.font.init()

# Window dimensions
width = 1800
height = 1200

background_color = (30, 30, 30)
primary = (255, 127, 80)
secondary = (100, 149, 237)
highlight = (235, 140, 102)
line_color = (200, 200, 200)
NEIGHBOR_CIRCLE_COLOR = (230, 230, 230, 50)
# Create the window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Travelling Salesman Problem")

font = pygame.font.Font(None, 30)

# List of points
points = []
for i in range(50):
    point = (random.randint(100, width-100), random.randint(100, height-100))
    points.append(point)
#points = [(110, 120), (400, 510), (600, 550), (900, 600), (630, 42)]

instance = Instance(points)

phase = 0
nearest_neighbor = NearestNeighbor(instance)
tour = nearest_neighbor.get_tour()
twoopt = None

# Circle radius
radius = 6
current_circle_radius = 0
max_radius = 20

# Main game loop
running = True

while running:
    # Clear the screen
    window.fill(background_color)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RIGHT:
                if phase == 0:
                    nearest_neighbor.step()
                    current_circle_radius = 0
                    if nearest_neighbor.is_done():
                        phase = 1
                        twoopt = TwoOpt(instance, tour)
                elif phase == 1:
                    twoopt.step()
                    if twoopt.is_done():
                        phase = 2
            if event.key == K_LEFT:
                if phase == 2:
                    phase = 1
                if phase == 1:
                    if not twoopt.unstep():
                        phase = 0
                if phase == 0:
                    nearest_neighbor.unstep()
                    current_circle_radius = 0

    # Draw text
    if phase >= 1:
        current_distance = instance.get_tour_distance(tour)
        text_surface = font.render(f"Distance: {current_distance:.2f}", True, (255, 255, 255))
        window.blit(text_surface, (10, 10))

    # Draw the tour
    for i in range(len(tour)-2):
        pygame.draw.line(window, line_color, points[tour[i]], points[tour[i+1]], 2) 
    if len(tour) > 1 and current_circle_radius == max_radius:
        pygame.draw.line(window, line_color, points[tour[-2]], points[tour[-1]], 2) 
    if len(tour) == len(points)+1:
        pygame.draw.line(window, line_color, points[tour[-2]], points[tour[-1]], 2) 

    # Draw the points as circles
    for i in range(len(points)):
        point = points[i]
        if i in tour[:-1]:
            pygame.draw.circle(window, primary, point, radius)
        elif i == tour[-1] and current_circle_radius == max_radius:
            pygame.draw.circle(window, primary, point, radius)
        elif i == tour[0]:
            pygame.draw.circle(window, primary, point, radius)
        else: 
            pygame.draw.circle(window, secondary, point, radius)

    # Draw an expanding circle around the current point
    if phase == 0 and len(tour) > 1:
        circle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if len(tour) < len(points)+1:
            max_radius = instance.get_dist(tour[-2], tour[-1])
        if current_circle_radius < max_radius:
            current_circle_radius += 5
            if current_circle_radius > max_radius:
                current_circle_radius = max_radius
        pygame.draw.circle(circle_surface, NEIGHBOR_CIRCLE_COLOR , points[tour[-2]], current_circle_radius)
        window.blit(circle_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    pygame.time.wait(20)
# Quit pygame
pygame.quit()
