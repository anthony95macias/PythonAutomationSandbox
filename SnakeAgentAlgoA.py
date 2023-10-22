import pygame
import sys
import random
import heapq

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SNAKE_SPEED = 10
NUM_AGENTS = 5  # Number of AI agents

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define a function to calculate the Manhattan distance between two points
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Define a function to find the path using A* search
def find_path(start, goal, obstacles):
    open_list = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        for neighbor in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]:
            if neighbor not in obstacles and 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    # Adjust the heuristic function based on your experimentation
                    h_score = manhattan_distance(neighbor, goal)
                    f_score = tentative_g_score + h_score
                    heapq.heappush(open_list, (f_score, neighbor))

    return None

# Define a function to move the AI snake using A* search
def move_ai_snake(snake, food):
    path = find_path(snake[0], food, snake[1:])
    if path:
        next_step = path[0]
        if next_step[0] > snake[0][0]:
            return (1, 0)  # Move right
        elif next_step[0] < snake[0][0]:
            return (-1, 0)  # Move left
        elif next_step[1] > snake[0][1]:
            return (0, 1)  # Move down
        else:
            return (0, -1)  # Move up
    else:
        # If no valid path found, move randomly
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

# Initialize a list to store accuracy rates and rankings
accuracy_rates = []

# Main game loop for each agent
for agent in range(NUM_AGENTS):
    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Snake Game - Agent {agent + 1}")

    # Snake initial position and direction
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (0, 1)  # Initial direction: down

    # Food initial position
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Game over flag
    game_over = False

    # Score and step counters
    score = 0
    steps = 0

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the AI snake
        ai_direction = move_ai_snake(snake, food)
        new_head = (snake[0][0] + ai_direction[0], snake[0][1] + ai_direction[1])
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

        # Increment step counter
        steps += 1

    # Calculate the accuracy rate for each agent
    accuracy_rate = score / steps if steps > 0 else 0
    accuracy_rates.append((agent + 1, accuracy_rate))

# Rank the agents based on their accuracy rates
ranked_agents = sorted(accuracy_rates, key=lambda x: x[1], reverse=True)
print("Agent Rankings:")
for rank, (agent, accuracy) in enumerate(ranked_agents, start=1):
    print(f"Rank {rank}: Agent {agent}, Accuracy Rate: {accuracy * 100:.2f}%")

# Print tuning recommendations based on rankings
if ranked_agents[0][1] > 0.08:
    print("Agent 1 is performing well. No significant changes needed.")
elif ranked_agents[0][1] > 0.06:
    print("Agent 1 shows good potential. Experiment with different heuristics and reward functions.")
elif ranked_agents[0][1] > 0.04:
    print("Agent 1 needs improvement. Focus on heuristic adjustments and more training data.")
else:
    print("Agent 1 has room for substantial improvement. Consider advanced algorithms and extensive training.")

# Quit Pygame
pygame.quit()
