import pygame
import random
import math
import time
from attractor import Attractor
import numpy as np


class AllGhost():
    def __init__(self, screen="", window_size=(0, 0), attractor=Attractor(), max_ghosts=5):
        self.screen = screen
        self.window_size = window_size
        self.attractor = attractor
        self.ghosts = []
        self.dying_ghosts = []
        self.max_ghosts = max_ghosts

    def add_ghost(self, img="",img_path="", size=50, speed=0.2):
        ghost = Ghost(AllGhost=self, img=img, img_path=img_path, size=size, speed=speed)
        self.ghosts.append(ghost)

        if len(self.ghosts) > self.max_ghosts:
            self.ghosts[0].status = "dying"
            self.dying_ghosts.append(self.ghosts.pop(0))

    def runall(self):
        for ghost in self.ghosts:
            ghost.run()
            
        for dying_ghost in self.dying_ghosts:
            if dying_ghost.dead:
                self.dying_ghosts.remove(dying_ghost)
            dying_ghost.run()


class Ghost():
    def __init__(self, AllGhost, img="", img_path="", size=50, speed=5):
        self.screen = AllGhost.screen
        self.window_width, self.window_height = AllGhost.window_size
        self.attractor = AllGhost.attractor

        if isinstance(img, np.ndarray):
            shape = img.shape
            surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
            pygame.pixelcopy.array_to_surface(surface, img[:,:,0:3])
            surface_alpha = np.array(surface.get_view('A'), copy=False)
            surface_alpha[:,:] = img[:,:,3]
            self.original_image = pygame.transform.scale(
                surface, (size, size))
        else:
            self.original_image = pygame.transform.scale(
                pygame.image.load(img_path), (size, size))

        self.flip_image = pygame.transform.flip(
            self.original_image, True, False)
        self.show_image = self.original_image.copy()

        self.size = size

        # Set spawn point
        self.spawn_point = (10,10)
        # Set dying point
        self.dying_point = (950,530)
        self.dead = False

        # Rect = show coord
        self.rect = self.original_image.get_rect()
        self.rect.x, self.rect.y = self.spawn_point

        # Coord = Real coord
        self.coord = [self.rect.x, self.rect.y]

        self.speed = speed
        self.goal_point = (0, 0)
        self.generate_new_goal()

        self.wobble_x = random.uniform(0, 6.28)
        self.wobble_offset = 0.002 * 100
        self.wobble_range = 8

        # Status : "move_to_goal", "pause", "follow", "dying"
        self.status = "move_to_goal"
        self.status_counter = 0
        self.last_change_time = time.time()

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
        self.goal_point = (random.randint(self.rect.width // 2, self.window_width - self.rect.width // 2),
                           random.randint(self.rect.height // 2, self.window_height - self.rect.height // 2))
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
            elif self.status == "dying":
                self.dead = True

    def wobble(self):
        self.coord_to_rect()
        self.wobble_x += self.wobble_offset
        self.rect.y = self.coord[1] + \
            math.sin(self.wobble_x) * self.wobble_range

    def move(self):
        if self.status == "dying":
            self.goal_point = self.dying_point
            self.move_towards_goal()
            self.detect_change_dir()


        elif self.attractor.is_active:
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

        self.wobble()

        self.status_counter += 1

    def draw(self):
        self.screen.blit(self.show_image, (self.rect.x -
                         self.size//2, self.rect.y - self.size//2))

    def draw_goal_point(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.goal_point, 5)


class ShowGhost():
    def __init__(self, screen, window_size, img="", img_path="", size=50, speed=5):
        self.screen = screen
        self.window_width, self.window_height = window_size
        # self.attractor = AllGhost.attractor

        if isinstance(img, np.ndarray):
            shape = img.shape
            surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
            pygame.pixelcopy.array_to_surface(surface, img[:,:,0:3])
            surface_alpha = np.array(surface.get_view('A'), copy=False)
            surface_alpha[:,:] = img[:,:,3]
            self.original_image = surface
        else:
            self.original_image = pygame.image.load(img_path)

        self.show_image = pygame.transform.scale(
                self.original_image, (size, size))
        self.is_flip = False

        self.size = size

        self.speed = speed
        self.goal_points = [(153,120), (84, 203), (151, 300) ,(224, 206)]
        self.goal_point = self.goal_points[0]


        # Rect = show coord
        self.rect = self.original_image.get_rect()
        self.rect.x, self.rect.y = self.goal_point

        # Coord = Real coord
        self.coord = [self.rect.x, self.rect.y]

        self.wobble_x = random.uniform(0, 6.28)
        self.wobble_offset = 0.002 * 100
        self.wobble_range = 8

        # Status : "move_to_goal", "pause", "waiting"
        self.status = "move_to_goal"
        self.status_counter = 0
        self.last_change_time = time.time()

        self.pause_time = 1

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
            self.is_flip = True
            self.show_image = pygame.transform.flip(pygame.transform.scale(self.original_image, (self.size, self.size)), True, False)
            # print("flip")
        elif dx < 0:
            self.is_flip = False
            self.show_image = pygame.transform.scale(self.original_image, (self.size, self.size))
            # print("no flip")

    def next_goal(self):
        self.goal_point = self.goal_points[0]
        # Cycle goal_points
        self.goal_points = self.goal_points[1:] + [self.goal_points[0]]

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
            elif self.status == "dying":
                self.dead = True

    def wobble(self):
        self.coord_to_rect()
        self.wobble_x += self.wobble_offset
        self.rect.y = self.coord[1] + \
            math.sin(self.wobble_x) * self.wobble_range

    def move(self):
        if self.status == "move_to_goal":
            self.move_towards_goal()

        elif self.status == "pause":
            # Pause
            if time.time() - self.last_change_time > self.pause_time:
                self.next_goal()
                self.change_status("move_to_goal")

        self.wobble()
        self.status_counter += 1

    def draw(self):
        self.screen.blit(self.show_image, (self.rect.x -
                         self.size//2, self.rect.y - self.size//2))

    def draw_goal_point(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.goal_point, 5)


    def change_size(self, new_size):
        self.size = new_size
        # self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        if self.is_flip:
            self.show_image = pygame.transform.flip(pygame.transform.scale(self.original_image, (self.size, self.size)), True, False)
            # print("flip")
            
        else:
            self.show_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        # self.flip_image = pygame.transform.flip(
        #     self.show_image, True, False)

    def change_speed(self, new_speed):
        self.speed = new_speed

    def flip_image(self, axis=0):
        if axis==0:
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif axis==1:
            self.original_image = pygame.transform.flip(self.original_image, False, True)

        self.detect_change_dir()

    def change_image(self, new_path):
        self.original_image = pygame.image.load(new_path)
        self.detect_change_dir()

    def change_image_from_array(self, img):
        shape = img.shape
        surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
        pygame.pixelcopy.array_to_surface(surface, img[:,:,0:3])
        surface_alpha = np.array(surface.get_view('A'), copy=False)
        surface_alpha[:,:] = img[:,:,3]
        self.original_image = surface
        self.detect_change_dir()


