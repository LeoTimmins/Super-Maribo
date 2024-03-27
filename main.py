#  Leo Timmins
#
# 'Super Mario Bros'
#  MIT Licence 2023

import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Super Mario Bros")

### init

class UI():
    def __init__(self) -> None:
        self.health = 3
        self.coins = 0
        # timer for respawn grace period
        self.inviciblity = -1
    
    def render(self):
        screen.blit(coin_bg, (130, 350))
        money_as_display = f"{self.coins}/36"
        if self.coins > 999:
            money_as_display = f"${round(self.coins/1000,1)}K"
        if self.coins > 9_999:
            money_as_display = f"${round(self.coins/1000,0)}K"
        if self.coins > 999_999:
            money_as_display = f"${round(self.coins/1_000_000,1)}M"
        if self.coins > 9_999_999:
            money_as_display = f"${round(self.coins/1_000_000,0)}M"
        
        img = pygame.font.SysFont(None, 50).render(money_as_display, True, (255, 255, 0))
        screen.blit(img, (175, 460))
        
        screen.blit(heart_bg, (0, 350))
        for x in range(self.health):
            screen.blit(heart_full, (-10+x*30, 435))
        
class Enemy():
    def __init__(self, pos) -> None:
        self.pos = pos
        self.velocity = [0,0]
        self.jump_timer = -1
        self.direction = "right"
        self.alive = True

    def render(self):
        if self.alive:
            self.physics()
        if self.alive == True:
            if self.direction == "left":
                screen.blit(turtle_left, (self.pos[0]-80-camera_pos[0], self.pos[1]-80-camera_pos[1]))
            if self.direction == "right":
                screen.blit(turtle_right, (self.pos[0]-70-camera_pos[0], self.pos[1]-80-camera_pos[1]))
    
    def physics(self):
        self.move(self.direction)
        
        self.on_floor = False
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        if player.pos[0] < self.pos[0] + 45 and self.pos[0] - 45  < player.pos[0]:
            if player.pos[1] > self.pos[1] - 35 and player.pos[1] < self.pos[1]:
                self.alive = False
                player.jump_timer = -1
                player.on_floor = True
                player.velocity = [0,0]
                player.move("up")
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('src/audio/sfx/punch.mp3'))
        if player.pos[0] < self.pos[0] + 45 and self.pos[0] < player.pos[0]:
            if player.pos[1] < self.pos[1] + 35 and player.pos[1] > self.pos[1]:
                if ui.inviciblity == -1:
                    ui.health -= 1
                    ui.inviciblity = 59
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('src/audio/sfx/ow.mp3'))
        
        
        for platform_tile in platform_list:
            if self.pos[0] < platform_tile.pos[0] + 70 and platform_tile.pos[0] < self.pos[0]:
                if self.pos[1] >= platform_tile.pos[1]-20 and (self.pos[1] > platform_tile.pos[1] + 35)==False:
                    self.pos[1] = platform_tile.pos[1]-20
                    if self.velocity[1] > 0:
                        self.velocity[1] = 0
                    self.on_floor = True
                elif self.pos[1] > platform_tile.pos[1] + 35 and self.pos[1] <= platform_tile.pos[1] + 100:
                    self.pos[1] = platform_tile.pos[1]+100
                    if self.velocity[1] < 0:
                        self.velocity[1] = 0
                    self.jump_timer = -1
                
        if self.pos[1] >= 390:
            self.pos[1] = 390
            self.on_floor = True
        
        if self.on_floor == False:   
            self.velocity[1] += 0.2
        else:
            if self.velocity[1] > 0:
                self.velocity[1] = 0
        
        
        if self.jump_timer > -1:
            self.velocity[1] -=0.3
            self.pos[1] -= 5
            self.jump_timer -= 5
        
        if self.on_floor == False:
            self.sprite = "walk"
        else:
            self.sprite = "idle"

        
    def move(self, dir):
        match dir:
            case "left":
                for platform_tile in platform_list:
                    if self.pos[1] <= platform_tile.pos[1] + 70 and platform_tile.pos[1] < self.pos[1]:
                        if self.pos[0] - 2 > platform_tile.pos[0] and self.pos[0] - 2 < platform_tile.pos[0] + 70:
                            self.pos[0] += 2
                            self.direction = "right"
                self.pos[0] -= 2
                if self.pos[0] < 20:
                    self.pos[0] = 20
            case "right":
                for platform_tile in platform_list:
                    if self.pos[1] <= platform_tile.pos[1] + 70 and platform_tile.pos[1] < self.pos[1]:
                        if self.pos[0] + 2 > platform_tile.pos[0] and self.pos[0] + 2 < platform_tile.pos[0] + 70:
                            self.pos[0] -= 2
                            self.direction = "left"
                self.pos[0] += 2
            case "up":
                if self.jump_timer <= -1 and self.on_floor:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/audio/sfx/jump.wav'))
                    self.jump_timer = 100
    

class Player():
    def __init__(self) -> None:
        self.pos = [300,200]
        self.velocity = [0,0]
        # timer to make a parabolic jump
        self.jump_timer = -1
        # animation settings
        self.sprite = "idle"
        self.direction = "right"
    
    def physics(self):
        self.on_floor = False
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        # colision
        for platform_tile in platform_list:
            if self.pos[0] < platform_tile.pos[0] + 70 and platform_tile.pos[0] < self.pos[0]:
                if self.pos[1] >= platform_tile.pos[1] and self.pos[1] <= platform_tile.pos[1] + 35:
                    self.pos[1] = platform_tile.pos[1]
                    if platform_tile.sprite == jump_booster:
                        # make a big jump
                        self.velocity[1] *= -0.8
                        self.move("up")
                        self.jump_timer = 200
                    elif self.velocity[1] > 0:
                        self.velocity[1] = 0
                    self.on_floor = True
                    
                    if platform_tile.sprite == spikes:
                        ui.health = 0
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('src/audio/sfx/ow.mp3'))
                    
                elif self.pos[1] > platform_tile.pos[1] and self.pos[1] < platform_tile.pos[1] + 90:
                    if platform_tile.sprite == mystery_box:
                        pygame.mixer.Channel(3).play(pygame.mixer.Sound('src/audio/sfx/mystery_hit.wav'))
                        ui.coins += 1
                        platform_tile.sprite = mystery_box_inactive
                    else:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('src/audio/sfx/block_hit.wav'))
                    self.pos[1] = platform_tile.pos[1] + 90
                    self.velocity[1] = 0
                    self.jump_timer = -1
                
        if self.pos[1] >= 400:
            self.pos[1] = 400
            self.on_floor = True
        
        if self.on_floor == False:   
            self.velocity[1] += 0.2
        else:
            if self.velocity[1] > 0:
                self.velocity[1] = 0
        
        if self.jump_timer > -1:
            self.velocity[1] -=0.3
            self.pos[1] -= 5
            self.jump_timer -= 5
            
        ## Camera movement
        if self.pos[0] >= 600 + camera_pos[0]:
            camera_pos[0] += 6
            
        if self.pos[0] <= 200 + camera_pos[0]:
            camera_pos[0] -= 6
            if camera_pos[0] < 0:
                camera_pos[0] = 0
        
        if self.pos[1] >= 250 + camera_pos[1]:
            camera_pos[1] += 6
            if camera_pos[1] > 30:
                camera_pos[1] = 30
            
        if self.pos[1] <= 150 + camera_pos[1]:
            camera_pos[1] -= 6 
        ##
        
        if self.on_floor == False:
            self.sprite = "walk"
        else:
            self.sprite = "idle"

        
    def move(self, dir):
        match dir:
            case "left":
                self.direction = "left"
                for platform_tile in platform_list:
                    if self.pos[1] <= platform_tile.pos[1] + 70 and platform_tile.pos[1] < self.pos[1]:
                        if self.pos[0] - 6 > platform_tile.pos[0] and self.pos[0] - 6 < platform_tile.pos[0] + 70:
                            self.pos[0] += 6
                self.pos[0] -= 6
                if self.pos[0] < 20:
                    self.pos[0] = 20
            case "right":
                self.direction = "right"
                for platform_tile in platform_list:
                    if self.pos[1] <= platform_tile.pos[1] + 70 and platform_tile.pos[1] < self.pos[1]:
                        if self.pos[0] + 6 > platform_tile.pos[0] and self.pos[0] + 6 < platform_tile.pos[0] + 70:
                            self.pos[0] -= 6
                self.pos[0] += 6
            case "up":
                # jump
                if self.jump_timer <= -1 and self.on_floor:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/audio/sfx/jump.wav'))
                    self.jump_timer = 100
                
    def render(self):
        self.physics()
        #deubuging - point of collision
        #pygame.draw.rect(screen, (200,50,50), pygame.Rect(self.pos[0]-10-camera_pos[0],self.pos[1]-10,20,20))
        if f"{self.sprite}_{self.direction}" == "idle_left":
            screen.blit(player_animation_idle_left, (self.pos[0]-camera_pos[0]-30, self.pos[1]-55-camera_pos[1]))
        elif f"{self.sprite}_{self.direction}" == "idle_right":
            screen.blit(player_animation_idle_right, (self.pos[0]-camera_pos[0]-30, self.pos[1]-55-camera_pos[1]))
        elif f"{self.sprite}_{self.direction}" == "walk_left":
            screen.blit(player_animation_walk_left, (self.pos[0]-camera_pos[0]-30, self.pos[1]-55-camera_pos[1]))
        elif f"{self.sprite}_{self.direction}" == "walk_right":
            screen.blit(player_animation_walk_right, (self.pos[0]-camera_pos[0]-30, self.pos[1]-55-camera_pos[1]))
class Floor():
    def __init__(self, pos) -> None:
        self.pos = pos
    
    def render(self):
        screen.blit(floor, (self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1]))

class Cloud():
    def __init__(self, pos) -> None:
        self.pos = pos
        # To Do: Varying clouds
        c = random.randint(1,1)
        if c == 1:
            self.sprite = cloud_1
    
    def render(self):
        screen.blit(self.sprite, (self.pos[0]-camera_pos[0], self.pos[1]))

class Platform():
    def __init__(self,pos, type) -> None:
        self.pos = pos
        match type:
            case "Crate":    
                self.sprite = crate
            case "Myst":
                self.sprite = mystery_box
            case "Spikes":
                self.sprite = spikes
            case "Jumper":
                self.sprite = jump_booster
    
    def render(self):
        if self.sprite != "None":
            screen.blit(self.sprite, (self.pos[0]-camera_pos[0], self.pos[1]-camera_pos[1]))

# The selected scene
level = "menu"

camera_pos = [0,0]

pygame.mixer.music.load("src/audio/menu_theme.mp3")
pygame.mixer.music.play(-1)

## preload assets
jump_booster = pygame.image.load("src/img/jump_booster.png")
crate = pygame.image.load("src/img/crate.png")
crate = pygame.transform.scale(crate, (70,70))
mystery_box = pygame.image.load("src/img/myst_box.png")
mystery_box = pygame.transform.scale(mystery_box, (70,70))
spikes = pygame.image.load("src/img/spikes.png")
spikes = pygame.transform.scale(spikes, (70,70))
mystery_box_inactive = pygame.image.load("src/img/mystery_box_inactive.png")
mystery_box_inactive = pygame.transform.scale(mystery_box_inactive, (70,70))
logo = pygame.image.load("src/img/logo.png")
floor = pygame.image.load("src/img/dirt.png")
floor = pygame.transform.scale(floor, (150,150))
cloud_1 = pygame.image.load("src/img/cloud_1.png")
cloud_1 = pygame.transform.scale(cloud_1, (200,150))
sky = pygame.image.load("src/img/sky.jpeg")
sky = pygame.transform.scale(sky, (800,500))
turtle = pygame.image.load("src/img/turtle.png")
turtle_right = pygame.transform.scale(turtle, (150,150))
turtle_left = pygame.transform.flip(turtle_right, True, False)

heart_full = pygame.image.load("src/img/ui/heart_full.png")
heart_empty = pygame.image.load("src/img/ui/heart_empty.png")
heart_full= pygame.transform.scale(heart_full, (100,100))
heart_empty= pygame.transform.scale(heart_empty, (100,100))
heart_bg = pygame.image.load("src/img/ui/heart_bg.png")
heart_bg= pygame.transform.scale(heart_bg, (180,180))
coin_bg = pygame.image.load("src/img/ui/coin_bg.png")
coin_bg= pygame.transform.scale(coin_bg, (180,180))

logo_animation = -1

player_animation_idle_left = pygame.image.load("src/img/charecters/tile028.png")
player_animation_idle_right = pygame.image.load("src/img/charecters/tile043.png")
player_animation_walk_left = pygame.image.load("src/img/charecters/tile027.png")
player_animation_walk_right = pygame.image.load("src/img/charecters/tile042.png")
##

# Only one instance at a time should be active
player = Player()
ui = UI()

# render lists
scenery_list=[]
platform_list = []
enemy_list = []

for x in range(80):
    scenery_list.append(Floor((x*150, 400)))
    
for x in range(50):
    scenery_list.append(Cloud((x*400+20, random.randint(25,90))))

# Compile text into map
line_count = 0
word_count = 0
for line in open("platform_spawn.txt", "r").read().split("\n"):
    word_count = 0
    for word in line.split(" "):
        if word in ("Crate", "Myst", "Spikes", "Jumper"):
            platform_list.append(Platform((line_count*68, 340 - word_count*68), word))
        if word == "Enemy":
            enemy_list.append(Enemy([line_count*68, 340 - word_count*68]))
        word_count+=1
    line_count+=1


left_down = False
right_down = False
###


exit = False
while not exit:
    ## Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left_down = True
            if event.key == pygame.K_d:
                right_down = True
            if event.key == pygame.K_w:
                player.move("up")
            if event.key == pygame.K_r:
                ui.health = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                match level:
                    case "menu":
                        if logo_animation  == -1:
                            logo_animation = 0
            if event.key == pygame.K_a:
                left_down = False
            if event.key == pygame.K_d:
                right_down = False
    
    if left_down:
        player.move("left")
    if right_down:
        player.move("right")
    ##
    if ui.inviciblity != -1:
        ui.inviciblity -= 1
        
    # if dead => reset map
    if ui.health == 0:
        ui.health = 3
        ui.coins = 0
        for block in platform_list:
            if block.sprite == mystery_box_inactive:
                block.sprite = mystery_box
        for enemy in enemy_list:
            enemy.alive = True
        player = Player()
        player.pos[1]-=50
            
    screen.fill((50,200,250))
    screen.blit(sky, (0,0))
    
    for scenery_tile in scenery_list:
        scenery_tile.render()
    
    match level:
        case "menu":
            screen.blit(logo, (250,70+logo_animation))
            img = pygame.font.SysFont(None, 50).render("press 'Space' to play", True, (10,10,10))
            screen.blit(img, (235, 220 - logo_animation))
            # Move the logo
            if logo_animation != -1 and logo_animation >= -300:
                logo_animation -= 3
            # Check if animation is done
            if logo_animation <= -300:
                level = 1
                camera_pos[0] = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load("src/audio/gameplay_theme.mp3")
                pygame.mixer.music.play(-1)
            
            camera_pos[0] += 1  
        case 1:
            for platform_tile in platform_list:
                platform_tile.render()
            for enemy_tile in enemy_list:
                enemy_tile.render()
            player.render()
            ui.render()
        # To do: more levels?
            
          
    pygame.display.update()
    # frame rate capped to 140 fps
    pygame.time.Clock().tick(140)