from re import S
import pygame, math, random, time

class Player:
    def __init__(self, startingx, startingy, player_width, player_height, screen_width, screen_height, surface_width, surface_height, acceleration, deceleration, max_speed, max_health, max_stamina):
        self.x, self.y = startingx, startingy
        self.width, self.height = player_width, player_height
        self.screen_width, screen_height,self.surface_width, self.surface_height = screen_width, screen_height, surface_width, surface_height

        self.setup_skins()

        # movement
        self.xv, self.yv = 0, 0
        self.x_acceleration, self.y_acceleration = acceleration, acceleration
        self.deceleration = deceleration
        self.max_xv, self.max_yv, self.min_xv, self.min_yv = max_speed, max_speed, -max_speed, -max_speed
        self.xd, self.yd = 0, 0

        self.stamina = self.max_stamina = max_stamina
        self.health = self.max_health = max_health

        self.sprint_factor = 2

        self.stamina_drain = 0
        self.stamina_drain_factor = 0.15
        self.stamina_recovery = 1


        self.walking = True
        self.moving_x = False
        self.moving_y = False

        self.juking = False
        self.juke_frames = 0 #frames remaining in a juke at any time
        self.last_juke = time.time()
        self.juke_delay = 0.5
        self.juke_frame_length = 5
        self.juke_speed_factor = 6
        self.juke_stamina_drain = 10





        self.steps_per_second = 5
        self.last_step = time.time()



    def setup_skins(self):
        
        skins_url = [
            "Moon_Game/Old_Man/Back1.xcf",
            "Moon_Game/Old_Man/Back2.xcf",
            "Moon_Game/Old_Man/Back3.xcf",
            "Moon_Game/Old_Man/Right1.xcf",
            "Moon_Game/Old_Man/Right2.xcf",
            "Moon_Game/Old_Man/Right3.xcf",
            "Moon_Game/Old_Man/Front1.xcf",
            "Moon_Game/Old_Man/Front2.xcf",
            "Moon_Game/Old_Man/Front3.xcf",
            "Moon_Game/Old_Man/Left1.xcf",
            "Moon_Game/Old_Man/Left2.xcf",
            "Moon_Game/Old_Man/Left3.xcf",
        ]
        self.img_skins = []
        for skin in skins_url:
            self.img_skins.append(pygame.image.load(skin))
        self.skins = []
        for skin in self.img_skins:
            self.skins.append(pygame.transform.scale(skin, (self.width, self.height)))
        
        self.back_skins = self.skins[0:3]
        self.back_skins.append(self.skins[1])

        self.right_skins = self.skins[3:6]
        self.right_skins.append(self.skins[4])

        self.front_skins = self.skins[6:9]
        self.front_skins.append(self.skins[7])

        self.left_skins = self.skins[9::]
        self.left_skins.append(self.skins[10])

        self.active_skins = self.front_skins
        self.active_skin_index = 0
    

    def get_input(self, keys, bindings):


        if keys[bindings["sprint"][0]] and self.stamina > 4*self.stamina_drain_factor:
            self.active_sprint_factor = self.sprint_factor
            self.steps_per_second = 10
            self.stamina_drain = 2
        else: 
            self.active_sprint_factor = 1
            self.steps_per_second = 5
            self.stamina_drain = 0

        self.moving_x = False
        self.moving_y = False
       
        if keys[bindings["up"][0]] or keys[bindings["up"][1]]:
            self.moving_y = True
            self.yd = -1
            self.active_skins = self.back_skins
            #self.yv -= self.y_acceleration

            if self.yv == self.min_yv:pass
            elif self.yv - self.y_acceleration < self.min_yv: self.yv -= self.y_acceleration
            else: self.yv = self.min_yv

        elif keys[bindings["down"][0]] or keys[bindings["down"][1]]:
            self.moving_y = True
            self.yd = 1
            self.active_skins = self.front_skins

            if self.yv == self.max_yv:pass
            elif self.yv + self.y_acceleration < self.max_yv: self.yv += self.y_acceleration
            else: self.yv = self.max_yv

        elif keys[bindings["left"][0]] or keys[bindings["left"][1]]:
            self.moving_x = True
            self.xd = -1
            self.active_skins = self.left_skins

            if self.xv == self.min_xv:pass
            elif self.xv - self.x_acceleration < self.min_xv: self.xv -= self.x_acceleration
            else: self.xv = self.min_xv


        elif keys[bindings["right"][0]] or keys[bindings["right"][1]]:
            self.moving_x = True
            self.xd = 1
            self.active_skins = self.right_skins

            if self.xv == self.max_xv:pass
            elif self.xv + self.x_acceleration < self.max_xv: self.xv += self.x_acceleration
            else: self.xv = self.max_xv
        
        else:
            self.active_skin_index = 1

            #slow down or stop y velocity
        if keys[bindings["juke"][0]] and time.time()-self.last_juke > self.juke_delay and self.stamina > self.juke_stamina_drain:
            self.walking = False
            self.juking = True
            self.juke_frames = self.juke_frame_length
            self.last_juke = time.time()
            

    def move(self, keys, bindings, uni_x_coord, physical_sprites):

        self.get_input(keys, bindings)

        if self.walking == True:

            #walking animations 
            if self.moving_x == True or self.moving_y == True: 
                current_time = time.time()
                if current_time - self.last_step > 1/self.steps_per_second:
                    self.next_skin()
                    self.last_step = current_time

                self.stamina -= self.stamina_drain*self.stamina_drain_factor
            
            else:
                if self.stamina + self.stamina_recovery < self.max_stamina: self.stamina += self.stamina_recovery
                else: self.stamina = self.max_stamina

            
            #deceleration

            if self.moving_y == False:
                #slow down or stop y velocity
                if self.yv > self.deceleration: self.yv -= self.deceleration
                elif self.yv < -self.deceleration: self.yv += self.deceleration
                else: self.yv = 0

            if self.moving_x == False:
                #slow down or stop x velocity 
                if self.xv > self.deceleration: self.xv -= self.deceleration
                elif self.xv < -self.deceleration: self.xv += self.deceleration
                else: self.xv = 0

            #moving player
            new_x, new_y = self.x + self.xv*self.active_sprint_factor, self.y+ self.yv*self.active_sprint_factor

            sprite_collision = False
            player_hitbox = self.get_hitbox(new_x, new_y)
            for sprite in physical_sprites:
                if sprite != self:
                    sprite_hitbox = sprite.get_hitbox()
                    if player_hitbox[1][1] < sprite_hitbox[1][0] or player_hitbox[1][0] > sprite_hitbox[1][1] or player_hitbox[0][1] < sprite_hitbox[0][0] or player_hitbox[0][0] > sprite_hitbox[0][1]:pass
                        #sprite_collision = False
                    else:
                        sprite_collision =True
                        break
            # sprite_collision = False
            # player_hitbox = self.get_hitbox(new_x, new_y)
            # for sprite in physical_sprites:
            #     if sprite != self:
            #         sprite_hitbox = sprite.get_hitbox()
            #         if player_hitbox[1][1] < sprite_hitbox[1][0]:pass
            #         elif player_hitbox[1][0] > sprite_hitbox[1][1]:pass
            #         elif player_hitbox[0][1] < sprite_hitbox[0][0]:pass
            #         elif player_hitbox[0][0] > sprite_hitbox[0][1]:pass
            #             #sprite_collision = False
            #         else:
            #             sprite_collision =True
            #             break
            
            if sprite_collision == False:
                if self.xv <0:
                    if new_x > self.width/2 + self.screen_width*0.0187: 
                        self.x = new_x
                elif self.xv >0:
                    if new_x < self.surface_width-self.width/2-self.screen_width*0.0187: self.x = new_x
                
                if self.yv <0:
                    if new_y > self.height/2: self.y = new_y
                elif self.yv >0:
                    if new_y < self.surface_height-self.height/2: self.y = new_y

            #if new_x < self.surface_width-self.width/2 and self.xv > 0: self.x = new_x

        
        elif self.juking == True:
            if self.juke_frames > 1:
                new_x, new_y = self.x + self.xv*self.active_sprint_factor*self.juke_speed_factor, self.y+ self.yv*self.active_sprint_factor*self.juke_speed_factor

                sprite_collision = False
                player_hitbox = self.get_hitbox(new_x, new_y)
                for sprite in physical_sprites:
                    if sprite != self:
                        sprite_hitbox = sprite.get_hitbox()
                        if player_hitbox[1][1] < sprite_hitbox[1][0] or player_hitbox[1][0] > sprite_hitbox[1][1] or player_hitbox[0][1] < sprite_hitbox[0][0] or player_hitbox[0][0] > sprite_hitbox[0][1]:pass
                            #sprite_collision = False
                        else:
                            sprite_collision =True
                            break
                if sprite_collision == False:
                    if self.xv <0:
                        if new_x > self.width/2: self.x = new_x
                    elif self.xv >0:
                        if new_x < self.surface_width-self.width/2: self.x = new_x
                    
                    if self.yv <0:
                        if new_y > self.height/2: self.y = new_y
                    elif self.yv >0:
                        if new_y < self.surface_height-self.height/2: self.y = new_y
                
                self.juke_frames -= 1
                self.stamina -= self.juke_stamina_drain*self.stamina_drain_factor
            else:
                self.juking = False
                self.walking = True
                self.move(keys, bindings, uni_x_coord, physical_sprites)
        
        #SCROLL

        return(self.x-self.screen_width/2)
        # if self.x-uni_x_coord > self.surface_width*2/3: 
        #     #uni_x_coord_shift = self.x-self.surface_width*2/3-uni_x_coord
        #     uni_x_coord += self.x-uni_x_coord-self.surface_width*2/3
        #     #self.x = self.surface_width*2/3
        #     return(-uni_x_coord)
        # elif self.x+uni_x_coord < self.surface_width/3: 
        #     uni_x_coord_shift = self.x-self.surface_width/3
        #     uni_x_coord += self.x-uni_x_coord-self.surface_width/3
        #     #self.x = self.surface_width/3
        #     return(-uni_x_coord)
        # else:
        #     return(uni_x_coord)
      

    def next_skin(self):
        self.active_skin_index += 1
        if self.active_skin_index > len(self.active_skins)-1:
            self.active_skin_index = 0

    def draw(self,surface):
        pygame.draw.ellipse(surface, (0, 0, 0, 100), pygame.Rect(self.x-self.width/2.5, self.y+self.height/8, self.width/1.25, self.height/2))
        surface.blit(self.active_skins[self.active_skin_index], (round(self.x - self.active_skins[self.active_skin_index].get_width()/2), round(self.y - self.skins[self.active_skin_index].get_height()/2)))
    
    def get_hitbox(self, x=None, y=None):
        if x == None: x,y =self.x, self.y
        return([x-self.width/4, x+self.width/4],[y+self.height/4, y+self.height/2],[x, y])


class Glomp:
    def __init__(self, x, y, width, height, shot_interval):
        self.x, self.y, self.width, self.height = x, y, width, height
    
        self.state = 'sitting' #shooting

        self.raw_skin = pygame.image.load('Moon_Game/Enemies/Glomp/glomp.xcf')
        self.skin = pygame.transform.scale(self.raw_skin, (self.width, self.height)) 

        self.shot_interval = shot_interval
        self.last_shot =time.time()
    
    def move(self, num, Tracking_Bullet, aggression, surface_width, surface_height):
        if time.time()-self.last_shot > self.shot_interval:
            self.last_shot = time.time()
            return(self.shoot(num, Tracking_Bullet, aggression, surface_width, surface_height))
        else: return([])

    def shoot(self, num, Tracking_Bullet, aggression, surface_width, surface_height):
        bullets = []
        for i in range(num):

            bullets.append(Tracking_Bullet(self.x , self.y-self.height/2, (self.width/8), (128,53,133), 6, random.randint(-10, 10), random.randint(-15, -5), aggression, surface_width, surface_height))
        
        return(bullets)

    def draw(self, surface):
        surface.blit(self.skin, (self.x-self.width/2, self.y-self.height/2))
    
    def get_hitbox(self, x=None, y=None):
        if x == None: x,y =self.x, self.y
        return [[x-self.width/2,x+self.width/2], [y,y+self.height/2],[x, x]]


class Reaper:
    def __init__(self, x, y, size, speed):
        self.x, self.y = x, y
        self.size, self.speed = size, speed
        self.angle = 270
        self.spin_speed = 10

        self.state = "spinning"
        
        self.last_attack = time.time()
        self.attack_delay = 2

        self.width, self.height = 56*size, 56*size

        self.front_skin = pygame.transform.scale(pygame.image.load("Moon_Game/Enemies/Reaper/reaper_front.xcf"), (self.width, self.height))
        self.right_skin = pygame.transform.scale(pygame.image.load("Moon_Game/Enemies/Reaper/reaper_right.xcf"), (self.width, self.height))
        self.back_skin = pygame.transform.scale(pygame.image.load("Moon_Game/Enemies/Reaper/reaper_back.xcf"), (self.width, self.height))
        self.left_skin = pygame.transform.scale(pygame.image.load("Moon_Game/Enemies/Reaper/reaper_left.xcf"), (self.width, self.height))
    
    def move(self, player_x, player_y):
        if self.state == "standing": pass
        elif self.state == "spinning":
            self.angle += 30
    
    def draw(self, surface):
        
        self.angle = self.angle % 360
        if (self.angle >= 315 and self.angle <= 360) or (self.angle >= 0 and self.angle <45): skin = self.right_skin
        elif self.angle >= 45 and self.angle <135: skin = self.back_skin
        elif self.angle >= 135 and self.angle <225: skin = self.left_skin
        elif self.angle >= 225 and self.angle <315: skin = self.front_skin
        else: print("error")

        #print(self.angle - round(self.angle/90)*90)

        skin = pygame.transform.rotate(skin, (self.angle - round(self.angle/90)*90)/10)

        surface.blit(skin, (self.x-self.width/2, self.y-self.height/2))
        




