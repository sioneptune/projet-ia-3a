#####
# File containing the game's graphics
#####

import pygame
from game.core import Arena, Fighter, Bullet

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)


def pg_init():
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)    # problem with display size, FIX IT
    pygame.display.set_caption("Lol I hate life")
    return screen


def run():
    carry_on = True
    clock = pygame.time.Clock()
    screen = pg_init()

    game = Arena()
    game.fighters.append(Fighter())
    player = game.fighters[0]
    player.position = (600, 600)

    while carry_on:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on = False

        # Game logic goes here

        # Draw all the stuff
        screen.fill(GREY)
        render(game, screen)

        clock.tick(60)

    pygame.quit()


def render(arena, screen):
    """Main render function"""
    for f in arena.fighters:
        render_fighter(f, screen)
    pygame.display.flip()


def render_fighter(f, screen):
    """RTFT"""
    renderbox = [f.position[0]-f.health/2, f.position[1]-f.health/2, f.position[0]+f.health/2, f.position[1]+f.health/2]
    pygame.draw.ellipse(screen, RED, renderbox, f.health)


run()
