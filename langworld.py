#!/usr/bin/env python

import pygame, os, sys, operator

pygame.init()

# 0 = grass, 1 = stone, 2 = wood, 3 = water
MAP1_TERRAIN = ["0020",
"0020",
"1121",
"3323",
"1121",
"1121"]

# 0 = neutral, 1 = friend, 2 = badguy, 3 = shop
MAP1_SPRITES = ["0002",
"0000",
"0000",
"0000",
"0000",
"0000"]

MAP1 = {"terrain":MAP1_TERRAIN, "sprites":MAP1_SPRITES}

TILE_IMAGES = ["./data/images/" + img + ".png" for img in ["grass", "stone", "wood", "water"]]
PLAYER_IMAGE = "./data/images/" + "boy" + ".png"

KEYS = {"left"       : [pygame.K_a,pygame.K_LEFT],
        "right"      : [pygame.K_d,pygame.K_RIGHT],
        "up"         : [pygame.K_w,pygame.K_UP],
        "down"       : [pygame.K_s,pygame.K_DOWN],
        "quit"       : [pygame.K_q,pygame.K_ESCAPE]}

SPRITES = {}
SPRITES["badguy"] = {"image":"./data/images/badguy.png", "status":"enemy", "hitpoints":15, "aggression": 5}
SPRITE_IMAGES = [None, None, SPRITES["badguy"]["image"], None]

class Map:
    def __init__(self, map):
        self.map_terrain = map["terrain"]
        self.map_sprites = map["sprites"]
        self.map_player_pos = (0, 0)
        self.has_collision = False

    def _blit(self, screen, map_list, image_list, tile_width = 101, tile_height = 121, border_width = 38, tile_max = 24, column_max = 4):
        columns = 0
        rows = 0
        tile_count = 0

        for string in map_list:
            if tile_count == tile_max:
                    break
            for char in string:
                if image_list[int(char)] is not None:
                    screen.blit(pygame.image.load(image_list[int(char)]), (border_width + (tile_width*columns), tile_height*rows))
                columns += 1
                tile_count += 1
                if (columns == 4):
                    columns = 0
                    rows += 1

    def blit(self, screen):
        columns = 0
        rows = 0
        tile_count = 0
        tile_width = 101
        tile_height = 121
        border_width = 38

        self._blit(screen, self.map_terrain, TILE_IMAGES)
        self._blit(screen, self.map_sprites, SPRITE_IMAGES)

        #pygame.draw.rect(screen, (255,255,255), (38,800,404,800))

    def get_collisions(self):
        #return a collision if a sprite is in current player position on grid
        #print self.map_sprites[self.map_player_pos[0]][self.map_player_pos[1]]

        #todo: figure out why [1][0] position is detecting - x and y coords messed up?
        #todo, perhaps get rid of conditional and merge this method with self.collide
        #todo, character is returning None when world.dialog is called, not sure why
        if (int(self.map_sprites[self.map_player_pos[1]][self.map_player_pos[0]])) > 0:
            if self.has_collision is False:
                self.has_collision = True
                self.collisions = (self.map_player_pos[1], self.map_player_pos[0])
                return int(self.map_sprites[self.map_player_pos[1]][self.map_player_pos[0]])
        else:
            return 0

    def set_map_player_pos(self, player_rect):
        '''Accepts the player's rect (possibly from player.get_rect) as an argument
        then calculates and returns player position on map (i.e. the 4x6 grid).
        Useful for collision detection.
        '''
        self.map_player_pos = (player_rect.left / 101, player_rect.top / 121)


class Player:
    def __init__(self):
        self.pos = [0,0]
        self.rect = pygame.Rect(list(self.pos),(110, 63))

        self.clock = pygame.time.Clock()

    def get_rect(self):
        return self.rect

    def get_grid_position(self):
        pass

    def blit(self, screen):
        screen.blit(pygame.image.load(PLAYER_IMAGE), self.rect)

    def cycle(self):
        self.clock.tick()

    def move(self, direction):
        (self.rect.left, self.rect.top) = tuple(map(operator.add, (self.rect.left, self.rect.top), direction))

class World:
    def __init__(self):
        self.screen = pygame.display.set_mode((480,800))
        self.image = pygame.Surface((480,800))
        self.active_map = Map(MAP1)
        self.clock = pygame.time.Clock()
        self.player = Player()

    def blit(self):
        self.image.fill((128,128,128))
        self.active_map.blit(self.image)
        self.player.blit(self.image)
        self.screen.blit(self.image,(0,0))
        pygame.display.flip()

    def cycle(self):
        self.active_map.set_map_player_pos(self.player.get_rect())
        collision = self.active_map.get_collisions()
        if collision > 0:
            self.dialog(self.player, collision)

    def inputs(self):
        pygame.event.pump()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
        for i in KEYS["left"]:
            if pygame.key.get_pressed()[i]:
                self.player.move((-10, 0))
                break
        for i in KEYS["right"]:
            if pygame.key.get_pressed()[i]:
                self.player.move((10, 0))
                break
        for i in KEYS["up"]:
            if pygame.key.get_pressed()[i]:
                self.player.move((0, -10))
                break
        for i in KEYS["down"]:
            if pygame.key.get_pressed()[i]:
                self.player.move((0, 10))
                break

    def dialog(self, a, b):
        print "dialog between "
        print a
        print " and "
        print b

    def run(self):
        while True:
            self.clock.tick(30)
            self.inputs()
            self.cycle()
            self.blit()

w = World()
w.run()
