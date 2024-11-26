import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ship Sailing Adventure")

clock = pygame.time.Clock()
FPS = 60

ship_width, ship_height = 50, 30
ship_x, ship_y = 50, HEIGHT // 2
ship_speed = 5

obstacle_width, obstacle_height = 50, 50

background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

ship_image = pygame.image.load("player_ship.png").convert_alpha()
enemy_ship_image = pygame.image.load("enemy_ship.png").convert_alpha()
bomb_image = pygame.image.load("bomb.png").convert_alpha()

ship_image = pygame.transform.scale(ship_image, (ship_width, ship_height))
enemy_ship_image = pygame.transform.scale(enemy_ship_image, (obstacle_width, obstacle_height))
bomb_image = pygame.transform.scale(bomb_image, (20, 20))

running = True
score = 0
font = pygame.font.Font(None, 36)

obstacles = []
bombs = []

base_obstacle_speed = 5
base_bomb_speed = 7

def draw_text(text, x, y):
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (x, y))

def move_ship(keys, y):
    if keys[pygame.K_UP] and y > 0:
        y -= ship_speed
    if keys[pygame.K_DOWN] and y < HEIGHT - ship_height:
        y += ship_speed
    return y

def create_obstacle():
    return {
        "x": WIDTH + random.randint(50, 200),
        "y": random.randint(0, HEIGHT - obstacle_height),
        "throws_bombs": random.choice([True, False]),
        "thrown_bomb": False
    }

while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ship_y = move_ship(keys, ship_y)

    obstacle_speed = base_obstacle_speed + score // 10
    bomb_speed = base_bomb_speed + score // 10

    if random.randint(1, 60) == 1:
        obstacles.append(create_obstacle())

    for obstacle in obstacles[:]:
        obstacle["x"] -= obstacle_speed
        if obstacle["throws_bombs"] and not obstacle["thrown_bomb"] and random.randint(1, 100) == 1:
            bombs.append({"x": obstacle["x"], "y": obstacle["y"] + obstacle_height // 2})
            obstacle["thrown_bomb"] = True
        if obstacle["x"] < -obstacle_width:
            obstacles.remove(obstacle)
            score += 1

    for bomb in bombs[:]:
        bomb["x"] -= bomb_speed
        if bomb["x"] < -20:
            bombs.remove(bomb)

    ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)

    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle_width, obstacle_height)
        if ship_rect.colliderect(obstacle_rect):
            running = False

    for bomb in bombs:
        bomb_rect = pygame.Rect(bomb["x"], bomb["y"], 20, 20)
        if ship_rect.colliderect(bomb_rect):
            running = False

    screen.blit(ship_image, (ship_x, ship_y))

    for obstacle in obstacles:
        screen.blit(enemy_ship_image, (obstacle["x"], obstacle["y"]))

    for bomb in bombs:
        screen.blit(bomb_image, (bomb["x"], bomb["y"]))

    draw_text(f"Score: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
