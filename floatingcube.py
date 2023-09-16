import pygame
import random
import math
import time
# Initialize Pygame
pygame.init()

# Constants for the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BACKGROUND = (0, 0, 0)

class Ghost:
    def __init__(self, img="", size=50, speed=0.2):
        self.original_image = pygame.transform.scale(pygame.image.load(img), (size, size))
        self.show_image = self.original_image.copy()
        self.size = size 
        self.rect = self.original_image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
        self.coord = [self.rect.x, self.rect.y]

        self.speed = speed
        self.goal_point = self.generate_random_goal()

        self.wobble_x = random.uniform(0,6.28)
        self.wobble_offset = 0.002
        self.wobble_range = 8

        self.status = "move_to_goal"
        self.status_counter = 0
        self.last_change_time = time.time()

        self.pause_time = 2

    def run(self, screen):
        self.move()
        self.draw_goal_point(screen)
        self.draw(screen)
    
    def change_status(self, new_status):
        self.status = new_status
        self.status_counter = 0
        self.last_change_time = time.time()
        
    def generate_random_goal(self):
        new_goal = (random.randint(0, WINDOW_WIDTH - self.rect.width), random.randint(0, WINDOW_HEIGHT - self.rect.height))

        dx = new_goal[0] - self.rect.x
        if dx > 0:
            self.show_image = pygame.transform.flip(self.original_image, True, False)  # Flip the image horizontally
        else:
            self.show_image = self.original_image

        return new_goal

    def move_towards_goal(self):
        dx = self.goal_point[0] - self.rect.x
        dy = self.goal_point[1] - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            if distance < self.speed:
                self.rect.x = self.goal_point[0]
                self.rect.y = self.goal_point[1]
                self.goal_point = self.generate_random_goal()
            else:
                self.coord[0] += dx * self.speed / distance
                self.coord[1] += dy * self.speed / distance
                self.rect.x, self.rect.y = self.coord
        else:
            # Goal Reached
            self.change_status("pause")

    def wobble(self):
        self.wobble_x += self.wobble_offset
        self.rect.y = self.coord[1] + math.sin(self.wobble_x) * self.wobble_range

    def move(self):
        if self.status == "move_to_goal":
            self.move_towards_goal()
        elif self.status == "pause":
            # Pause
            if time.time() - self.last_change_time > self.pause_time:
                self.goal_point = self.generate_random_goal()
                self.change_status("move_to_goal")

        self.wobble()

        self.status_counter += 1

        # Check boundaries and bounce the ghost if it hits the edge
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH or self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.goal_point = self.generate_random_goal()

    def draw(self, screen):
        screen.blit(self.show_image, self.rect)
    
    def draw_goal_point(self, screen):
        pygame.draw.circle(screen, (0,0,255), self.goal_point, 5)

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Floating Ghosts")

# Create a list of ghosts
g1 = Ghost(img="pic/ghost1.png", size=80, speed=0.05)
g2 = Ghost(img="pic/ghost2-1.png", size=60, speed=0.035)
# g1 = Ghost(img="pic/ghost1.png", size=80, speed=1)
# g2 = Ghost(img="pic/ghost2-1.png", size=60, speed=1)
ghosts = [g1, g2]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BACKGROUND)

    # Move and draw each ghost
    for ghost in ghosts:
        ghost.run(screen)
        # print(ghost.goal_point, ghost.rect.x, ghost.rect.y)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
