from turtle import back
from sprites import Player, Glomp, Reaper
from game_objects import HUD, Tracking_Bullet, Button, Backdrop
import pygame, sys, time, random, pyautogui, math
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_LSHIFT, K_RETURN
pygame.init()
pygame.font.init()




#size = width, height =  1600, 1000
width, height = pyautogui.size()
width, height = int(width*7/8), int(height*7/8)
size = width, height
cycle_time = 0.025

screen = pygame.display.set_mode(size)


#----------SETTINGS----------#

#---HUD---#
font = "Fonts/yoster.ttf"
#---MAP---#

num_chunks = 3
biome_size_range = [2, 4]
render_distance = width


#___ENEMIES___#
glomp_width, glomp_height = 19*round(width/200), 19*round(width/200)
glomp_shot_num = 10
bullet_aggression = 4
glomp_shot_interval = 100

#---PLAYER---#
player_startingx, player_startingy = int(num_chunks/2)*width + width/2, height/2
player_width, player_height = 16*round(width/300), 18*round(width/300)  #16:18 ratio
player_acceleration, player_deceleration = 2, 1
player_max_speed = 6

player_max_stamina = 200
player_max_health = 100

#---SURFACE---#
surface_size = surface_width, surface_height = width*num_chunks, height
surface = pygame.Surface(surface_size, pygame.SRCALPHA)
static_surface = pygame.Surface(size, pygame.SRCALPHA)
screen_shake_amount = 7


#print(width, surface_width, surface_width/width, num_chunks)


key_bindings = {
    "up" : [K_w, K_UP],
    "left" : [K_a, K_LEFT],
    "down" : [K_s, K_DOWN],
    "right" : [K_d, K_RIGHT],
    "sprint" : [K_LSHIFT,0],
    "juke" : [K_SPACE, 0],
    "select" : [K_SPACE, K_RETURN]

}


def draw_sprites(sprites, player):
    sprites_dict = {}
    for sprite in sprites:
        sprites_dict[sprite.y] = sprite
    
    sprites_y_values = sorted(sprites_dict)

    for depth in sprites_y_values:
        if  abs(sprites_dict[depth].x - player.x) < render_distance:
            sprites_dict[depth].draw(surface)

#----------SETUP----------#

def setup():
    
    player = Player(player_startingx, player_startingy, player_width, player_height, width, height, surface_width, surface_height, player_acceleration, player_deceleration, player_max_speed, player_max_health, player_max_stamina)
    bullets = []
    sprites = []
    physical_sprites = []

    backdrop = Backdrop(width, height, surface_width, surface_height, num_chunks, biome_size_range)
    hud = HUD(width, height, font)
    try_again_button = Button(width/2, height/2, width/4, height/8, (100, 200, 100), "RESPAWN", (0, 0, 0), font)
    
    player_alive = True
    uni_x_coord = player_startingx

    glomps=[]
    for chunk in range(len(backdrop.terrain)):
        if backdrop.terrain[chunk] == "glomp canyon":
            glomps.append(Glomp(random.randint(width*chunk+100, width*(chunk+1)-100), random.randint(100, height-100), glomp_width, glomp_height, glomp_shot_interval))

    reapers = []
    reapers.append(Reaper(player.x, player.y+10, 5, 10))

    
    return(player, player_alive, hud, bullets, try_again_button, glomps, sprites, physical_sprites, uni_x_coord, backdrop, reapers)


player, player_alive, hud, bullets, try_again_button, glomps, sprites, physical_sprites, uni_x_coord, backdrop, reapers = setup()
#print(backdrop.terrain)
#print(backdrop.chunk_types)

surface_rect = (uni_x_coord, 0)
shake = 0
frame = 0

while 1:
    
    active_chunk = math.floor(player.x/width)
    #print(active_chunk)
    sprites = []
    physical_sprites = [player]
    for glomp in glomps: physical_sprites.append(glomp)
    frame+= 1
    now = time.time()


    if shake != 0: #screen shake cycle
        if shake == screen_shake_amount: shake = -screen_shake_amount
        elif shake == -screen_shake_amount: shake = 0
    
    #surface.blit(backdrop, backdrop_rect)
    #surface.fill((100, 100, 100))
    backdrop.draw(surface, active_chunk, player.x)
    static_surface.fill((0, 0, 0, 0))
    
    screen.fill((0, 0, 0))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()
    

    if player_alive == True:
    
        # if frame % 100 == 0: 
        #     new_bullets = glomp.shoot(glomp_shot_num, Tracking_Bullet, bullet_aggression, width, height)
        #     for bullet in new_bullets:
        #         bullets.append(bullet)
        for glomp in glomps:
            if abs(glomp.x-player.x) < render_distance:
                for new_bullet in glomp.move(glomp_shot_num, Tracking_Bullet, bullet_aggression, width, height):
                    bullets.append(new_bullet)
        
        for reaper in reapers:
            reaper.move(player.x, player.y)


        for bullet in bullets: 
            bullet_state = bullet.move(player.x, player.y)

            if abs(bullet.x -player.x) < player_width/4 and abs(bullet.y-player.y)<player_height/2:
                player.health -= bullet.damage
                player.x += bullet.xv
                player.y += bullet.yv
                bullets.remove(bullet)
                shake = screen_shake_amount

            if bullet_state == "explode": bullets.remove(bullet)
            #bullet.draw(surface)


        uni_x_coord = player.move(keys, key_bindings, uni_x_coord, physical_sprites )
        #print("player x:", player.x, "uni_x", uni_x_coord)
        #player.draw(surface)

        if player.health <= 0:
            player_alive = False
            player.health = 0

        #glomp.draw(surface)

        sprites.append(player)
        for glomp in glomps: sprites.append(glomp)
        for bullet in bullets: 
            sprites.append(bullet)

        #for reaper in reapers: sprites.append(reaper)


        draw_sprites(sprites, player)

        hud.display(static_surface, player_max_stamina, player_max_health, player.stamina, player.health, active_chunk, backdrop.terrain)
        


        
    else:
        try_again_button.draw(static_surface)
        if keys[key_bindings["select"][0]] or keys[key_bindings["select"][0]]:
            player, player_alive, hud, bullets, try_again_button, glomps, sprites, physical_sprites, uni_x_coord, backdrop, reapers = setup()

        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if try_again_button.clicked(mouse) == True:
                        player, player_alive, hud, bullets, try_again_button, glomps, sprites, physical_sprites, uni_x_coord, backdrop, reapers = setup()


    surface_rect=(-uni_x_coord + shake, 0)
    screen.blit(surface, surface_rect)
    screen.blit(static_surface, (0, 0))

    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)
