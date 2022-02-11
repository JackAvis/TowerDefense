import sys
import pygame as py
from vector import Vector
from gm import collision
from enemy import Enemy
from fighter import Fighter
from projectile import Projectile
from trap import Trap
import random
import pygame_gui
py.init()



# Window
size = width, height = 640, 480

# RGBA constants
green = 12, 10,154 ,0
default_color = 12, 200, 10
enemy_colors = [[242, 5, 25], [230, 242, 5], [242, 155, 5], [167, 5, 242]]
road = 200, 54, 164
p_color = 200, 200, 0
color = 100, 50, 20, 10
button = py.Rect(490, 160, 20, 20) 
button_color = [242, 5, 25]
trap_button_color = [242, 5, 25]
p_speed_button_color = [242, 5, 25]
p_speed_button = py.Rect(25, 75, 20, 20) 
p_size_button = py.Rect(25, 145, 20, 20) 
trap_button = py.Rect(490, 230, 20, 20) 


FRAMES = 60

enemy_position: Vector = Vector(50, 200)
enemy_list: list[Enemy] = []
fighter_list: list[Fighter] = []
projectile_list: list[Projectile] = []
trap_list: list[Trap] = []
p_list_fixed: list[Projectile] = []

# Makes Screen
screen = py.display.set_mode(size)

# Game clock
clock = py.time.Clock()

#Keeps game loop running
playing = True

#Handles GUI
manager = pygame_gui.UIManager((width, height))


#UI Elements for GUI
hp = 15

health = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 5), (210, 30)),
                text=f'Health: {hp}',
                manager=manager) 
lv = 0
level = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 30), (210, 30)),
                text='Level: ' + str(lv),
                manager=manager) 

g = 10000
gold = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 60), (210, 30)),
                text='Gold: ' + str(g),
                manager=manager) 
shop = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 95), (210, 30)),
                text='SHOP',
                manager=manager) 
place_ui = "(Not Placing)"
trap_place_ui = "(Not Placing)"
soldier = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 130), (210, 30)),
                text='SOLDIER: ' + "10g",
                manager=manager) 
placement = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 160), (210, 30)),
                text="placement button:" + str(place_ui),
                manager=manager) 
trap = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 200), (210, 30)),
                text='TRAP: ' + "5g",
                manager=manager) 
trap_placement = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 230), (210, 30)),
                text="        " + str(trap_place_ui),
                manager=manager) 
upgrades = pygame_gui.elements.UILabel(relative_rect=py.Rect((0, 5), (210, 30)),
                text="UPGRADES",
                manager=manager) 
p_speed_cost = 20
p_speed_level = 0
p_size = 5
projectile_speed = pygame_gui.elements.UILabel(relative_rect=py.Rect((0, 40), (210, 30)),
                text=f"Faster Projectiles:  {p_speed_cost}g",
                manager=manager) 
blank_p = pygame_gui.elements.UILabel(relative_rect=py.Rect((0, 70), (210, 30)),
                text=f"      upgrade level: {p_speed_level}",
                manager=manager) 
p_size_cost = 15
p_size_level = 0
projectile_size = pygame_gui.elements.UILabel(relative_rect=py.Rect((0, 110), (210, 30)),
                text=f"Larger Projectiles:  {p_size_cost}g",
                manager=manager) 
blank_b = pygame_gui.elements.UILabel(relative_rect=py.Rect((0, 140), (210, 30)),
                text=f"      upgrade level: {p_size_level}",
                manager=manager) 

# Warning message
warning = pygame_gui.elements.UILabel(relative_rect=py.Rect((430, 200), (210, 0)),
                text='',
                manager=manager) 
frame = 0
warning_track = 0
list_index = 0
warning_bool = False
enemies_killed = 0
enemies_killed_list = []
p_speed = 2.0
placing = False
trap_placing = False
z = 0
t = 0
o = 0

# Game Loop
while playing:
    pos = py.mouse.get_pos()
    
    
    # Games internal clock, sets number of frames run per second
    clock.tick(FRAMES)
    frame += 1
    if warning_bool == True:
        warning_track += 1
        if warning_track % 120 == 1:
            warning_bool = False
            warning_track == 0
            warning.set_dimensions((0, 0))
    if frame % 120 == 1 and frame > 0:
        if lv <= 2:
            enemy_list.append(Enemy(Vector(300, .01), enemy_colors[random.randint(0, 0)], random.randint(1, 1), 2, frame))
        if lv >= 3:
            enemy_list.append(Enemy(Vector(300, .01), enemy_colors[random.randint(0, 1)], random.randint(1, 1), 2, frame))
        if lv >= 4:
            enemy_list.append(Enemy(Vector(300, .01), enemy_colors[random.randint(0, 2)], random.randint(1, 2), 3, frame))
        if lv >= 5:
            enemy_list.append(Enemy(Vector(300, .01), enemy_colors[random.randint(0, 3)], random.randint(2, 3 + int(lv *.2 )), 2 + int(lv * .2), frame))




        

    # Tracks player interaction
    for event in py.event.get():
        if event.type == py.QUIT: sys.exit()
        # Places fighter if game manager agrees
        if event.type == py.MOUSEBUTTONUP:
            pos = py.mouse.get_pos()
            if g >= 10 and button.collidepoint(pos) == False and placing == True and p_speed_button.collidepoint(pos) == False and p_size_button.collidepoint(pos) == False and trap_button.collidepoint(pos) == False:
                fighter_list.append(Fighter(Vector(pos[0], pos[1]), default_color))
                g -= 10
            if g >= 5 and button.collidepoint(pos) == False and trap_placing == True and p_speed_button.collidepoint(pos) == False and p_size_button.collidepoint(pos) == False and trap_button.collidepoint(pos) == False:
                trap_list.append(Trap(Vector(pos[0], pos[1]), [0,0,0]))
                g -= 5
            else:
                if button.collidepoint(pos) == False and placing == True and g < 10:
                    warning.set_position((pos[0], pos[1]))
                    warning.set_dimensions((300, 30))
                    warning.set_text("Not Enough Gold!")
                    warning_bool = True
            if trap_button.collidepoint(pos) and trap_placing == False:
                trap_placing = True
                trap_button_color = [167, 5, 242]
            else:
                if trap_button.collidepoint(pos) and trap_placing == True:
                    trap_placing = False
                    trap_button_color = [242, 5, 25]
            if button.collidepoint(pos) and placing == False:
                placing = True
                button_color = [167, 5, 242]
            else:
                if button.collidepoint(pos) and placing == True:
                    placing = False
                    button_color = [242, 5, 25]
            if p_speed_button.collidepoint(pos) == True and g >= p_speed_cost:
                p_speed = p_speed + p_speed * .2
                p_speed_cost = int(p_speed_cost + p_speed_cost * .2)
                p_speed_level += 1
                g -= p_speed_cost
            else:
                if p_speed_button.collidepoint(pos) == True or p_size_button.collidepoint(pos) == True and g < p_size_cost:
                    warning.set_position((pos[0], pos[1]))
                    warning.set_dimensions((300, 30))
                    warning.set_text("Not Enough Gold!")
                    warning_bool = True
            if p_size_button.collidepoint(pos) == True and g >= p_size_cost:
                p_size = p_size + p_size * .2
                p_size_cost = int(p_size_cost + p_size_cost * .2)
                p_size_level += 1
                g -= p_size_cost
            else:
                if p_size_button.collidepoint(pos) == True and g < p_speed_cost:
                    warning.set_position((pos[0], pos[1]))
                    warning.set_dimensions((300, 30))
                    warning.set_text("Not Enough Gold!")
                    warning_bool = True

    screen.fill(green)
     
    r_x = 250
    r_y = 500
    # ROAD
    py.draw.polygon(screen, road, [(r_x, .01), (r_x + 100, .01), (r_x + 100, r_y), (r_x, r_y)])
    # Middle Rect
   
  
    if placing == True:
        place_ui = "(Placing!)"
    else:
        if placing == False:
            place_ui = "(Not placing)"
    if trap_placing == True:
        trap_place_ui = "(Placing!)"
    else:
        if trap_placing == False:
            trap_place_ui = "(Not placing)"
  
    for fighter in fighter_list:
        if fighter.position.x < 250 or fighter.position.x > 350:
            py.draw.circle(screen, fighter.color, (fighter.position.x, fighter.position.y), 20)
        else:
            if placing == True and button.collidepoint(pos) == False:
                fighter_list.remove(fighter)
                warning.set_position((pos[0], pos[1]))
                warning.set_dimensions((300, 30))
                warning_bool = True
                warning.set_text('Please place fighter outside of path')
                g += 10
        if len(enemy_list) > 0 and frame % 60 == 1 and frame > 0:
            projectile_list.append(Projectile(Vector(fighter.position.x, fighter.position.y), p_color, p_speed, enemy_list[0]))
        for projectile in projectile_list:
            py.draw.circle(screen, projectile.color, (projectile.position.x, projectile.position.y), p_size)
            if projectile.enemy in enemy_list:
                if len(enemy_list) > 0:
                    projectile.unit_vector = projectile.move_projectile(Vector(enemy_list[0].position.x, enemy_list[0].position.y))
                    if projectile.enemy.position.x > 1:
                        z = projectile.enemy.position.x
                    if projectile.enemy.position.y > 1:
                        t = projectile.enemy.position.y
            else:

                projectile.move_projectile(Vector(projectile.enemy.position.x, projectile.enemy.position.y))

                projectile.enemy.position.x += projectile.unit_vector.x * 1 / len(projectile_list) * 5
                projectile.enemy.position.y += projectile.unit_vector.y * 1 / len(projectile_list) * 5
                   
                if fighter.position.x > 250 and projectile.position.x < 250 or fighter.position.x < 350 and projectile.position.x > 350:
                    projectile_list.remove(projectile)
            if len(enemy_list) > 0:
                if collision(projectile.position, enemy_list[0].position) == True:
                    projectile_list.remove(projectile)
                    enemy_list[0].health -= 1
                    if enemy_list[0].health <= 0:
                        enemy_list.remove(enemy_list[0])
                        enemies_killed += 1
                        g += 5
                    

    for trap in trap_list:
        if trap.position.x > 250 or trap.position.x < 350:
            py.draw.circle(screen, trap.color, (trap.position.x, trap.position.y), 20)
        else:
            if placing == True and button.collidepoint(pos) == False:
                trap_list.remove(trap)
                warning.set_position((pos[0], pos[1]))
                warning.set_dimensions((300, 30))
                warning_bool = True
                warning.set_text('Please place trap inside of path')
                g += 5
        if len(enemy_list) > 0:
            if collision(trap.position, enemy_list[0].position) == True:
                trap_list.remove(trap)
                enemy_list[0].health -= 3
                if enemy_list[0].health <= 0:
                    enemy_list.remove(enemy_list[0])
                    enemies_killed += 1
                    g += 2.5
    for enemy in enemy_list:
        py.draw.circle(screen, enemy.color, (enemy.position.x, enemy.position.y), 20)
        enemy.move_enemy(Vector(r_x + 50, 600))
        if enemy.health == 0:
            enemy.position.y == 600
        if enemy.position.y > 500:
            enemy_list.remove(enemy)   
            hp -= 1 
                
    if enemies_killed % 5 == 1 and enemies_killed not in enemies_killed_list:
        enemies_killed_list.append(enemies_killed)
        lv += 1
    if g < 0:
        g = 0
    
    #GUI Updates
    health.set_text(f"Health: {hp}")
    level.set_text("Level: " + str(lv))
    gold.set_text("Gold: " + str(g))
    placement.set_text(f"         {place_ui}")
    projectile_speed.set_text(f"Faster Projectiles:  {p_speed_cost}g")
    blank_p.set_text(f"      upgrade level: {p_speed_level}")
    projectile_size.set_text(f"Larger Projectiles:  {p_size_cost}g")
    blank_b.set_text(f"      upgrade level: {p_size_level}")
    trap_placement.set_text("        " + str(trap_place_ui))
    manager.process_events(event)
    manager.update(20)
    manager.draw_ui(screen)
    py.draw.rect(screen, button_color, button)
    py.draw.rect(screen, p_speed_button_color, p_speed_button)
    py.draw.rect(screen, p_speed_button_color, p_size_button)
    py.draw.rect(screen, trap_button_color, trap_button)
    # Game Over Screen

    if hp == 0:
        warning = pygame_gui.elements.UILabel(relative_rect=py.Rect((200, 130), (210, 80)),
                text=f'Game Over!',
                manager=manager) 
        level_ui = pygame_gui.elements.UILabel(relative_rect=py.Rect((200, 180), (210, 80)),
                text=f'level achieved: {lv}',
                manager=manager) 
        enemy_ui = pygame_gui.elements.UILabel(relative_rect=py.Rect((200, 230), (210, 80)),
                text=f'enemies killed: {enemies_killed}',
                manager=manager) 

        py.display.update()

    else:
        if hp > 0:
            py.display.update()
    #Flips all the updates from the loop onto screen
  