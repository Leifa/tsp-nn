import pygame
import math
from pygame.locals import *
import random
from mini import *

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
for i in range(10):
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

    # Draw text
    if algo.phase == PHASE_IMPROVE or algo.phase == PHASE_DONE:
        current_distance = algo.get_tour_distance()
        text_surface = font.render(f"Distance: {current_distance:.2f}", True, (255, 255, 255))
        window.blit(text_surface, (10, 10))

    # Draw the tour
    for (p, q) in algo.edges:
        pygame.draw.line(window, line_color, p, q, 3) 

    # Draw the points as circles
    for i in range(len(points)):
        point = points[i]
        pygame.draw.circle(window, secondary, point, radius)

    # Update the display
    pygame.display.flip()

    pygame.time.wait(20)
# Quit pygame
pygame.quit()
