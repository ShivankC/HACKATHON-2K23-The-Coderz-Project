# Pls note a few requirements to run this code
# Change image paths to what ever image path the image occupies on your system. On mine it shows the currently set paths. To copy the image paths on windows, right click on the image in file explorer and select copy image path. On mac, right click on the image in finder and then press option to view the copy image as pathname option.

import pygame
import moviepy
from moviepy.editor import *

pygame.init()

Screen_Height = 798
Screen_Width = 1235

screen = pygame.display.set_mode((Screen_Width,Screen_Height))

clock = pygame.time.Clock()

Player1_victory = VideoFileClip('/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/human.mp4')
Player2_victory = VideoFileClip('/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/alien.mp4')

gravity1 = 0
gravity2 = 0

Player1_Sprite_Sheet = pygame.image.load("/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/Light Bandit/LightBandit.png")
Player2_Sprite_Sheet = pygame.image.load("/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/Heavy Bandit/HeavyBandit.png")
Background = pygame.image.load("/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/BG.png")
Ground = pygame.image.load("/Users/Nupur/Desktop/Shivank/Coding/PygameStreetFighter-Project/Images/Screenshot 2023-07-29 at 11.35.58 AM.png")
Ground.set_colorkey("#FFFFFF")

Player1_move_right = False
Player1_move_left = False
Player1_attack = False
global Player1_action
Player1_action = "idle"
Player1_flip = True

Player2_move_right = False
Player2_move_left = False
Player2_attack = False
global Player2_action
Player2_action = "idle"
Player2_flip = False

Player1_x = 655 - 153
Player1_y = 435
Player2_x = 655 - 153
Player2_y = 435

bg = (50, 50, 50)

def get_image(sheet, frame, sprite_type, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        if sprite_type == "idle":
            image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        if sprite_type == "aggressive":
            image.blit(sheet, (0, 0), ((frame * width) + 192, 0, width, height))
        if sprite_type == "move": 
            image.blit(sheet, (0, 0), ((frame * width), 48, width, height))
        if sprite_type == "attack": 
            image.blit(sheet, (0, 0), ((frame * width), 96, width, height))
        if sprite_type == "jump": 
            image.blit(sheet, (0, 0), ((frame * width), 192, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

def get_animation(player, animation_type, steps):
    animation_list = []
    for i in range(steps):
        if player == "Player1":
            animation_list.append(get_image(Player1_Sprite_Sheet, i, animation_type, 48, 48, 3.2))
        if player == "Player2":
            animation_list.append(get_image(Player2_Sprite_Sheet, i, animation_type, 48, 48, 3.2))
    return animation_list

def change_action(player, action, zero):
    if player == "Player1":
        global Player1_action, Player1_frame
        Player1_action = action
        if zero == True:
            Player1_frame = 0
    if player == "Player2":
        global Player2_action, Player2_frame
        Player2_action = action
        if zero == True:
            Player2_frame = 0

def get_hits(player_rect, tile_rects):
    hits = []
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            hits.append(tile)
    return hits

def draw_health_bars(player, health, x, y):
    ratio = health / 100
    if player != "Player1":
        pygame.draw.rect(screen, "red", (x, y, 480, 45))
    else:
        pygame.draw.rect(screen, "red", (x, y, 400, 45))
    pygame.draw.rect(screen, "yellow", (x, y, 400 * ratio, 45))


Player1_idle_animation_steps = 4
Player1_aggressive_animation_steps = 4
Player1_animation_list = get_animation("Player1", "idle", Player1_idle_animation_steps)
Player1_move_animation_steps = 8
Player1_attack_animation_steps = 8
Player2_idle_animation_steps = 4
Player2_aggressive_animation_steps = 4
Player2_animation_list = get_animation("Player2", "idle", Player2_idle_animation_steps)
Player2_move_animation_steps = 8
Player2_attack_animation_steps = 8

Player1_idle_animation_last_update = pygame.time.get_ticks()
Player1_idle_animation_cooldown = 130
Player1_aggressive_animation_last_update = pygame.time.get_ticks()
Player1_aggressive_animation_cooldown = 130
Player1_move_animation_last_update = pygame.time.get_ticks()
Player1_move_animation_cooldown = 100
Player1_attack_animation_last_update = pygame.time.get_ticks()
Player1_attack_animation_cooldown = 70
Player1_frame = 0
Player1_on_ground = True
Player1_health = 100
Player2_idle_animation_last_update = pygame.time.get_ticks()
Player2_idle_animation_cooldown = 140
Player2_aggressive_animation_last_update = pygame.time.get_ticks()
Player2_aggressive_animation_cooldown = 140
Player2_move_animation_last_update = pygame.time.get_ticks()
Player2_move_animation_cooldown = 130
Player2_attack_animation_last_update = pygame.time.get_ticks()
Player2_attack_animation_cooldown = 70
Player2_frame = 0
Player2_on_ground = True
Player2_health = 120

tile_rects = [pygame.Rect((310, 335), (205, 45)), 
              pygame.Rect((700, 335), (205, 45)), 
              pygame.Rect((95, 435), (105, 45)), 
              pygame.Rect((1020, 435), (105, 45)), 
              pygame.Rect((350, 565), (520, 90))]

Player1_y_collisons = False

run = True
while run:
    screen.blit(Background, (0, 0))
    screen.blit(Ground, (0, 0))

    if Player1_x < 95: 
        Player1_x = 95
    if Player1_x + 100 > 1125:
        Player1_x = 1125 - 100
    if Player1_y < 120:
        Player1_y = 120

    if Player2_x < 95: 
        Player2_x = 95
    if Player2_x + 100 > 1125:
        Player2_x = 1125 - 100
    if Player2_y < 120:
        Player2_y = 120

    if Player1_action == "jump":
        Player1_on_ground = False
    if Player2_action == "jump":
        Player2_on_ground = False

    gravity1 += 2.5
    if gravity1 >= 50:
        gravity1 = 50
    gravity2 += 2.5
    if gravity2 >= 50:
        gravity2 = 50
    
    if Player1_on_ground == True:
        gravity1 = 0
    if Player2_on_ground == True:
        gravity2 = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Player1_move_left = True
                if Player1_action != "attack" and Player1_action != "jump" and Player1_on_ground == True:
                    change_action("Player1", "move", True)
            if event.key == pygame.K_d:
                Player1_move_right = True
                if Player1_action != "attack" and Player1_action != "jump" and Player1_on_ground == True:
                    change_action("Player1", "move", True)
            if event.key == pygame.K_s and Player1_action != "attack":
                Player1_attack = True
                change_action("Player1", "attack", True)
                if Player1_flip == True:
                    Player1_attack_rect = pygame.Rect(Player1_rect.centerx, Player1_rect.y, 150, 153)
                    if Player1_attack_rect.colliderect(Player2_rect):
                        Player2_health -= 10
                elif Player1_flip == False:
                    Player1_attack_rect = pygame.Rect(Player1_rect.centerx - 143, Player1_rect.y, 150, 153)
                    if Player1_attack_rect.colliderect(Player2_rect):
                        Player2_health -= 10
            if event.key == pygame.K_w:
                Player1_jump = True
                if Player1_action != "attack":
                    change_action("Player1", "jump", True)
                gravity1 = -30
            if event.key == pygame.K_LEFT:
                Player2_move_left = True
                if Player2_action != "attack" and Player2_action != "jump" and Player2_on_ground == True:
                    change_action("Player2", "move", True)
            if event.key == pygame.K_RIGHT:
                Player2_move_right = True
                if Player2_action != "attack" and Player2_action != "jump" and Player2_on_ground == True:
                    change_action("Player2", "move", True)
            if event.key == pygame.K_DOWN and Player2_action != "attack":
                Player2_attack = True
                change_action("Player2", "attack", True)
                if Player2_flip == False:
                    Player2_attack_rect = pygame.Rect(Player2_rect.centerx - 143, Player2_rect.y, 150, 153)
                    if Player2_attack_rect.colliderect(Player1_rect):
                        Player1_health -= 10
                elif Player1_flip == True:
                    Player2_attack_rect = pygame.Rect(Player2_rect.centerx, Player2_rect.y, 150, 153)
                    if Player2_attack_rect.colliderect(Player1_rect):
                        Player1_health -= 10
            if event.key == pygame.K_UP:
                Player2_jump = True
                if Player2_action != "attack":
                    change_action("Player2", "jump", True)
                gravity2 = -30
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Player1_move_left = False
                if Player1_move_right == True:
                    change_action("Player1", "move", True)
                elif Player1_y < 655-153 and Player1_on_ground == False:
                    change_action("Player1", "jump", True)
                elif Player1_action == "aggressive":
                    change_action("Player1", "agressive", True)
                else:
                    change_action("Player1", "idle", True)
            if event.key == pygame.K_d:
                Player1_move_right = False
                if Player1_move_left == True:
                    change_action("Player1", "move", True)
                elif Player1_y < 655-153 and Player1_on_ground == False:
                    change_action("Player1", "jump", True)
                elif Player1_action == "aggressive":
                    change_action("Player1", "agressive", True)
                else:
                    change_action("Player1", "idle", True)
            if event.key == pygame.K_LEFT:
                Player2_move_left = False
                if Player2_move_right == True:
                    change_action("Player2", "move", True)
                elif Player2_y < 655-153 and Player2_on_ground == False:
                    change_action("Player2", "jump", True)
                elif Player2_action == "aggressive":
                    change_action("Player2", "agressive", True)
                else:
                    change_action("Player2", "idle", True)
            if event.key == pygame.K_RIGHT:
                Player2_move_right = False
                if Player2_move_left == True:
                    change_action("Player2", "move", True)
                elif Player2_y < 655-153 and Player2_on_ground == False:
                    change_action("Player2", "jump", True)
                elif Player2_action == "aggressive":
                    change_action("Player2", "agressive", True)
                else:
                    change_action("Player2", "idle", True)
                
    
    if Player1_move_left == True:
        Player1_x -= 14  
        Player1_flip = False
    elif Player1_move_right == True:
        Player1_x += 14
        Player1_flip = True
    if Player1_y + gravity1 >= 655 - 153:
        Player1_y = 655 - 153
    else:
        Player1_y += gravity1

    if Player2_move_left == True:
        Player2_x -= 12 
        Player2_flip = False
    elif Player2_move_right == True:
        Player2_x += 12
        Player2_flip = True
    if Player2_y + gravity2 >= 655 - 153:
        Player2_y = 655 - 153
    else:
        Player2_y += gravity2
    
    if Player1_y == Player2_y and Player1_action != "move" and Player1_action != "attack" and Player1_action != "aggressive" and Player1_action != "jump":
        change_action("Player1", "aggressive", True)
    if Player1_y == Player2_y and Player2_action != "move" and Player2_action != "attack" and Player2_action != "aggressive" and Player2_action != "jump":
        change_action("Player2", "aggressive", True)

    if Player1_action == "attack":
        Player1_animation_list = get_animation("Player1", "attack", Player1_attack_animation_steps)
        Player1_attack_animation_current_time = pygame.time.get_ticks()
        if Player1_attack_animation_current_time - Player1_attack_animation_last_update >= Player1_attack_animation_cooldown:
            Player1_frame += 1
            Player1_attack_animation_last_update = Player1_attack_animation_current_time
            if Player1_frame >= 7:
                Player1_frame = 0
                if Player1_on_ground == False:
                    change_action("Player1", "jump", True)
                elif Player1_y == 655 - 153 and (Player1_move_left == True or Player1_move_right == True):
                    change_action("Player1", "move", True)
                else:
                    change_action("Player1", "idle", True)
                Player1_attack = False

    if Player1_action == "move":
        Player1_animation_list = get_animation("Player1", "move", Player1_move_animation_steps)
        Player1_move_animation_current_time = pygame.time.get_ticks()
        if Player1_move_animation_current_time - Player1_move_animation_last_update >= Player1_move_animation_cooldown:
            Player1_frame += 1
            Player1_move_animation_last_update = Player1_move_animation_current_time
            if Player1_frame >= 7:
                Player1_frame = 0

    if Player1_action == "aggressive":
        Player1_animation_list = get_animation("Player1", "aggressive", Player1_aggressive_animation_steps)
        Player1_aggressive_animation_current_time = pygame.time.get_ticks()
        if Player1_aggressive_animation_current_time - Player1_aggressive_animation_last_update >= Player1_aggressive_animation_cooldown:
            Player1_frame += 1
            Player1_aggressive_animation_last_update = Player1_aggressive_animation_current_time
            if Player1_frame >= len(Player1_animation_list):
                Player1_frame = 0

    if Player1_action == "idle":
        Player1_animation_list = get_animation("Player1", "idle", Player1_idle_animation_steps)
        Player1_idle_animation_current_time = pygame.time.get_ticks()
        if Player1_idle_animation_current_time - Player1_idle_animation_last_update >= Player1_idle_animation_cooldown:
            Player1_frame += 1
            Player1_idle_animation_last_update = Player1_idle_animation_current_time
            if Player1_frame >= len(Player1_animation_list):
                Player1_frame = 0

    if Player1_action != "jump":
        if Player1_flip == True:
            Player1_image = pygame.transform.flip(Player1_animation_list[Player1_frame], True, False)
        else:
            Player1_image = pygame.transform.flip(Player1_animation_list[Player1_frame], False, False)
    else:
        Player1_image = get_image(Player1_Sprite_Sheet, 3, "jump", 48, 48, 3.2)
        if Player1_flip == True:
            Player1_image = pygame.transform.flip(Player1_image, True, False)
        else:
            Player1_image = pygame.transform.flip(Player1_image, False, False)
        if Player1_y == 655 - 153 and (Player1_move_left == True or Player1_move_right == True) and Player1_attack == False:
            change_action("Player1", "move", True)
        elif Player1_attack == True:
            change_action("Player1", "attack", True)
        elif Player1_y == 655 - 153 and (Player1_move_left == False or Player1_move_right == False) and Player1_attack == False:
            change_action("Player1", "idle", True)
        elif Player1_on_ground == False:
            change_action("Player1", "jump", True)

    if Player2_action == "attack":
        Player2_animation_list = get_animation("Player2", "attack", Player2_attack_animation_steps)
        Player2_attack_animation_current_time = pygame.time.get_ticks()
        if Player2_attack_animation_current_time - Player2_attack_animation_last_update >= Player2_attack_animation_cooldown:
            Player2_frame += 1
            Player2_attack_animation_last_update = Player2_attack_animation_current_time
            if Player2_frame >= 7:
                Player2_frame = 0
                if Player2_on_ground == False:
                    change_action("Player2", "jump", True)
                elif Player2_y == 655 - 153 and (Player2_move_left == True or Player2_move_right == True):
                    change_action("Player2", "move", True)
                else:
                    change_action("Player2", "idle", True)
                Player2_attack = False

    if Player2_action == "move":
        Player2_animation_list = get_animation("Player2", "move", Player2_move_animation_steps)
        Player2_move_animation_current_time = pygame.time.get_ticks()
        if Player2_move_animation_current_time - Player2_move_animation_last_update >= Player2_move_animation_cooldown:
            Player2_frame += 1
            Player2_move_animation_last_update = Player2_move_animation_current_time
            if Player2_frame >= 7:
                Player2_frame = 0

    if Player2_action == "aggressive":
        Player2_animation_list = get_animation("Player2", "aggressive", Player2_aggressive_animation_steps)
        Player2_aggressive_animation_current_time = pygame.time.get_ticks()
        if Player2_aggressive_animation_current_time - Player2_aggressive_animation_last_update >= Player2_aggressive_animation_cooldown:
            Player2_frame += 1
            Player2_aggressive_animation_last_update = Player2_aggressive_animation_current_time
            if Player2_frame >= len(Player2_animation_list):
                Player2_frame = 0

    if Player2_action == "idle":
        Player2_animation_list = get_animation("Player2", "idle", Player2_idle_animation_steps)
        Player2_idle_animation_current_time = pygame.time.get_ticks()
        if Player2_idle_animation_current_time - Player2_idle_animation_last_update >= Player2_idle_animation_cooldown:
            Player2_frame += 1
            Player2_idle_animation_last_update = Player2_idle_animation_current_time
            if Player2_frame >= len(Player2_animation_list):
                Player2_frame = 0

    if Player2_action != "jump":
        if Player2_flip == True:
            Player2_image = pygame.transform.flip(Player2_animation_list[Player2_frame], True, False)
        else:
            Player2_image = pygame.transform.flip(Player2_animation_list[Player2_frame], False, False)
    else:
        Player2_image = get_image(Player2_Sprite_Sheet, 3, "jump", 48, 48, 3.2)
        if Player2_flip == True:
            Player2_image = pygame.transform.flip(Player2_image, True, False)
        else:
            Player2_image = pygame.transform.flip(Player2_image, False, False)
        if Player2_on_ground and (Player2_move_left == True or Player2_move_right == True) and Player2_attack == False:
            change_action("Player2", "move", True)
        elif Player2_attack == True:
            change_action("Player2", "attack", True)
        elif Player2_on_ground and (Player2_move_left == False or Player2_move_right == False) and Player2_attack == False:
            change_action("Player2", "idle", True)
        elif Player2_on_ground == False:
            change_action("Player2", "jump", True)

    Player1_rect = pygame.Rect((Player1_x + 25, Player1_y), (80, 153))
    Player2_rect = pygame.Rect((Player2_x + 25, Player2_y), (80, 153))

    collisions = get_hits(Player1_rect, tile_rects)
    if len(collisions) != 0:
        Player1_y_collisons = True
    elif Player1_y == 655 - 153: 
        Player1_on_ground = True
    else:
        Player1_y_collisons = False
        Player1_on_ground = False
    for tile in collisions:
        if gravity1 > 0:
            Player1_y = tile.top - 140
            Player1_on_ground = True
        elif gravity1 < 0:
            Player1_y = tile.bottom

    collisions = get_hits(Player2_rect, tile_rects)
    if len(collisions) != 0:
        Player2_y_collisons = True
    elif Player2_y == 655 - 153: 
        Player2_on_ground = True
    else:
        Player2_y_collisons = False
        Player2_on_ground = False
    for tile in collisions:
        if gravity2 > 0:
            Player2_y = tile.top - 140
            Player2_on_ground = True
        elif gravity2 < 0:
            Player2_y = tile.bottom



    collisions = get_hits(Player1_rect, tile_rects)
    for tile in collisions:
        if Player1_move_right == True and Player1_on_ground == False and Player1_y_collisons == False:
            Player1_x = tile.left - 153
            Player1_y = Player1_y
        elif Player1_move_left == True and Player1_on_ground == False and Player1_y_collisons == False:
            Player1_x = tile.right
            Player1_y = Player1_y

    collisions = get_hits(Player2_rect, tile_rects)
    for tile in collisions:
        if Player2_move_right == True and Player2_on_ground == False and Player2_y_collisons == False:
            Player2_x = tile.left - 153
            Player2_y = Player2_y
        elif Player2_move_left == True and Player2_on_ground == False and Player2_y_collisons == False:
            Player2_x = tile.right
            Player2_y = Player2_y

    if Player1_health <= 0:
        Player2_victory.preview()
        run = False
    elif Player2_health <= 0:
        Player1_victory.preview()
        run = False

    draw_health_bars("Player1", Player1_health, 20, 20)
    draw_health_bars("Player2", Player2_health, 735, 20)
    
    screen.blit(Player1_image, (Player1_x, Player1_y))
    screen.blit(Player2_image, (Player2_x, Player2_y))

    pygame.display.update()

    clock.tick(60)

    

pygame.quit()
