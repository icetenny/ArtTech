import pygame
import cv2

video = cv2.VideoCapture("pic/countdown.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)

window = pygame.display.set_mode(video_image.shape[1::-1])
clock = pygame.time.Clock()

run = success
while run:
    clock.tick(fps*10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    success, video_image = video.read()
    if success:
        video_surf = pygame.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
    else:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, video_image = video.read()
    window.blit(video_surf, (0, 0))
    pygame.display.flip()

pygame.quit()
exit()