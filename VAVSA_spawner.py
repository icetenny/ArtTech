import pygame
import sys
import numpy as np
import time
from custom_socket import CustomSocket
import socket
import cv2
import json
from ghost import ShowGhost
import os
import datetime
from rembg import remove
import cv2
import queue
import threading
import time


def get_available_camera_indexes():
    available_cameras = []
    for index in range(10):
        print("here")
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            continue
        available_cameras.append(index)
        cap.release()
    return available_cameras

# Get a list of available camera indexes
# available_cameras = get_available_camera_indexes()

# if available_cameras:
#     print("Available camera indexes:")
#     for index in available_cameras:
#         print(f"Camera {index}")
# else:
#     print("No cameras found.")
#     exit()

# bufferless VideoCapture


class VideoCapture:
    def __init__(self, name, resolution):
        # self.cap = cv2.VideoCapture(name)
        cap = cv2.VideoCapture(name)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Current resolution: {width}x{height}")
        cap.release()
        self.cap = cv2.VideoCapture(name)

        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


# Initialize Pygame
pygame.init()

# Constants
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
BG_COLOR = (255, 255, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

host = socket.gethostname()
port_receiver = 10011

cap = VideoCapture(int(input("Camera Index : ")), resolution=(960, 540))
# cap = cv2.VideoCapture("pic/bg2.mp4")

# Initialize the screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_info = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 540
# print(screen_width, screen_height)
# screen_width, screen_height = 1920, 1080

# Create a fullscreen Pygame window
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


pygame.display.set_caption("Spawn GUI")
clock = pygame.time.Clock()
fps = 30

icon = pygame.image.load("pic/vavsa_logo_2.png")
pygame.display.set_icon(icon)

# Fonts
font = pygame.font.Font(None, 36)

ui_bg = pygame.transform.scale(pygame.image.load(
    "pic/VAVSA_SPAWN.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))


class NP_Screen:
    def __init__(self, shape):
        self.screen = np.zeros(shape, dtype="uint8")  # Width , height
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)
        x, y, w, h = element.position
        self.screen[x:x+w, y:y+h] = element.id
        self.update()

    def update(self):
        for element in self.elements:
            if isinstance(element, Slider):
                x, y, w, h = element.slider_position
                self.screen[x:x+w, y:y+h] = element.id

    def draw_all_elements(self):
        for element in self.elements:
            element.draw()


class Button():
    def __init__(self, id, position=(0, 0, 0, 0), position_n=(0, 0, 0, 0), drawing=True, color=(255, 0, 0), pressed_color=(0, 255, 0)):
        self.id = id
        self.position = position
        self.position_n = position_n
        self.color = color
        self.drawing = drawing
        self.pressed_color = pressed_color

        if self.position_n != (0, 0, 0, 0):
            x1, y1, x2, y2 = int(self.position_n[0] * (SCREEN_WIDTH)), int(self.position_n[1] * (SCREEN_HEIGHT)), \
                int(self.position_n[2] * (SCREEN_WIDTH)
                    ), int(self.position_n[3] * (SCREEN_HEIGHT))
            self.position = (x1, y1, (x2-x1), (y2-y1))

    def draw(self):
        if self.drawing:
            pygame.draw.rect(screen, self.color, self.position)


class Slider():
    def __init__(self, id, position=(0, 0, 0, 0), position_n=(0, 0, 0, 0), drawing=True, color=(255, 0, 0), slider_size=(20, 30), slider_color=(0, 255, 0)):
        self.id = id
        self.position = position
        self.position_n = position_n
        self.color = color
        self.drawing = drawing
        self.slider_size = slider_size
        self.slider_color = slider_color
        self.slider_position = (0, 0, 0, 0)

        if self.position_n != (0, 0, 0, 0):
            x1, y1, x2, y2 = int(self.position_n[0] * (SCREEN_WIDTH)), int(self.position_n[1] * (SCREEN_HEIGHT)), \
                int(self.position_n[2] * (SCREEN_WIDTH)
                    ), int(self.position_n[3] * (SCREEN_HEIGHT))
            self.position = (x1, y1, (x2-x1), (y2-y1))

        self.slider_width = self.position[2]
        # Initial Value
        self.value = 0.5
        self.update_slider_position()

    def update_slider_position(self):
        dy = (self.slider_size[1] - self.position[3])//2
        self.slider_position = (
            self.position[0] + int(self.value * self.slider_width) - self.slider_size[0]//2, self.position[1] - dy, self.slider_size[0], self.slider_size[1])

    def update_value(self, pos_x):
        self.value = min(
            self.position[2], max(0, pos_x - self.position[0])) / self.slider_width
        self.update_slider_position()

    def set_value(self, new_value):
        self.value = new_value
        self.update_slider_position()

    def draw(self):
        if self.drawing:
            pygame.draw.rect(screen, self.color, self.position)
            pygame.draw.rect(screen, self.slider_color, self.slider_position)


def blit_center(screen, image, position):
    shape = image.get_size()
    x = position[0] - shape[0] // 2
    y = position[1] - shape[1] // 2
    screen.blit(image, (x, y))


def map_value(value, min, max):
    return (max - min) * value + min


running = True

np_screen = NP_Screen((SCREEN_WIDTH, SCREEN_HEIGHT))

# Spawn
button1 = Button(id=1, position_n=(0.607, 0.770, 0.827, 0.905), drawing=False)
np_screen.add_element(button1)

# Size
slider2 = Slider(id=2, position_n=(0.667, 0.439, 0.905, 0.459), drawing=True, color=(
    255, 240, 240), slider_size=(30, 20), slider_color=(150, 180, 225))
np_screen.add_element(slider2)

# Speed
slider3 = Slider(id=3, position_n=(0.667, 0.541, 0.905, 0.561), drawing=True, color=(
    255, 240, 240), slider_size=(30, 20), slider_color=(150, 180, 225))
np_screen.add_element(slider3)

# Flip1
button4 = Button(id=4, position_n=(0.579, 0.231, 0.652, 0.361),
                 drawing=False, color=(50, 50, 150))
np_screen.add_element(button4)

# Flip2
button5 = Button(id=5, position_n=(0.681, 0.231, 0.755, 0.359),
                 drawing=False, color=(200, 200, 0))
np_screen.add_element(button5)

# Capture
button6 = Button(id=6, position_n=(0.392, 0.709, 0.524, 0.941),
                 drawing=False, color=(200, 200, 0))
np_screen.add_element(button6)

# Delete
button7 = Button(id=7, position_n=(0.026, 0.039, 0.102, 0.178),
                 drawing=False, color=(255, 100, 100))
np_screen.add_element(button7)

# Rotate
button8 = Button(id=8, position_n=(0.782, 0.23, 0.858, 0.358),
                 drawing=False, color=(255, 100, 100))
np_screen.add_element(button8)

# Effect +
button9 = Button(id=9, position_n=(0.802, 0.622, 0.848, 0.724),
                 drawing=False, color=(0, 200, 100))
np_screen.add_element(button9)

# Effect -
button10 = Button(id=10, position_n=(0.585, 0.624, 0.634,
                  0.722), drawing=False, color=(0, 100, 200))
np_screen.add_element(button10)

clicked_id = 0

show_ghost = ShowGhost(
    screen, (SCREEN_WIDTH, SCREEN_HEIGHT), img_path="pic/pol_out.png")
goal_points_n = [(0.257, 0.198), (0.11, 0.383),
                 (0.39, 0.676), (0.148, 0.798), (0.39, 0.387)]
show_ghost.goal_points = [
    (int(gp[0] * SCREEN_WIDTH), int(gp[1] * SCREEN_HEIGHT)) for gp in goal_points_n]

ui_is_active = False
effect = 0
max_effect = 2

FONT_SIZE = 300  # Change font size
FONT_COLOR = (0, 200, 200)  # Change font color to blue
COUNTDOWN_DURATION = 4  # Countdown duration in seconds
font = pygame.font.Font(None, FONT_SIZE)
countdown_status = False

# size_min, size_max = 50, 200

while running:
    clock.tick(fps)
    try:
        screen.blit(ui_bg, (0, 0))

        game_out = dict()
        cam_out = dict()

        if not ui_is_active:
            raw_frame = cap.read()
            frame = cv2.transpose(raw_frame)

        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked_id = 0
                np_screen.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(round(mouse_x / SCREEN_WIDTH, 3),
                      round(mouse_y / SCREEN_HEIGHT, 3))
                clicked_id = np_screen.screen[mouse_x, mouse_y]
                if ui_is_active:
                    if clicked_id == 1:
                        print("Button clicked")
                        send_image = pygame.transform.scale(
                            show_ghost.original_image, (size_show, size_show))
                        data = np.dstack((pygame.surfarray.array3d(
                            send_image), pygame.surfarray.array_alpha(send_image)))
                        # print(data)

                        game_out["size"] = size_show
                        game_out["speed"] = speed
                        game_out["effect"] = effect
                        game_out["img"] = data.tolist()
                        game_out["task"] = "spawn"
                        ui_is_active = False

                        # Send ghost to receiver
                        client_receiver = CustomSocket(host, port_receiver)
                        client_receiver.clientConnect()
                        client_receiver.sendMsg(
                            client_receiver.sock, json.dumps(game_out))
                        client_receiver.clientDisconnect()

                        slider2.set_value(0.5)
                        slider3.set_value(0.5)
                        effect = 0
                        show_ghost.effect = effect
                        show_ghost.re_effect()

                    elif clicked_id == 4:
                        show_ghost.flip_image(axis=0)
                    elif clicked_id == 5:
                        show_ghost.flip_image(axis=1)
                    elif clicked_id == 7:
                        ui_is_active = False
                        effect = 0
                        show_ghost.effect = effect
                        show_ghost.re_effect()
                    elif clicked_id == 8:
                        show_ghost.rotate_image()
                    elif clicked_id == 9:
                        effect = (effect + 1) % (max_effect + 1)
                        show_ghost.effect = effect
                        show_ghost.re_effect()
                    elif clicked_id == 10:
                        effect = (effect - 1) % (max_effect + 1)
                        show_ghost.effect = effect
                        show_ghost.re_effect()

                elif clicked_id == 6:
                    if not countdown_status:
                        countdown_status = True
                        start_time = time.time()
                        end_time = start_time + COUNTDOWN_DURATION

            if clicked_id == 2:
                slider2.update_value(mouse_x)
            elif clicked_id == 3:
                slider3.update_value(mouse_x)

        if countdown_status:
            if time.time() >= end_time:
                countdown_status = False
                print("Capturing")
                cam_out["img"] = frame.tolist()
                cam_out["task"] = "rembg"

                client_receiver = CustomSocket(host, port_receiver)
                client_receiver.clientConnect()
                client_receiver.sendMsg(
                    client_receiver.sock, json.dumps(cam_out))
                rev_data = json.loads(
                    client_receiver.recvMsg(client_receiver.sock))
                client_receiver.clientDisconnect()
                show_ghost.change_image_from_array(
                    img=np.array(rev_data["img"], dtype="uint8"))

                ui_is_active = True

            else:
                remaining_time = int(end_time - time.time())
                text = font.render(str(remaining_time), True, FONT_COLOR)  # Use new font size and color
                text_rect = text.get_rect(center=(200, 200))
                screen.blit(text, text_rect)

        size_show = int(map_value(slider2.value, 50, 120))
        speed = map_value(slider3.value, 2, 10)

        np_screen.draw_all_elements()

        if ui_is_active:
            show_ghost.change_size(new_size=size_show)
            show_ghost.change_speed(new_speed=speed)
            show_ghost.run()
        else:
            frame_show = np.transpose(cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB), (1, 0, 2))
            TOP_LEFT_CAM = (0.115, 0.061)
            screen.blit(pygame.transform.scale(pygame.surfarray.make_surface(frame_show), (50,50)), (int(
                TOP_LEFT_CAM[0] * SCREEN_WIDTH), int(TOP_LEFT_CAM[1] * SCREEN_HEIGHT)))

        pygame.display.flip()

    except Exception as e:
        print(f"An exception occurred: {e}")


pygame.quit()
sys.exit()
