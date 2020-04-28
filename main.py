import pygame
import sys
import time

display_width = 256
display_height = 223
disp_SIZE = display_width, display_height
# BACKGROUND_COLOR = pygame.Color('white')
FPS = 30


def sprite_sheet(size, file, pos=(0, 0)):

    # Initial Values
    len_sprt_x, len_sprt_y = size  # sprite size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet = pygame.image.load(file).convert()  # Load the sheet
    sheet.set_colorkey((0, 128, 255))
    sheet_rect = sheet.get_rect()
    sprites = []
    print(sheet_rect.height, sheet_rect.width)
    for i in range(0, sheet_rect.height-len_sprt_y, size[1]):  # rows
        print("row")
        for i in range(0, sheet_rect.width-len_sprt_x, size[0]):  # columns
            print("column")
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y,
                                       len_sprt_x, len_sprt_y))  # find sprite you want
            # grab the sprite you want
            sprite = sheet.subsurface(sheet.get_clip())
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    print(sprites)
    return sprites


class backGround(pygame.sprite.Sprite):
    def __init__(self, image_file, size, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class obstruction(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(obstruction, self).__init__()
        self.rect = pygame.Rect(x, y, w, h)

    def getRect(self):
    	return self.rect


class mySprite(pygame.sprite.Sprite):
    def __init__(self, image_file, sprite_size, def_pos):
        super(mySprite, self).__init__()

        # sprite_size = width*height
        self.sprites = sprite_sheet(sprite_size, image_file)

        self.images = []
        # self.images.append(pygame.image.load('walk1.png'))
        for sprite in self.sprites:
            self.images.append(sprite)

        self.index = 0
        self.counter = 0
        self.framecap = FPS/5

        self.image = self.images[self.index]

        self.x, self.y = def_pos
        self.w, self.h = sprite_size

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def loop(self):
        self.counter += 1
        if self.counter >= self.framecap:
            self.index += 1
            self.counter = 0

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]

    def play(self):
        self.counter += 1
        if self.counter >= self.framecap:
            self.index += 1
            self.counter = 0

        if self.index >= len(self.images):
            return 1

        self.image = self.images[self.index]

    def resetIndex(self):
        self.index = 0

    def move(self, newpos):
        self.x, self.y = newpos
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def getRect(self):
    	return self.rect


class Character():
    def __init__(self, name, position, velocity):
        self.name = name
        self.state = None
        self.states = []
        self.posx, self.posy = position
        self.vx, self.vy = velocity

    def addState(self, s_name, s_loop, image_file, sprite_size, s_nextstate=None):
        a_state = State(s_name, s_loop, (self.posx, self.posy),
                        image_file, sprite_size, s_nextstate)
        self.states.append(a_state)

    def updateState(self, newstate):
        self.state = newstate

    def getState(self):
        return self.state

    def getStates(self):
        return self.states

    def findState(self, aname):
        for state in self.states:
            if(state.getName() == aname):
                match = state
        return match

    def move(self, newpos):
        self.posx, self.posy = newpos
        self.state.move(newpos)

    def getLoc(self):
        return self.posx, self.posy

    def getVel(self):
        return self.vx, self.vy


class State():
    def __init__(self, name, loop, def_pos, image_file, sprite_size, nextstate=None):
        self.name = name
        self.loop = loop
        self.nextstate = nextstate
        self.default_position = def_pos
        self.sprite = mySprite(image_file, sprite_size, self.default_position)

    def getSprite(self):
        return self.sprite

    def getLoop(self):
        return self.loop

    def nextState(self):
        return self.nextstate

    def getName(self):
        return self.name

    def move(self, newpos):
        self.sprite.move(newpos)


def col_check(x, y, w, h, x2, y2, w2, h2):
	if (x < (x2 + w2) and (x + w) > x2 and y < (y2 + h2) and (h + y) > y2):
		print("COLLIDED!!!")


def main():
    pygame.init()
    screen = pygame.display.set_mode(disp_SIZE)

    clock = pygame.time.Clock()

    bg = backGround("Resources/images/cut/bg.png", (disp_SIZE), (0, 0))
    screen.fill((255, 255, 255))
    screen.blit(bg.image, bg.rect)

    # sprite size
    swidth = 43
    sheight = 46

    # default spawn
    dx = 100
    dy = 100

    # Declaring Crystal Snail
    cs = Character("Crystal Snail", (dx, dy), (10, 10))

    # Declaring states for Crystal Snail
    alist = cs.getStates()
    cs.addState("Stand", True, "Resources/images/cut/stand.png",
                (swidth, sheight))
    cs.addState("Intro", False, "Resources/images/cut/intro.png",
                (swidth, sheight), cs.findState("Stand"))
    cs.updateState(cs.findState("Intro"))
    for item in alist:
        print(item.getName())

    # cs = mySprite("Resources/images/cut/intro.png", (swidth, sheight))
    # cs_group = pygame.sprite.Group(cs)

    # Declaring Floors & Walls
    floor = obstruction(0, 191, 255, 223)

    # For continuous movement
    move_right = move_left = move_up = move_down = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cs.updateState(cs.findState("Intro"))
                elif event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_UP:
                    move_up = True
                elif event.key == pygame.K_DOWN:
                    move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_UP:
                    move_up = False
                elif event.key == pygame.K_DOWN:
                    move_down = False
        # Check for movement
        if(move_right):
            x, y = cs.getLoc()
            vx, vy = cs.getVel()
            x += vx
            cs.move((x, y))
        elif(move_left):
            x, y = cs.getLoc()
            vx, vy = cs.getVel()
            x -= vx
            cs.move((x, y))
        elif(move_up):
            x, y = cs.getLoc()
            vx, vy = cs.getVel()
            y -= vy
            cs.move((x, y))
        elif(move_down):
            x, y = cs.getLoc()
            vx, vy = cs.getVel()
            y += vy
            cs.move((x, y))

        # State transitions
        cs_curr_sprite = cs.getState().getSprite()
        cs_group = pygame.sprite.Group(cs_curr_sprite)
        if(cs.getState().getLoop()):
            cs_curr_sprite.loop()
        elif(not cs.getState().getLoop()):
            done = cs_curr_sprite.play()
            if(done):
                cs.updateState(cs.getState().nextState())
                cs_curr_sprite.resetIndex()
        obs_group = pygame.sprite.Group(floor)
        # Check functions
        # print(cs.getState().getName())
        # print(pygame.mouse.get_pos())

        # If CS collides with floor
        a, b, c, d = cs.getState().getSprite().getRect()
        e, f, g, h = floor.getRect()
        col_check(a, b, c, d, e, f, g, h)
        # if pygame.sprite.spritecollide(cs.getState().getSprite(), obs_group, True):
        # 	print(cs.getState().getSprite().getRect(), floor.getRect())
        # 	print("cs collided with floor")

        screen.fill((255, 255, 255))
        screen.blit(bg.image, bg.rect)
        cs_group.draw(screen)
        pygame.display.update()

        clock.tick(FPS)


main()
