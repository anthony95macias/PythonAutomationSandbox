import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define a function to check if two points are adjacent
def is_adjacent(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

# Define a function to perform Breadth-First Search
def bfs(start, goal, obstacles):
    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        visited.add(current)

        if current == goal:
            return path

        for neighbor in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]:
            if (
                neighbor not in visited
                and neighbor not in obstacles
                and 0 <= neighbor[0] < GRID_WIDTH
                and 0 <= neighbor[1] < GRID_HEIGHT
            ):
                queue.append((neighbor, path + [neighbor]))

    return None

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - BFS Agent")

# Snake initial position and direction
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (0, 1)  # Initial direction: down

# Food initial position
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game over flag
game_over = False

# Score counter
score = 0

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate the next move using BFS
    path = bfs(snake[0], food, snake[1:])

    if path:
        next_step = path[0]
        if next_step[0] > snake[0][0]:
            direction = (1, 0)  # Move right
        elif next_step[0] < snake[0][0]:
            direction = (-1, 0)  # Move left
        elif next_step[1] > snake[0][1]:
            direction = (0, 1)  # Move down
        else:
            direction = (0, -1)  # Move up

    # Move the snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check for collisions with food
    if snake[0] == food:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 1

    # Check for collisions with the wall or itself
    if (
        snake[0][0] < 0
        or snake[0][0] >= GRID_WIDTH
        or snake[0][1] < 0
        or snake[0][1] >= GRID_HEIGHT
        or snake[0] in snake[1:]
    ):
        game_over = True

    # Clear the screen
    screen.fill(WHITE)

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the food
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(SNAKE_SPEED)

# Print the final score
print(f"Final Score: {score}")

# Quit Pygame
pygame.quit()

