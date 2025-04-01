import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Cell and screen settings
CELL_SIZE = 20
CELL_WIDTH = 30
CELL_HEIGHT = 20
WIDTH = CELL_WIDTH * CELL_SIZE
HEIGHT = CELL_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY  = (100, 100, 100)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game with Levels')

# Fonts
font = pygame.font.SysFont('Verdana', 20)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Wall positions
walls = []

def generate_walls(level):
    """Generate walls depending on the current level."""
    walls.clear()
    if level >= 2:
        for x in range(10, 20):
            walls.append((x, 10))
    if level >= 3:
        for y in range(5, 15):
            walls.append((15, y))

# Snake class
class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT
        self.grow_flag = False

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.append(new_head)
        if not self.grow_flag:
            self.body.pop(0)
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def check_collision(self):
        head = self.body[-1]
        # Check wall boundaries
        if head[0] < 0 or head[0] >= CELL_WIDTH or head[1] < 0 or head[1] >= CELL_HEIGHT:
            return True
        # Check collision with itself
        if head in self.body[:-1]:
            return True
        # Check collision with wall
        if head in walls:
            return True
        return False

# Food class
class Food:
    def __init__(self, snake):
        self.position = (0, 0)
        self.generate(snake)

    def generate(self, snake):
        """Generate food not on walls or the snake body."""
        while True:
            x = random.randint(0, CELL_WIDTH - 1)
            y = random.randint(0, CELL_HEIGHT - 1)
            if (x, y) not in snake.body and (x, y) not in walls:
                self.position = (x, y)
                break

# Main game loop
def game_loop():
    snake = Snake()
    food = Food(snake)
    clock = pygame.time.Clock()
    score = 0
    level = 1
    speed = 5

    generate_walls(level)

    running = True
    while running:
        clock.tick(speed)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != DOWN:
            snake.direction = UP
        elif keys[pygame.K_DOWN] and snake.direction != UP:
            snake.direction = DOWN
        elif keys[pygame.K_LEFT] and snake.direction != RIGHT:
            snake.direction = LEFT
        elif keys[pygame.K_RIGHT] and snake.direction != LEFT:
            snake.direction = RIGHT

        # Move the snake
        snake.move()

        # Check for game over
        if snake.check_collision():
            print("Game Over! Score:", score)
            running = False

        # Check if food is eaten
        if snake.body[-1] == food.position:
            snake.grow()
            score += 1
            food.generate(snake)

            # Increase level and speed
            if score % 4 == 0:
                level += 1
                speed += 2
                generate_walls(level)

        # Draw background
        screen.fill(BLACK)

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, GRAY, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw snake
        for block in snake.body:
            pygame.draw.rect(screen, GREEN, (block[0]*CELL_SIZE, block[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, (food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw score and level
        score_text = font.render(f'Score: {score}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 120, 10))

        pygame.display.flip()

# Start the game
game_loop()
