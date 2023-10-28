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
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BG_COLOR = (255, 255, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

host = socket.gethostname()
port_game = 10011
client_game = CustomSocket(host, port_game)
# client_game.clientConnect()

port_cam = 10012
client_cam = CustomSocket(host, port_cam)
# server_cam.startServer()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spawn GUI")
clock = pygame.time.Clock()
fps = 30

icon = pygame.image.load("pic/vavsa_logo_2.png")
pygame.display.set_icon(icon)

# Fonts
font = pygame.font.Font(None, 36)

cam_icon = pygame.transform.scale(pygame.image.load("pic/camera.png"), (100,100))

ui_bg = pygame.transform.scale(pygame.image.load("pic/spawn_ui.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

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


class Element:
    def __init__(self, id, position, drawing, color):
        self.id = id
        self.position = position
        self.color = color
        self.drawing = drawing


class Button(Element):
    def __init__(self, id, position=(0, 0, 0, 0), drawing=True, color=(255, 0, 0), pressed_color=(0, 255, 0)):
        super().__init__(id, position, drawing, color)
        self.pressed_color = pressed_color

    def draw(self):
        if self.drawing:
            pygame.draw.rect(screen, self.color, self.position)


class Slider(Element):
    def __init__(self, id, position=(0, 0, 0, 0), drawing=True, color=(255, 0, 0), slider_size=(20, 30), slider_color=(0, 255, 0)):
        super().__init__(id, position, drawing, color)
        self.slider_size = slider_size
        self.slider_color = slider_color
        self.slider_width = position[2]
        self.slider_position = (0, 0, 0, 0)

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
button1 = Button(id=1, position=(370, 265, 135, 49), drawing=False)
np_screen.add_element(button1)

# Size
slider2 = Slider(id=2, position=(398, 187, 168, 5), drawing=True, color=(
    255, 240, 240), slider_size=(30, 20), slider_color=(20, 20, 20))
np_screen.add_element(slider2)

# Speed
slider3 = Slider(id=3, position=(398, 231, 168, 5), drawing=True, color=(
    255, 240, 240), slider_size=(30, 20), slider_color=(100, 20, 20))
np_screen.add_element(slider3)

# Flip1
button4 = Button(id=4, position=(373, 99, 51, 51), drawing=False, color=(50,50,150))
np_screen.add_element(button4)

# Flip2
button5 = Button(id=5, position=(445, 99, 51, 51), drawing=False, color=(200,200,0))
np_screen.add_element(button5)

# Capture
button6 = Button(id=6, position=(108, 172, 98, 76), drawing=False, color=(200,200,0))
np_screen.add_element(button6)

# Delete
button7 = Button(id=7, position=(35, 32, 20, 20), drawing=True, color=(255,100,100))
np_screen.add_element(button7)


clicked_id = 0

show_ghost = ShowGhost(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), img_path="pic/pol_out.png")
ui_is_active = False

# size_min, size_max = 50, 200

cam_server_connected = client_cam.clientConnect()

game_server_connected = client_game.clientConnect()

while running:
    clock.tick(fps)

    if not game_server_connected:
        try:
            game_server_connected = client_game.clientConnect()
        except Exception as e:
            print("Game server not connected")

    if not cam_server_connected:
        try:
            cam_server_connected = client_cam.clientConnect()
        except Exception as e:
            print("Cam server not connected")

    try:
        screen.blit(ui_bg, (0,0))

        game_out = dict()
        cam_out = dict()

        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # print(mouse_x, mouse_y)
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked_id = 0
                np_screen.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_id = np_screen.screen[mouse_x, mouse_y]
                if ui_is_active:
                    if clicked_id == 1:
                        slider2.set_value(0.5)
                        slider3.set_value(0.5)
                        print("Button clicked")
                        send_image =  pygame.transform.scale(show_ghost.original_image, (size_show, size_show))
                        data = np.dstack((pygame.surfarray.array3d(send_image), pygame.surfarray.array_alpha(send_image)))
                        # print(data)

                        game_out["size"] = size_show
                        game_out["speed"] = speed
                        game_out["img"] = data.tolist()
                        ui_is_active = False
                        
                    elif clicked_id == 4:
                        show_ghost.flip_image(axis=0)
                    elif clicked_id == 5:
                        show_ghost.flip_image(axis=1)
                    elif clicked_id == 7:
                        ui_is_active = False

                elif clicked_id == 6:
                    print("Capturing")
                    cam_out["req"] = True

            if clicked_id == 2:
                slider2.update_value(mouse_x)
            elif clicked_id == 3:
                slider3.update_value(mouse_x)

        size_show = int(map_value(slider2.value, 50, 120))
        speed = map_value(slider3.value, 2, 10)

        if cam_server_connected:
            try:
                # Capturing gohst pic from cam
                cam_data = client_cam.req(json.dumps(cam_out))
                if cam_data:
                    captured_image = np.array(cam_data["img"])
                    show_ghost.change_image_from_array(img=captured_image)
                    ui_is_active = True
            except:
                print("Server disconnect")
                cam_server_connected = False
                client_cam = CustomSocket(host, port_cam)

        if game_server_connected:
            try:
                # Spawning Ghost to game
                data = client_game.req(json.dumps(game_out))
            except:
                print("Server disconnect")
                game_server_connected = False
                client_game = CustomSocket(host, port_game)


        np_screen.draw_all_elements()

        if ui_is_active:
            show_ghost.change_size(new_size=size_show)
            show_ghost.change_speed(new_speed=speed)
            show_ghost.run()
        else:
            blit_center(screen=screen, image=cam_icon, position=(155,208))

        pygame.display.flip()
    
    except Exception as e:
        print(f"An exception occurred: {e}")


pygame.quit()
sys.exit()

