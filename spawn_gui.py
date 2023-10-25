import pygame
import sys
import numpy as np
import time
from custom_socket import CustomSocket
import socket
import cv2
import json
from ghost import ShowGhost
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

host = socket.gethostname()
port = 10011
c = CustomSocket(host, port)
c.clientConnect()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spawn GUI")
clock = pygame.time.Clock()
fps = 30


# Fonts
font = pygame.font.Font(None, 36)


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
    def __init__(self, id, position, color):
        self.id = id
        self.position = position
        self.color = color


class Button(Element):
    def __init__(self, id, position=(0, 0, 0, 0), color=(255, 0, 0), pressed_color=(0, 255, 0)):
        super().__init__(id, position, color)
        self.pressed_color = pressed_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.position)
        text = font.render("Update", True, BG_COLOR)
        screen.blit(text, (170, 135))


class Slider(Element):
    def __init__(self, id, position=(0, 0, 0, 0), color=(255, 0, 0), slider_size=(20, 30), slider_color=(0, 255, 0)):
        super().__init__(id, position, color)
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
        pygame.draw.rect(screen, self.color, self.position)
        pygame.draw.rect(screen, self.slider_color, self.slider_position)


def blit_center(screen, image, position):
    shape = image.get_size()
    x = position[0] - shape[0] // 2
    y = position[1] - shape[1] // 2
    screen.blit(image, (x, y))

def map_value(value, min, max):
    return (max - min) * value + min

def main():
    running = True

    np_screen = NP_Screen((SCREEN_WIDTH, SCREEN_HEIGHT))

    button1 = Button(id=1, position=(150, 450, 100, 40))
    np_screen.add_element(button1)

    slider2 = Slider(id=2, position=(50, 250, 300, 10), color=(
        255, 240, 240), slider_size=(30, 20), slider_color=(20, 20, 20))
    np_screen.add_element(slider2)

    slider3 = Slider(id=3, position=(50, 300, 300, 10), color=(
        255, 240, 240), slider_size=(30, 20), slider_color=(100, 20, 20))
    np_screen.add_element(slider3)

    button4 = Button(id=4, position=(150, 350, 100, 40), color=(50,50,150))
    np_screen.add_element(button4)

    button5 = Button(id=5, position=(150, 400, 100, 40), color=(200,200,0))
    np_screen.add_element(button5)

    clicked_id = 0
    # last_clicked_id = 0

    img_ori = pygame.image.load("pic/pol_out.png")
    img_show = img_ori.copy()

    show_ghost = ShowGhost(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), img_path="pic/pol_out.png")
    
    # size_min, size_max = 50, 200

    while running:
        try:
            clock.tick(fps)
            screen.fill(BG_COLOR)

            out = dict()

            

            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # print(clicked_id)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    clicked_id = 0
                    np_screen.update()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_id = np_screen.screen[mouse_x, mouse_y]

                    if clicked_id == 1:
                        slider2.set_value(0.5)
                        slider3.set_value(0.5)
                        print("Button clicked")
                        send_image =  pygame.transform.scale(show_ghost.original_image, (size_show, size_show))
                        data = np.dstack((pygame.surfarray.array3d(send_image), pygame.surfarray.array_alpha(send_image)))
                        print(data)

                        out["size"] = size_show
                        out["speed"] = speed
                        out["img"] = data.tolist()
                        
                    elif clicked_id == 4:
                        show_ghost.flip_image(axis=0)
                    elif clicked_id == 5:
                        show_ghost.flip_image(axis=1)


                if clicked_id == 2:
                    slider2.update_value(mouse_x)
                elif clicked_id == 3:
                    slider3.update_value(mouse_x)


            # size_show = slider2.value
            # speed = slider3.value

            size_show = int(map_value(slider2.value, 50, 120))
            speed = map_value(slider3.value, 2, 10)

            # img_show = pygame.transform.scale(img_ori, (size_show, size_show))
    
            data = c.req(json.dumps(out))

            np_screen.draw_all_elements()

            # blit_center(screen=screen, image=img_show, position=(200,100))
            show_ghost.change_size(new_size=size_show)
            show_ghost.change_speed(new_speed=speed)
            show_ghost.run()

            pygame.display.flip()
        
        except Exception as e:
            print(f"An exception occurred: {e}")


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
