import pygame

class Character():
    def __init__(self, name, position, colorkey=(0, 0, 0), facing="left"):
        self.name = name
        self.state = None
        self.states = []
        self.posx, self.posy = position
        self.vx, self.vy = (0, 0)
        self.facing = facing
        self.colorkey = colorkey

    def addState(self, s_name, s_loop, image_file, sprite_size, s_nextstate=None):
        a_state = State(s_name, s_loop, (self.posx, self.posy),
                        image_file, sprite_size, s_nextstate, self.colorkey)
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

    def setVel(self, newv):
        self.vx, self.vy = newv

    def getVel(self):
        return self.vx, self.vy

    def setFacing(self, orientation):
        self.facing = orientation
        self.getState().changeDirection(self.facing)
    
    def getFacing(self):
        return self.facing

class State(pygame.sprite.Sprite):
    def __init__(self, name, loop, def_pos, image_file, sprite_size, nextstate=None, colorkey=(0, 0, 0)):
        super(State, self).__init__()

        self.name = name
        self.loopcon = loop
        self.nextState = nextstate
        self.colorkey = colorkey

        # sprite_size = width*height
        self.sprites = sprite_sheet(sprite_size, image_file, (0, 0), self.colorkey)

        self.images_left = []
        self.images_right = []
        # self.images.append(pygame.image.load('walk1.png'))
        for sprite in self.sprites:
            self.images_left.append(sprite.getImage())
            self.images_right.append(pygame.transform.flip(sprite.getImage(), True, False))

        self.index = 0
        self.framecounter = 0
        self.image = self.images_left[self.index]

        self.x, self.y = def_pos
        self.w, self.h = sprite_size

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.facing = "left"

    def loop(self):
        self.index += 1

        if self.facing == "left":
            # if self.index >= len(self.images_left):
            #     self.index = 0
            # self.image = self.images_left[self.index]
            if self.index >= self.sprites[self.framecounter].getMFT():
                self.index = 0
                self.framecounter += 1

            if self.framecounter >= len(self.sprites):
                self.framecounter = 0

            self.image = self.images_left[self.framecounter]
            
        elif self.facing == "right":
            # if self.index >= len(self.images_right):
            #     self.index = 0
            # self.image = self.images_right[self.index]
            if self.index >= self.sprites[self.framecounter].getMFT():
                self.index = 0
                self.framecounter += 1

            if self.framecounter >= len(self.sprites):
                self.framecounter = 0

            self.image = self.images_right[self.framecounter]
            

    def play(self):
        self.index += 1
        if self.framecounter >= len(self.sprites):
            return 1
        elif self.index >= self.sprites[self.framecounter].getMFT():
                self.index = 0
                self.framecounter += 1
        
        if self.facing == "left":
            # if self.index >= len(self.images_left):
            #     self.image = self.images_left[len(self.images_left)-1]    
            #     return 1
            # self.image = self.images_left[self.index]

            if self.framecounter >= len(self.sprites):
                self.image = self.images_left[len(self.images_left)-1]
                return 1
            
            self.image = self.images_left[self.framecounter]

        elif self.facing == "right":
            # if self.index >= len(self.images_right):
            #     self.image = self.images_right[len(self.images_right)-1]    
            #     return 1
            # self.image = self.images_right[self.index]
            
            if self.framecounter >= len(self.sprites):
                self.image = self.images_right[len(self.images_right)-1]    
                return 1

            self.image = self.images_right[self.framecounter]

    def resetIndex(self):
        self.index = 0
        self.framecounter = 0

    def move(self, newpos):
        self.x, self.y = newpos
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def getRect(self):
        return self.rect

    def changeDirection(self, orientation):
        if self.facing == orientation:
            self.facing = orientation
        elif self.facing != orientation:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = orientation
    
    def getLoop(self):
        return self.loopcon
    
    def getSprites(self):
        return self.sprites
    
    def getName(self):
        return self.name
    
    def getnextState(self):
        return self.nextState
    
    def rotateImg(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)

    def checkLastFrame(self):
        return self.framecounter == len(self.sprites)-1
                
class spriteFrame(pygame.sprite.Sprite):
    def __init__(self, image):
        super(spriteFrame, self).__init__()
        self.mft = 1 # max frame timer
        self.image = image
    
    def setMFT(self, duration):
        self.mft = duration
    
    def getMFT(self):
        return self.mft

    def getImage(self):
        return self.image


def sprite_sheet(size, file, pos=(0, 0), colorkey=(0, 0, 0)):

    # Initial Values
    len_sprt_x, len_sprt_y = size  # sprite size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet = pygame.image.load(file).convert()  # Load the sheet
    # Filters out background color
    sheet.set_colorkey(colorkey)
    sheet_rect = sheet.get_rect()
    sprites = []
    print(sheet_rect.height, sheet_rect.width)
    for i in range(0, sheet_rect.height-len_sprt_y, size[1]):  # rows
        # print("row")
        for i in range(0, sheet_rect.width-len_sprt_x, size[0]):  # columns
            # print("column")
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y,
                                       len_sprt_x, len_sprt_y))  # find sprite you want
            # grab the sprite you want
            sprite = sheet.subsurface(sheet.get_clip())
            spriteframe = spriteFrame(sprite) # Inititates single frame into an spriteFrame object
            sprites.append(spriteframe)
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

class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image_file, colorkey=(0, 0, 0)):
        super(projectile, self).__init__()
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0
        self.w = w
        self.h = h
        self.colorkey = colorkey
        self.sprites = sprite_sheet((w, h), image_file, (0, 0), self.colorkey)
        self.images_left = []
        self.images_right = []
        for sprite in self.sprites:
            self.images_left.append(sprite.getImage())
            self.images_right.append(pygame.transform.flip(sprite.getImage(), True, False))

        self.index = 0
        self.framecounter = 0
        self.image = self.images_left[self.index]

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.facing = "left"
    
    def getRect(self):
        return self.rect
    
    def setSpawn(self, loc):
        x, y = loc
        self.rect = pygame.Rect(x, y, self.w, self.h)

    def setVel(self, vel):
        self.vx, self.vy = vel
    
    def getVel(self):
        return self.vx, self.vy
    
    def getLoc(self):
        x, y, w, h = self.rect
        return x, y
    
    def move(self, loc):
        self.x, self.y = loc
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    
    def loop(self):
        self.index += 1

        if self.facing == "left":
            # if self.index >= len(self.images_left):
            #     self.index = 0
            # self.image = self.images_left[self.index]
            if self.index >= self.sprites[self.framecounter].getMFT():
                self.index = 0
                self.framecounter += 1

            if self.framecounter >= len(self.sprites):
                self.framecounter = 0

            self.image = self.images_left[self.framecounter]
            
        elif self.facing == "right":
            # if self.index >= len(self.images_right):
            #     self.index = 0
            # self.image = self.images_right[self.index]
            if self.index >= self.sprites[self.framecounter].getMFT():
                self.index = 0
                self.framecounter += 1

            if self.framecounter >= len(self.sprites):
                self.framecounter = 0

            self.image = self.images_right[self.framecounter]
    
    def resetIndex(self):
        self.index = 0
        self.framecounter = 0

    def getSprites(self):
        return self.sprites

    def changeDirection(self, orientation):
        if self.facing == orientation:
            self.facing = orientation
        elif self.facing != orientation:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = orientation