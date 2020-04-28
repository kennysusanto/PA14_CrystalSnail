import pygame
import sys
import time

display_width = 256 * 2
display_height = 223 * 2
SIZE = display_width, display_height
# BACKGROUND_COLOR = pygame.Color('white')
FPS = 4

def sprite_sheet(size,file,pos=(0,0)):

    #Initial Values
    len_sprt_x,len_sprt_y = size #sprite size
    sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

    sheet = pygame.image.load(file).convert() #Load the sheet
    sheet.set_colorkey((0,128,255))
    sheet_rect = sheet.get_rect()
    sprites = []
    print(sheet_rect.height, sheet_rect.width)
    for i in range(0,sheet_rect.height-len_sprt_y,size[1]):#rows
        print("row")
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
            print("column")
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
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

class mySprite(pygame.sprite.Sprite):
    def __init__(self, image_file, sprite_size):
        super(mySprite, self).__init__()

        # sprite_size = width*height
        self.sprites = sprite_sheet(sprite_size, image_file)

        self.images = []
        # self.images.append(pygame.image.load('walk1.png'))
        for sprite in self.sprites:
        	self.images.append(sprite)
        
        self.index = 0

        self.image = self.images[self.index]

        self.rect = pygame.Rect(5, 5, sprite_size[0], sprite_size[1])

    def update(self):
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]

class Character():
	def __init__(self, name, state, position, vx, vy, frame_index, frame_timer):
		self.name = name
		self.state = state
		self.posx, self.posy = position
		self.vx = vx
		self.vy = vy
		self.frame_index = frame_index
		self.frame_timer = frame_timer

	def updateState(newstate):
		self.state = newstate

	def update():
		self.frame_index += 1

class State():
	def __init__(self, name):
		self.name = name

	def setSprite():
		self.sprite = mySprite()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    swidth = 43
    sheight = 46
    cs = mySprite("Resources/images/cut/intro.png", (swidth,sheight))
    cs_group = pygame.sprite.Group(cs)
    clock = pygame.time.Clock()

    bg = backGround("Resources/images/cut/bg.png", (SIZE), (0,0))
    screen.fill((255, 255, 255))
    screen.blit(bg.image, bg.rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        cs_group.update()
        screen.fill((255, 255, 255))
        screen.blit(bg.image, bg.rect)
        cs_group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

main()