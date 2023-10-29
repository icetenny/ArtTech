import pygame
pygame.init()

available_displays = [pygame.display.Info(i) for i in range(pygame.display.get_num_displays())]

second_monitor_index = 1
if second_monitor_index >= len(available_displays):
    print("Second monitor is not available.")
    pygame.quit()
    exit()

second_monitor_info = available_displays[second_monitor_index]
display_mode = (second_monitor_info.current_w, second_monitor_info.current_h)

screen = pygame.display.set_mode(display_mode, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, display=second_monitor_index)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
