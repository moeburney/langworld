import pygame, os, sys, operator

pygame.init()

# this is map 1, it can go into a separate file once we have more maps.

MAP1 = ["0020",
"0020",
"1121",
"3323",
"1121",
"1121"]

# these are constant dicts for tile images

TILE_IMAGES = ["./data/images/" + img + ".png" for img in ["grass", "stone", "wood", "water"]]
PLAYER_IMAGE = "./data/images/" + "boy" + ".png"
KEYS = {"left"       : [pygame.K_a,pygame.K_LEFT],
        "right"      : [pygame.K_d,pygame.K_RIGHT],
        "up"         : [pygame.K_w,pygame.K_UP],
        "down"       : [pygame.K_s,pygame.K_DOWN],
        "quit"       : [pygame.K_q,pygame.K_ESCAPE]}

class Map:
    def __init__(self, map):
        self.map = map
        self.map_tiles = []

    def blit(self, screen):
        columns = 0
        rows = 0
        tile_count = 0
        tile_width = 101
        tile_height = 121
        border_width = 38

        for string in self.map:
            if tile_count == 24:
                    break
            for char in string:
                screen.blit(pygame.image.load(TILE_IMAGES[int(char)]), (border_width + (tile_width*columns), tile_height*rows))
                columns += 1
                tile_count += 1
                if (columns == 4):
                    columns = 0
                    rows += 1

        #pygame.draw.rect(screen, (255,255,255), (38,800,404,800))

class Player:
    def __init__(self):
        self.pos = [0,0]
        self.rect = pygame.Rect(list(self.pos),(110, 63))

        self.clock = pygame.time.Clock()

    def get_rect(self):
        return self.rect

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
        pass

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

    def run(self):
        while True:
            self.clock.tick(30)
            self.inputs()
            self.blit()

w = World()
w.run()
