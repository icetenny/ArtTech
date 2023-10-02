import pygame
import random
import math
import time
from attractor import Attractor


class AllGhost():
    def __init__(self, screen="", window_size=(0, 0), attractor=Attractor()):
        self.screen = screen
        self.window_size = window_size
        self.attractor = attractor
        self.ghosts = []

    def add_ghost(self, img="", size=50, speed=0.2):
        ghost = Ghost(AllGhost=self, img=img, size=size, speed=speed)
        self.ghosts.append(ghost)

    def runall(self):
        for ghost in self.ghosts:
            ghost.run()


class Ghost():
    def __init__(self, AllGhost=AllGhost(), img="", size=50, speed=0.2):
        self.screen = AllGhost.screen
        self.window_width, self.window_height = AllGhost.window_size
        self.attractor = AllGhost.attractor

        self.original_image = pygame.transform.scale(
            pygame.image.load(img), (size, size))
        self.flip_image = pygame.transform.flip(
            self.original_image, True, False)
        self.show_image = self.original_image.copy()
        self.size = size
        # Rect = show coord
        self.rect = self.original_image.get_rect()
        self.rect.x = random.randint(0, self.window_width - self.rect.width)
        self.rect.y = random.randint(0, self.window_height - self.rect.height)
        # Coord = Real coord
        self.coord = [self.rect.x, self.rect.y]

        self.speed = speed
        self.goal_point = (0, 0)
        self.generate_new_goal()

        self.wobble_x = random.uniform(0, 6.28)
        self.wobble_offset = 0.002 * 100
        self.wobble_range = 8

        # Status : "move_to_goal", "pause", "follow"
        self.status = "move_to_goal"
        self.status_counter = 0
        self.last_change_time = time.time()

        self.direction = "+x"

        self.pause_time = 2

    def coord_to_rect(self):
        self.rect.x, self.rect.y = self.coord

    def run(self):
        self.move()
        # self.draw_goal_point()
        self.draw()
    def change_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.status_counter = 0
            self.last_change_time = time.time()

    def detect_change_dir(self):
        dx = self.goal_point[0] - self.coord[0]
        if dx > 0:
            self.show_image = self.flip_image
        elif dx < 0:
            self.show_image = self.original_image

    def generate_new_goal(self):
        self.goal_point = (random.randint(self.rect.width, self.window_width - self.rect.width),
                           random.randint(self.rect.height, self.window_height - self.rect.height))
        self.detect_change_dir()
        return self.goal_point

    def move_towards_goal(self):
        dx = self.goal_point[0] - self.coord[0]
        dy = self.goal_point[1] - self.coord[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            if distance < self.speed:
                self.coord[0] = self.goal_point[0]
                self.coord[1] = self.goal_point[1]
            else:
                self.coord[0] += dx * self.speed / distance
                self.coord[1] += dy * self.speed / distance
        else:
            # Goal Reached
            if self.status == "move_to_goal":
                self.change_status("pause")

    # def follow(self):
    #     dx = self.goal_point[0] - self.coord[0]
    #     dy = self.goal_point[1] - self.coord[1]
    #     distance = (dx ** 2 + dy ** 2) ** 0.5
    #     if distance > 30:
    #         self.coord[0] += dx * self.speed / distance
    #         self.coord[1] += dy * self.speed / distance

    #     self.detect_change_dir()

    def wobble(self):
        self.wobble_x += self.wobble_offset
        self.rect.y = self.coord[1] + \
            math.sin(self.wobble_x) * self.wobble_range

    def move(self):
        if self.attractor.is_active:
            self.change_status("follow")
            self.goal_point = self.attractor.pos
            self.move_towards_goal()
            self.detect_change_dir()

        elif not self.attractor.is_active and self.status == "follow":
            self.generate_new_goal()
            self.change_status("move_to_goal")

        elif self.status == "move_to_goal":
            self.move_towards_goal()

        elif self.status == "pause":
            # Pause
            if time.time() - self.last_change_time > self.pause_time:
                self.generate_new_goal()
                self.change_status("move_to_goal")

        self.coord_to_rect()
        self.wobble()

        self.status_counter += 1

    def draw(self):
        self.screen.blit(self.show_image, (self.rect.x - self.size//2, self.rect.y - self.size//2))

    def draw_goal_point(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.goal_point, 5)
