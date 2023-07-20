import pygame
import math
from pygame.locals import *
import random
from algo import *

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
for i in range(130):
    point = (random.randint(100, width-100), random.randint(100, height-100))
    points.append(point)
#points = [(110, 120), (400, 510), (600, 550), (900, 600), (630, 42)]

algo = Algo(points)

# Circle radius
radius = 8
current_circle_radius = 0
max_radius = 20

# Main game loop
running = True

while running:
    # Clear the screen
    window.fill(background_color)
#    algo.step()
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RIGHT:
                algo.step()
                current_circle_radius = 0
            if event.key == K_LEFT:
                algo.unstep()
                current_circle_radius = 0

    # Draw text
    if algo.phase == PHASE_IMPROVE or algo.phase == PHASE_DONE:
        current_distance = algo.get_tour_distance()
        text_surface = font.render(f"Distance: {current_distance:.2f}", True, (255, 255, 255))
        window.blit(text_surface, (10, 10))

    # Draw the tour
    tour = algo.tour 
    for i in range(len(tour)-2):
        pygame.draw.line(window, line_color, points[tour[i]], points[tour[i+1]], 3) 
    if len(tour) > 1 and current_circle_radius == max_radius:
        pygame.draw.line(window, line_color, points[tour[-2]], points[tour[-1]], 3) 
    if len(tour) == len(points)+1:
        pygame.draw.line(window, line_color, points[tour[-2]], points[tour[-1]], 3) 

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
    if algo.phase == PHASE_NEAREST_NEIGHBOR and len(tour) > 1:
        circle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if len(tour) < len(points)+1:
            max_radius = distance(points[tour[-2]], points[tour[-1]])
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
