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

    def add_ghost(self, img="", img_path="", size=50, speed=0.2, effect=0):
        ghost = Ghost(AllGhost=self, img=img, img_path=img_path,
                      size=size, speed=speed, effect=effect)
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
    def __init__(self, AllGhost, img="", img_path="", size=50, speed=5, effect=0):
        self.screen = AllGhost.screen
        self.window_width, self.window_height = AllGhost.window_size
        self.attractor = AllGhost.attractor

        if isinstance(img, np.ndarray):
            shape = img.shape
            surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
            pygame.pixelcopy.array_to_surface(surface, img[:, :, 0:3])
            surface_alpha = np.array(surface.get_view('A'), copy=False)
            surface_alpha[:, :] = img[:, :, 3]
            self.original_image = pygame.transform.scale(
                surface, (size, size))
        else:
            self.original_image = pygame.transform.scale(
                pygame.image.load(img_path), (size, size))

        # self.flip_image = pygame.transform.flip(
        #     self.original_image, True, False)
        self.is_flipped = False
        self.show_image = self.original_image.copy()

        self.size = size

        # Set spawn point
        self.spawn_point = (0, self.window_height)
        # Set dying point
        self.dying_point = (self.window_width, self.window_height)
        self.dead = False

        # Rect = show coord
        self.rect = self.original_image.get_rect()
        self.rect.x, self.rect.y = self.spawn_point

        # Coord = Real coord
        self.coord = [self.rect.x, self.rect.y]

        self.speed = speed
        self.goal_point = (0, 0)
        self.generate_new_goal()

        # self.wobble_x = random.uniform(0, 6.28)
        # self.wobble_offset = 0.002 * 100
        # self.wobble_range = 8
        self.wobble_x = random.uniform(0, 6.28)
        self.wobble_offset = random.uniform(0.1, 0.4)
        self.wobble_range = random.uniform(4,10)

        # Status : "move_to_goal", "pause", "follow", "dying"
        self.status = "move_to_goal"
        self.status_counter = 0
        self.last_change_time = time.time()

        self.pause_time = random.uniform(2,4)

        self.effect = effect

        # Effect 1,2,3 : Trail
        self.trail_positions = []
        self.max_trail = 20

        # Effect 4 : Size wobble
        self.size_step = 0
        self.original_size = self.size
        self.wobble_ratio = 0.3

        # Effect 5 : Fading
        self.current_alpha = 255
        self.alpha_increasing = False
        self.alpha_step = 5

        # Effect 6 : Spinning

    def coord_to_rect(self):
        self.rect.x, self.rect.y = self.coord

    def run(self):
        self.move()
        # self.draw_goal_point()
        if self.effect == 1:
            self.trail_effect(color=(0, 0, 0), max_alpha=128)
        elif self.effect == 2:
            self.trail_effect(color=(200, 200, 200), max_alpha=128)
        elif self.effect == 3:
            self.trail_effect(color=(200, 0, 0), max_alpha=128)

        self.draw()

    def change_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.status_counter = 0
            self.last_change_time = time.time()

    def detect_change_dir(self):
        dx = self.goal_point[0] - self.coord[0]
        if dx > 0:
            self.is_flipped = True
            self.show_image = self.flip(self.original_image)
        elif dx < 0:
            self.is_flipped = False
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
        
    def size_wobble(self):
        self.size_step += 0.1
        self.size = self.original_size+ \
            math.sin(self.size_step) * (self.original_size * self.wobble_ratio)
        
        if self.is_flipped:
            self.show_image = self.scale(self.flip(self.original_image))
        else:
            self.show_image = self.scale(self.original_image)

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

        if self.effect in [1, 2, 3]:
            self.append_trail()
        elif self.effect == 4:
            self.size_wobble()
        # elif self.effect == 5:
        #     self.show_image = pygame.transform.rotate(self.show_image, 2)

        self.status_counter += 1

    def draw(self):
        if self.effect == 5:
            showing_image = self.show_image.copy()
            showing_image.set_alpha(self.current_alpha)
            self.screen.blit(showing_image, (self.rect.x -
                            self.size//2, self.rect.y - self.size//2))
            if self.alpha_increasing:
                self.current_alpha += self.alpha_step
                if self.current_alpha >= 255:
                    self.alpha_increasing = False
            else:
                self.current_alpha -= self.alpha_step
                if self.current_alpha <= 0:
                    self.alpha_increasing = True
        else:
            self.screen.blit(self.show_image, (self.rect.x -
                            self.size//2, self.rect.y - self.size//2))


    def draw_goal_point(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.goal_point, 5)

    def append_trail(self):
        self.trail_positions.append((self.rect.x, self.rect.y))
        if len(self.trail_positions) > self.max_trail:
            self.trail_positions.pop(0)

    def color_mask(self, color):
        mask_surface = self.show_image.copy()
        mask_surface.fill(color)
        surface_alpha = np.array(mask_surface.get_view('A'), copy=False)
        surface_alpha[:, :] = pygame.surfarray.array_alpha(self.show_image)
        return mask_surface

    def trail_effect(self, color=(0, 0, 0), max_alpha=255):
        mask = self.color_mask(color=color)
        for i, (x, y) in enumerate(self.trail_positions):
            alpha = int(max_alpha * (i / len(self.trail_positions)))

            # Scale the image based on the position in the trail
            scale_factor = (i / len(self.trail_positions))
            current_mask = pygame.transform.scale(mask, (int(self.show_image.get_width(
            ) * scale_factor), int(self.show_image.get_height() * scale_factor)))
            current_mask.set_alpha(alpha)

            image_rect = current_mask.get_rect()
            image_rect.center = (x, y)
            self.screen.blit(current_mask, image_rect)
    def scale(self, surface, size=0):
        if size == 0:
            return pygame.transform.scale(surface, (self.size, self.size))
        else:
            return pygame.transform.scale(surface, (size, size))
        
    def flip(self, surface):
        return pygame.transform.flip(
            surface, True, False)



class ShowGhost():
    def __init__(self, screen, window_size, img="", img_path="", size=50, speed=5, effect=0):
        self.screen = screen
        self.window_width, self.window_height = window_size
        # self.attractor = AllGhost.attractor

        if isinstance(img, np.ndarray):
            shape = img.shape
            surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
            pygame.pixelcopy.array_to_surface(surface, img[:, :, 0:3])
            surface_alpha = np.array(surface.get_view('A'), copy=False)
            surface_alpha[:, :] = img[:, :, 3]
            self.original_image = surface
        else:
            self.original_image = pygame.image.load(img_path)

        self.show_image = pygame.transform.scale(
            self.original_image, (size, size))
        self.is_flip = False

        self.size = size

        self.speed = speed
        self.goal_points = [(153, 120), (84, 203), (151, 300), (224, 206)]
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

        self.effect = effect

        # Effect 1,2,3 : Trail
        self.trail_positions = []
        self.max_trail = 20

        # Effect 4 : Size wobble
        self.size_step = 0
        self.original_size = self.size
        self.wobble_ratio = 0.3

        # Effect 5 : Fading
        self.current_alpha = 255
        self.alpha_increasing = False
        self.alpha_step = 5

        # Effect 6 : Spinning


    def coord_to_rect(self):
        self.rect.x, self.rect.y = self.coord

    def run(self):
        self.move()
        # self.draw_goal_point()
        if self.effect == 1:
            self.trail_effect(color=(0, 0, 0), max_alpha=128)
        elif self.effect == 2:
            self.trail_effect(color=(200, 200, 200), max_alpha=128)
        elif self.effect == 3:
            self.trail_effect(color=(200, 0, 0), max_alpha=128)
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
            self.show_image = pygame.transform.flip(pygame.transform.scale(
                self.original_image, (self.size, self.size)), True, False)
            # print("flip")
        elif dx < 0:
            self.is_flip = False
            self.show_image = pygame.transform.scale(
                self.original_image, (self.size, self.size))
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
        
    def size_wobble(self):
        self.size_step += 0.1
        self.size = self.original_size + \
            math.sin(self.size_step) * (self.original_size * self.wobble_ratio)
        
        if self.is_flip:
            self.show_image = self.scale(self.flip(self.original_image))
        else:
            self.show_image = self.scale(self.original_image)

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

        if self.effect in [1, 2, 3]:
            self.append_trail()
        elif self.effect == 4:
            self.size_wobble()

    def draw(self):
        if self.effect == 5:
            showing_image = self.show_image.copy()
            showing_image.set_alpha(self.current_alpha)
            self.screen.blit(showing_image, (self.rect.x -
                            self.size//2, self.rect.y - self.size//2))
            if self.alpha_increasing:
                self.current_alpha += self.alpha_step
                if self.current_alpha >= 255:
                    self.alpha_increasing = False
            else:
                self.current_alpha -= self.alpha_step
                if self.current_alpha <= 0:
                    self.alpha_increasing = True
        else:
            self.screen.blit(self.show_image, (self.rect.x -
                            self.size//2, self.rect.y - self.size//2))

    def draw_goal_point(self):
        pygame.draw.circle(self.screen, (0, 0, 255), self.goal_point, 5)

    def change_size(self, new_size):
        self.size = new_size
        self.original_size = new_size
        # self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        if self.is_flip:
            self.show_image = pygame.transform.flip(pygame.transform.scale(
                self.original_image, (self.size, self.size)), True, False)
            # print("flip")

        else:
            self.show_image = pygame.transform.scale(
                self.original_image, (self.size, self.size))
        # self.flip_image = pygame.transform.flip(
        #     self.show_image, True, False)

    def change_speed(self, new_speed):
        self.speed = new_speed

    def flip_image(self, axis=0):
        if axis == 0:
            self.original_image = pygame.transform.flip(
                self.original_image, True, False)
        elif axis == 1:
            self.original_image = pygame.transform.flip(
                self.original_image, False, True)

        self.detect_change_dir()
    
    def rotate_image(self):
        self.original_image = pygame.transform.rotate(self.original_image, 270)

    def change_image(self, new_path):
        self.original_image = pygame.image.load(new_path)
        self.detect_change_dir()

    def change_image_from_array(self, img):
        shape = img.shape
        surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)
        pygame.pixelcopy.array_to_surface(surface, img[:, :, 0:3])
        surface_alpha = np.array(surface.get_view('A'), copy=False)
        surface_alpha[:, :] = img[:, :, 3]
        self.original_image = surface
        self.detect_change_dir()

    def append_trail(self):
        self.trail_positions.append((self.rect.x, self.rect.y))
        if len(self.trail_positions) > self.max_trail:
            self.trail_positions.pop(0)

    def color_mask(self, color):
        mask_surface = self.show_image.copy()
        mask_surface.fill(color)
        surface_alpha = np.array(mask_surface.get_view('A'), copy=False)
        surface_alpha[:, :] = pygame.surfarray.array_alpha(self.show_image)
        return mask_surface

    def trail_effect(self, color=(0, 0, 0), max_alpha=255):
        mask = self.color_mask(color=color)
        for i, (x, y) in enumerate(self.trail_positions):
            alpha = int(max_alpha * (i / len(self.trail_positions)))

            # Scale the image based on the position in the trail
            scale_factor = (i / len(self.trail_positions))
            current_mask = pygame.transform.scale(mask, (int(self.show_image.get_width(
            ) * scale_factor), int(self.show_image.get_height() * scale_factor)))
            current_mask.set_alpha(alpha)

            image_rect = current_mask.get_rect()
            image_rect.center = (x, y)
            self.screen.blit(current_mask, image_rect)
    def scale(self, surface, size=0):
        if size == 0:
            return pygame.transform.scale(surface, (self.size, self.size))
        else:
            return pygame.transform.scale(surface, (size, size))
        
    def flip(self, surface):
        return pygame.transform.flip(
            surface, True, False)
    
    def re_effect(self):
        self.trail_positions = []
        self.size_step = 0
