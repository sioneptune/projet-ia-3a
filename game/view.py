#####
# File containing the game's graphics
#####

import pygame
from game.core import Arena, Fighter, Bullet
from math import cos, sin, radians

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)


def pg_init():
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)    # problem with display size, FIX IT
    pygame.display.set_caption("Lol I kinda tolerate life")
    return screen


def events(game, player, screen):
    """Manages the events and movements of the objects"""

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turn(False)
        print("pressed left")
        print(player.direction)
    if keys[pygame.K_RIGHT]:
        player.turn(True)
        print("turned right")
        print(player.direction)
    if keys[pygame.K_UP]:
        player.move()
        print("moved")
        print(player.position)
    if keys[pygame.K_g]:
        player.health += 10
    if keys[pygame.K_s]:
        player.health -= 10
    if keys[pygame.K_f]:
        player.shoot()
        print("shot")

    for b in game.bullets:
        if 700 >= b.position[0] >= 0 and 700 >= b.position[1] >=0:
            b.move()
            print("BULLET")
        else:
            game.bullets.remove(b)
            print("BULLET GOT DED LOL")


def run():
    carry_on = True
    clock = pygame.time.Clock()
    screen = pg_init()

    game = Arena()
    player = Fighter((600, 600), game)
    game.fighters.append(player)
    game.fighters.append(Fighter((100, 100), game))
    game.fighters.append(Fighter((600, 100), game))
    game.fighters.append(Fighter((100, 600), game))

    player.turn(False)
    player.move()

    while carry_on:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False
        events(game, player, screen)

        # Game logic goes here

        # Draw all the stuff
        screen.fill(GREY)
        render(game, screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def render(arena, screen):
    """Main render function"""
    render_fighter(arena.fighters[0], screen, BLUE)
    render_fighter(arena.fighters[1], screen, RED)
    render_fighter(arena.fighters[2], screen, YELLOW)
    render_fighter(arena.fighters[3], screen, GREEN)

    for bullet in arena.bullets:
        render_bullet(bullet, screen)


def render_fighter(f, screen, color):
    """RTFT"""
    renderbox = [f.position[0]-f.health/4, f.position[1]-f.health/4, f.health/2, f.health/2]
    pygame.draw.ellipse(screen, color, renderbox)
    pygame.draw.line(screen, BLACK, list(f.position), [f.position[0] + f.health/3 * cos(radians(f.direction)),
                                                       f.position[1] + f.health/3 * sin(radians(f.direction))],
                     int(f.health/20))


def render_bullet(b, screen):
    pygame.draw.ellipse(screen, BLACK, [b.position[0] - 5, b.position[1] - 5, 10, 10])

run()
