import pygame
import math
from pygame.locals import *
import random

# Initialize pygame
pygame.display.init()
pygame.font.init()

# Window dimensions
width = 1600
height = 1200

background_color = (30, 30, 30)
primary = (255, 127, 80)
secondary = (100, 149, 237)
highlight = (235, 140, 102)
line_color = (200, 200, 200)

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

# Calculate distance
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def distances(points):
    dim = len(points)
    result = [[None for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            result[i][j] = distance(points[i], points[j])
    return result

# Nearest neighbor heuristic
def get_initial_solution(points):
    visited = [False for i in range(len(points))]
    tour = [0]
    dists = distances(points)
    current = 0
    while len(tour) < len(points):
        lowest_distance = 99999999
        nearest_neighbor = None
        for i in range(len(points)):
            if i not in tour:
                distance_from_current_to_i = dists[current][i]
                if distance_from_current_to_i < lowest_distance:
                    nearest_neighbor = i
                    lowest_distance = distance_from_current_to_i
        tour.append(nearest_neighbor)
        current = nearest_neighbor
    tour.append(0)
    return tour

def find_improvement(atour):
    improvements = [[None for _ in range(len(atour)-1)] for _ in range(len(atour)-1)]
    for i in range(len(atour)-3):
        for j in range(i+2, len(atour)-1):
            p1 = points[atour[i]]
            p2 = points[atour[i+1]]
            p3 = points[atour[j]]
            p4 = points[atour[j+1]]
            # instead of p1-p2 and later p3-p4, we go p1-p3 and later p2-p4
            delta = -distance(p1,p2)-distance(p3,p4)+distance(p1,p3)+distance(p2,p4)
            improvements[i][j] = delta
    # find most negative value
    best_index = None
    best_delta = -0.000000001
    for i in range(len(atour)-3):
        for j in range(i+2, len(atour)-1):
            delta = improvements[i][j]
            if delta is not None:
                if delta < best_delta:
                    best_delta = delta
                    best_index = (i, j)
    return best_index

def calculate_swaps(atour):
    newtour = atour[:]
    best_index = find_improvement(newtour)
    swaps = []
    while best_index is not None:
        swaps.append(best_index)
        newtour[best_index[0]+1:best_index[1]+1] = newtour[best_index[0]+1:best_index[1]+1][::-1]
        best_index = find_improvement(newtour)
    return swaps

def perform_swap(tour, swaps, index):
    best_index = swaps[index] 
    tour[best_index[0]+1:best_index[1]+1] = tour[best_index[0]+1:best_index[1]+1][::-1]

def calculate_tour_distance(tour):
    total = 0
    for i in range(len(tour)-1):
        total += distance(points[tour[i]], points[tour[i+1]])
    return total

# Use the nearest neighbor heuristic to find an initial solution
tour = get_initial_solution(points)

# Find improvements
swaps = calculate_swaps(tour)

# Calculate the distance of the initial tour
current_distance = calculate_tour_distance(tour)

# Circle radius
radius = 7
current_circle_radius = 0
max_radius = 20

# Main game loop
running = True
step = 0
swap_step = 0

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
                if step < len(tour)-1:
                    step += 1
                    current_circle_radius = 0
                elif swap_step < len(swaps):
                    perform_swap(tour, swaps, swap_step)
                    swap_step += 1
                    current_distance = calculate_tour_distance(tour)
            if event.key == K_LEFT:
                if swap_step > 0:
                    swap_step -= 1
                    perform_swap(tour, swaps, swap_step)
                    current_distance = calculate_tour_distance(tour)
                elif step > 0:
                    step -= 1
                    current_circle_radius = 0
    # Draw text
    if step == len(tour)-1:
        text_surface = font.render(f"Distance: {current_distance:.2f}", True, (255, 255, 255))
        window.blit(text_surface, (10, 10))

    # Draw the tour
    for i in range(step):
        pygame.draw.line(window, line_color, points[tour[i]], points[tour[i+1]], 3)  # 5 is the line thickness

    # Draw the points as circles
    for i in range(len(points)):
        point = points[i]
        if i in tour[:step+1]:
            pygame.draw.circle(window, primary, point, radius)
        elif i == tour[step+1] and current_circle_radius == max_radius:
            pygame.draw.circle(window, highlight, point, radius)
        else: 
            pygame.draw.circle(window, secondary, point, radius)

    # Draw an expanding circle around the current point
    if swap_step == 0:
        circle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if step < len(tour)-1:
            max_radius = distance(points[tour[step]], points[tour[step+1]])
        if current_circle_radius < max_radius:
            current_circle_radius += 8
            if current_circle_radius > max_radius:
                current_circle_radius = max_radius
        if step < len(tour)-1:
            pygame.draw.circle(circle_surface, (230, 230, 230, 50), points[tour[step]], current_circle_radius)
            window.blit(circle_surface, (0, 0))

    # Update the display
    pygame.display.flip()

    pygame.time.wait(30)
# Quit pygame
pygame.quit()
