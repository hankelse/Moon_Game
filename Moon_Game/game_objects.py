import pygame, time, random, math



class HUD:
    def __init__(self, surface_width, surface_height, font_url):
        self.surface_width, self.surface_height = surface_width, surface_height
        self.font_url = font_url
    def display(self, surface, player_max_stamina, player_max_health, player_stamina, player_health, active_chunk, terrain):
        font = pygame.font.Font(self.font_url, 30)

        stamina_txt = font.render('STAMINA', False, (0, 0, 0))
        stamina_txt_rect = stamina_txt.get_rect(center=(self.surface_width/20*3, self.surface_height/40*3))

        health_txt = font.render('HEALTH', False, (0, 0, 0))
        health_txt_rect = stamina_txt.get_rect(center=(self.surface_width/20*17, self.surface_height/40*3))

        pygame.draw.rect(surface, (160, 160, 160), pygame.Rect(self.surface_width/20, self.surface_height/20, self.surface_width/5, self.surface_height/20))
        stamina_bar_x = self.surface_width/20 + (player_stamina/player_max_stamina)*self.surface_width/5
        pygame.draw.polygon(surface, (100, 200, 100), ((self.surface_width/20, self.surface_height/10),(self.surface_width/20, self.surface_height/20),  (stamina_bar_x, self.surface_height/20), (stamina_bar_x, self.surface_height/10)))
        surface.blit(stamina_txt, stamina_txt_rect)

        pygame.draw.rect(surface, (160, 160, 160), pygame.Rect(self.surface_width/4*3, self.surface_height/20, self.surface_width/5, self.surface_height/20))
        health_bar_x = self.surface_width/4*3 + (player_health/player_max_health)*self.surface_width/5
        pygame.draw.polygon(surface, (200, 100, 100), ((self.surface_width/4*3, self.surface_height/10),(self.surface_width/4*3, self.surface_height/20),  (health_bar_x, self.surface_height/20), (health_bar_x, self.surface_height/10)))
        surface.blit(health_txt, health_txt_rect)

        big_font = pygame.font.Font(self.font_url, 60)
        biome_txt = big_font.render(terrain[active_chunk], False, (0, 0, 0))
        biome_txt_rect = biome_txt.get_rect(center=(self.surface_width/2, self.surface_height/40*5))
        surface.blit(biome_txt, biome_txt_rect)

class Tracking_Bullet:
    def __init__(self, x, y, size, color, lifespan, xv, yv, aggression, surface_width, surface_height):
        self.x, self.y = x, y
        self.size = size
        
        self.xv, self.yv = xv, yv
        self.max_xv, self.min_xv = 5, -5
        self.max_yv, self.min_yv= 5, -5

        self.acceleration = aggression/10
        self.deceleration = 0.125

        self.color = color

        self.creation_time = time.time()
        self.lifespan = lifespan

        self.damage = 25

        self.surface_width, self.surface_height = surface_width, surface_height
    

    def decelerate(self, vel):
        if vel > self.deceleration: vel -= self.deceleration
        elif vel < -self.deceleration: vel += self.deceleration
        else: vel = 0


    def move(self, desired_x=None, desired_y=None):
        if time.time() - self.creation_time < self.lifespan:
            d_x, d_y = desired_x, desired_y
            #print(d_x, d_y)
            if d_x != None or d_y != None: 
                
                if d_x < self.x and self.xv-self.acceleration > self.min_xv: 
                    self.xv -= self.acceleration

                elif d_x > self.x and self.xv+self.acceleration < self.max_xv: 
                    self.xv += self.acceleration
                
                else:
                    self.decelerate(self.xv)

                if d_y < self.y and self.yv-self.acceleration > self.min_yv: 
                    self.yv -= self.acceleration

                elif d_y > self.y and self.yv+self.acceleration < self.max_yv: 
                    self.yv += self.acceleration
                
                else:
                    self.decelerate(self.yv)


            else:
                self.decelerate(self.xv)
                self.decelerate(self.yv)
            
            self.x += self.xv
            self.y += self.yv
        else:
            #self.color = (0, 0, 0)
            if self.y < self.surface_height+self.size and self.y > -self.size:
                self.x += self.xv 
                self.y += self.yv
                if self.xv < 0: self.xv -= self.acceleration/3
                else:self.xv += self.acceleration/4
                if self.yv < 0: self.yv -= self.acceleration/3
                else: self.yv += self.acceleration/4
                self.yv *=1.001
            else:
                return("explode")
    
    def draw(self, surface):
        pygame.draw.ellipse(surface, (0, 0, 0), pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))
        pygame.draw.ellipse(surface, self.color, pygame.Rect(self.x-self.size*9/20, self.y-self.size*9/20, self.size*9/10, self.size*9/10))



class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.color = color
        self.text, self.text_color = text, text_color
        self.font = pygame.font.Font(font, 40)
        self.text_obj = self.font.render(self.text, False, self.text_color)
        self.text_rect = self.text_obj.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.x-self.width/2, self.y-self.height/2, self.width, self.height))
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x-self.width*9/20, self.y-self.height*9/20, self.width*9/10, self.height*9/10))
        surface.blit(self.text_obj, self.text_rect)

    def clicked(self, mouse):
        if abs(self.x - mouse[0]) < self.width/2 and abs(self.y-mouse[1])<self.height/2: return(True)
        else: return(False)


class Backdrop:
    def __init__(self, screen_width, screen_height, surface_width, surface_height, num_chunks, biome_size_range):
        self.screen_width, self.screen_height = screen_width, screen_height
        self.num_chunks, self.biome_size_range = num_chunks, biome_size_range
        self.screen_width, self.screen_height, self.surface_width, self.surface_height =  screen_width, screen_height, surface_width, surface_height
        #self.backdrop_raw = pygame.image.load("Moon_Game/Backdrop/backdrop.xcf")
        #self.backdrop = pygame.transform.scale(self.backdrop_raw, (screen_width, screen_height))
        
        self.biome_dict = {
            "glomp_canyon_norm": "Moon_Game/Backdrop/glomp_canyon.xcf",
            "glomp_canyon_start": "Moon_Game/Backdrop/glomp_canyon_start.xcf",
            "glomp_canyon_end": "Moon_Game/Backdrop/glomp_canyon_end.xcf",
        }
        self.load_images()

        self.biomes = ["glomp_canyon"]
        # for biome in self.biome_dict:
        #     self.biomes.append(biome)

        #self.backdrop_rect = self.backdrop.get_rect(center=(screen_width/2, screen_height/2))

        self.terrain = []
        self.chunk_types = []
        self.generate_chunks()

        for i in range(len(self.terrain)):
            index = self.terrain[i].find("_")
            #print(index)
            temp = list(self.terrain[i])
            temp[index] = " "
            self.terrain[i] = "".join(temp)
        #print(self.terrain)
    
    def generate_chunks(self):
        while len(self.terrain) < self.num_chunks:
            for biome in range(len(self.biomes)):
                biome_size = random.randint(self.biome_size_range[0], self.biome_size_range[1])
                if len(self.terrain) + biome_size > self.num_chunks:
                    biome_size = self.num_chunks - len(self.terrain)
                for i in range(biome_size):
                    self.terrain.append(self.biomes[biome])
                if len(self.terrain) == self.num_chunks: break
        else:
            for thing in self.terrain:
                self.chunk_types.append(thing)
            for i in range(1, len(self.chunk_types)-1):
                if self.chunk_types[i] == self.chunk_types[i+1]:
                    self.chunk_types[i] = str(self.chunk_types[i] + "_norm")
                else: self.chunk_types[i] = str(self.chunk_types[i]+"_"+self.chunk_types[i+1])
            self.chunk_types[0]= str(self.chunk_types[0]+"_start")
            self.chunk_types[-1]= str(self.chunk_types[-1]+"_end")
        
        
            #for i in range(len(terrain)):
                
                

    def load_images(self):
        for key in self.biome_dict:
            #print(self.screen_width)
            self.biome_dict[key]= pygame.transform.scale(pygame.image.load(self.biome_dict[key]), (self.screen_width, self.screen_height))

    
    def draw(self, surface, active_chunk, player_x):
        surface.blit(self.biome_dict[self.chunk_types[active_chunk]], (active_chunk*self.screen_width, 0))
        if player_x - self.screen_width*active_chunk > self.screen_width/2 and active_chunk != len(self.chunk_types)-1:
            surface.blit(self.biome_dict[self.chunk_types[active_chunk+1]], ((active_chunk+1)*self.screen_width, 0))
            #print(self.chunk_types[active_chunk+1])
        elif player_x - self.screen_width*active_chunk < self.screen_width/2 and active_chunk != 0:
            surface.blit(self.biome_dict[self.chunk_types[active_chunk-1]], ((active_chunk-1)*self.screen_width, 0))
            #print(active_chunk-1, (active_chunk-1)*self.screen_width, player_x)
        
        

