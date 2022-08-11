import pygame, sys, time
from sprites import Reaper
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d
pygame.init()

size = width, height =  800, 800
# size = width, height = pygame.display.get_window_size()
cycle_time = 0.025

screen = pygame.display.set_mode(size)
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

##----- IDEA:
# The image rotates but every 90 degrees it switches sprite


reaper = Reaper(400, 400, 5, 10)
while 1:
    

    
    now = time.time()
    screen.fill((160, 160, 160))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    reaper.move(400, 400)
    reaper.draw(screen)

    #screen.blit(skins[index], (x, 400))
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)
