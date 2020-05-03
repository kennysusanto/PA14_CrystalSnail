import pygame
import sys
import os
import time
import math
import random
import classes as fc

display_width = 256
display_height = 223
disp_SIZE = display_width, display_height
# BACKGROUND_COLOR = pygame.Color('white')
FPS = 30

def randRangeExcept(n, sprite1_size, sprite2_size , start, end):
    return list(range(start, n-sprite2_size)) + list(range(n+sprite1_size, end-sprite2_size))

def calcAngle(lineA,lineB):
    line1Y1 = lineA[0][1]
    line1X1 = lineA[0][0]
    line1Y2 = lineA[1][1]
    line1X2 = lineA[1][0]

    line2Y1 = lineB[0][1]
    line2X1 = lineB[0][0]
    line2Y2 = lineB[1][1]
    line2X2 = lineB[1][0]

    #calculate angle between pairs of lines
    angle1 = math.atan2(line1Y1-line1Y2,line1X1-line1X2)
    angle2 = math.atan2(line2Y1-line2Y2,line2X1-line2X2)
    angleDegrees = (angle1-angle2) * 360 / (2*math.pi)
    return angleDegrees

def col_check(rect1, rect2):
    x, y, w, h = rect1
    x2, y2, w2, h2 = rect2
    res = False
    if (x < (x2 + w2) and (x + w) > x2 and y < (y2 + h2) and (h + y) > y2):
        # print("COLLIDED!!!")
        res = True
    return res

def main():
    pygame.init()
    screen = pygame.display.set_mode(disp_SIZE)

    clock = pygame.time.Clock()

    # background
    bg = fc.backGround("Resources/images/cut/bg.png", (disp_SIZE), (0, 0))
    screen.fill((255, 255, 255))
    screen.blit(bg.image, bg.rect)

    # instructions
    myfont = pygame.font.SysFont("Arial", 10)

    # sprite size
    swidth = 43
    sheight = 46

    # default spawn position
    dx = 100
    dy = 100

    # Declaring characters
    cs = fc.Character("Crystal Snail", (dx+50, 15), (0, 128, 255), "left")
    mm = fc.Character("Megaman_dummy", (dx-50, dy), (50, 96, 166), "left")

    # Declaring states for Crystal Snail
    alist = cs.getStates()

    cs.addState("Stand", True, "Resources/images/cut/stand.png", (swidth, sheight))
    sprites = cs.findState("Stand").getSprites()
    for i in range(2):
        sprites[i].setMFT(6)
    
    cs.addState("Intro", False, "Resources/images/cut/intro.png", (swidth, sheight), cs.findState("Stand"))
    sprites = cs.findState("Intro").getSprites()
    for i in range(11):
        sprites[i].setMFT(5)
    sprites[11].setMFT(18)
    
    cs.addState("intro_bounce", False, "Resources/images/cut/intro_bounce.png", (40, 37))
    sprites = cs.findState("intro_bounce").getSprites()
    l = len(sprites)
    print(f"the Roll state have {l} frames")
    sprites[0].setMFT(1)

    cs.addState("intro_roll2", False, "Resources/images/cut/roll_straight.png", (swidth, 43), cs.findState("intro_bounce"))
    sprites = cs.findState("intro_roll2").getSprites()
    l = len(sprites)
    print(f"the Roll state have {l} frames")
    for i in range(30):
        sprites[i].setMFT(1)
    for i in range(30, 40):
        sprites[i].setMFT(2)
    
    cs.addState("intro_roll1", False, "Resources/images/cut/roll_straight.png", (swidth, 43), cs.findState("intro_roll2"))
    sprites = cs.findState("intro_roll1").getSprites()
    cs.updateState(cs.findState("intro_roll1"))
    l = len(sprites)
    print(f"the Roll state have {l} frames")
    for i in range(40):
        sprites[i].setMFT(1)

    cs.addState("Take_cover", False, "Resources/images/cut/take_cover.png", (swidth, sheight))
    sprites = cs.findState("Take_cover").getSprites()
    for i in range(4):
        sprites[i].setMFT(2)

    cs.addState("Trans_open_cover", False, "Resources/images/cut/open_cover.png", (swidth, sheight), cs.findState("Stand"))
    sprites = cs.findState("Trans_open_cover").getSprites()
    for i in range(4):
        sprites[i].setMFT(2)

    cs.addState("Roll", True, "Resources/images/cut/roll_straight.png", (swidth, 43))
    sprites = cs.findState("Roll").getSprites()
    l = len(sprites)
    print(f"the Roll state have {l} frames")
    for i in range(40):
        sprites[i].setMFT(1)

    
    cs.addState("Launch_upwards", False, "Resources/images/cut/launch.png", (swidth, 76), cs.findState("Roll"))
    sprites = cs.findState("Launch_upwards").getSprites()
    l = len(sprites)
    print(f"the Launch_upwards state have {l} frames")
    for i in range(3):
        sprites[i].setMFT(10)

    cs.addState("Throw", False, "Resources/images/cut/throw.png", (42, sheight), cs.findState("Stand"))
    sprites = cs.findState("Throw").getSprites()
    sprites[0].setMFT(12)

    cs.addState("Shoot_projectile", False, "Resources/images/cut/shooting_projectile_2.png", (swidth, sheight), cs.findState("Throw"))
    sprites = cs.findState("Shoot_projectile").getSprites()
    l = len(sprites)
    print(f"the Shoot_projectile state have {l} frames")
    for i in range(3):
        sprites[i].setMFT(12)

    cs.addState("Landing", False, "Resources/images/cut/landing.png", (44, 48))
    sprites = cs.findState("Landing").getSprites()
    l = len(sprites)
    print(f"the Landing state have {l} frames")
    for i in range(4):
        sprites[i].setMFT(3)
    
    cs.addState("Reroll_Charge_antennae", False, "Resources/images/cut/reroll_antennae.png", (44, 52), cs.findState("Roll"))
    sprites = cs.findState("Reroll_Charge_antennae").getSprites()
    l = len(sprites)
    print(f"the Charge_antennae state have {l} frames")
    for i in range(6):
        sprites[i].setMFT(2)

    cs.addState("Charge_antennae", False, "Resources/images/cut/charge_antennae.png", (44, 52), cs.findState("Reroll_Charge_antennae"))
    sprites = cs.findState("Charge_antennae").getSprites()
    l = len(sprites)
    print(f"the Charge_antennae state have {l} frames")
    for i in range(6):
        sprites[i].setMFT(3)

    cs.addState("Launch_towards_target", False, "Resources/images/cut/launch.png", (swidth, 76), cs.findState("Roll"))
    sprites = cs.findState("Launch_towards_target").getSprites()
    l = len(sprites)
    print(f"The Launch_towards_target state have {l} frames")
    for i in range(3):
        sprites[i].setMFT(10)

    cs.addState("Staggered", True, "Resources/images/cut/staggered.png", (swidth, 47))
    sprites = cs.findState("Staggered").getSprites()
    sprites[0].setMFT(12)


    for item in alist:
        print(item.getName())

    # Declaring states for megaman dummy
    mm.addState("Run", True, "Resources/images/cut/megaman/cut_run.png", (34, 35))
    sprites = mm.findState("Run").getSprites()
    l = len(sprites)
    print(f"The Run state have {l} frames")
    for i in range(11):
        sprites[i].setMFT(3)

    mm.addState("Intro", False, "Resources/images/cut/megaman/cut_intro.png", (30, 48), mm.findState("Run"))
    sprites = mm.findState("Intro").getSprites()
    l = len(sprites)
    print(f"The Run state have {l} frames")
    for i in range(12):
        sprites[i].setMFT(6)
    sprites[12].setMFT(18)

    mm.addState("Die", True, "Resources/images/cut/megaman/cut_hitordie.png", (26, 36))
    sprites = mm.findState("Die").getSprites()
    for i in range(2):
        sprites[i].setMFT(12)
    
    mm.addState("Dead", False, "Resources/images/cut/megaman/cut_hitordie.png", (26, 36))
    sprites = mm.findState("Die").getSprites()
    for i in range(2):
        sprites[i].setMFT(1)
    
    mm.addState("Frozen", True, "Resources/images/cut/megaman/cut_hitordie.png", (26, 36))
    sprites = mm.findState("Frozen").getSprites()
    for i in range(2):
        sprites[i].setMFT(2)


    # Declaring Floors & Walls
    # bot = 0-255, 191
    # left = 16, 0-223
    # top = 0-255, 14
    # right = 241, 0-223
    floor = fc.obstruction(0, 190, 255, 223)
    left_wall = fc.obstruction(0, 0, 16, 223)
    right_wall = fc.obstruction(241, 0, 255, 223)
    ceiling = fc.obstruction(0, 0, 255, 14)

    # Declaring crystal projectile with default attributes
    # 45 deg
    projectile1 = fc.projectile(0, 0, 16, 16, "Resources/images/cut/projectiles.png", (0, 128, 255))
    sprites = projectile1.getSprites()
    print(len(sprites))
    for i in range(2):
        sprites[i].setMFT(6)
    
    # 60 deg
    projectile2 = fc.projectile(0, 0, 16, 16, "Resources/images/cut/projectiles.png", (0, 128, 255))
    sprites = projectile2.getSprites()
    print(len(sprites))
    for i in range(2):
        sprites[i].setMFT(6)
    
    # horizontal
    projectile3 = fc.projectile(0, 0, 16, 16, "Resources/images/cut/projectiles.png", (0, 128, 255))
    sprites = projectile3.getSprites()
    print(len(sprites))
    for i in range(2):
        sprites[i].setMFT(6)

    # For continuous movement
    move_right = move_left = False
    gravity = True
    mmgravity = True

    # For drawing projectile
    throwable1 = False
    throwable2 = False
    throwable3 = False
    ctr = 0

    # Die animation loop counter for MM
    dctr = 0

    # Stagger animation loop counter for CS
    sctr = 0

    # Bounce counter for intro bounce for CS
    bctr = 0
    bounce = False

    # Freeze counter for MM
    fctr = 0

    # Slow down time bool
    slowmo = False
    smctr = 0

    # Main loop
    while True:
        # Event triggers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cs.updateState(cs.findState("Intro"))
                elif event.key == pygame.K_RIGHT:
                    cs.setFacing("right")
                elif event.key == pygame.K_LEFT:
                    cs.setFacing("left")
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    if(cs.getState().getName() == "Take_cover"):
                        cs_curr_sprite.resetIndex()
                        cs.updateState(cs.findState("Trans_open_cover"))
                    else:
                        if cs.getState().getName() == "Stand":
                            cs.updateState(cs.findState("Take_cover"))
                elif event.key == pygame.K_r:
                    if cs.getState().getName() == "Take_cover":
                        cs.updateState(cs.findState("Launch_upwards"))
                elif event.key == pygame.K_z:
                    cs.move((100, 100))
                elif event.key == pygame.K_l:
                    if cs.getState().getName() == "Roll":
                        cs.findState("Take_cover").resetIndex()
                        cs.findState("Landing").resetIndex()
                        x, y = cs.getLoc()
                        cs.updateState(cs.findState("Landing"))
                        cs.move((x, y))
                elif event.key == pygame.K_c:
                    if cs.getState().getName() == "Roll":
                        cs.findState("Take_cover").resetIndex()
                        cs.findState("Charge_antennae").resetIndex()
                        cs.updateState(cs.findState("Charge_antennae"))
                elif event.key == pygame.K_s:
                    if cs.getState().getName() == "Stand":
                        cs.findState("Shoot_projectile").resetIndex()
                        x, y, w, h = cs.getState().getRect()
                        a = math.floor(x+(w/2))
                        b = y-30
                        print(a, b)
                        projectile1.setSpawn((a, b))
                        projectile2.setSpawn((a, b))
                        projectile3.setSpawn((a, b))
                        cs.updateState(cs.findState("Shoot_projectile"))
                elif event.key == pygame.K_d:
                    if cs.getState().getName() == "Launch_upwards":
                        pass
                    else:
                        mm.updateState(mm.findState("Dead"))
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass

            # event.button can equal several integer values:
            # 1 - left click
            # 2 - middle click
            # 3 - right click
            # 4 - scroll up
            # 5 - scroll down
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if cs.getState().getName() == "Roll":
                    a, b, c, d = cs.getState().getRect()
                    
                    # line1 mengarah ke kanan
                    line1 = (a+(c/2), b+(d/2)), (a+c, b+(d/2))
                    line2 = (a+(c/2), b+(d/2)), pos
                    # print(ang(line1, line2))
                    angle = calcAngle(line1, line2)
                    print(angle)

                    cs.updateState(cs.findState("Launch_towards_target"))
                    
        # Display Text
        disp_txt1 = ""
        disp_txt2 = ""
        disp_txt3 = ""
        disp_txt4 = ""

        # Left and right movement, will be deleted
        cs_rect = cs.getState().getRect()
        if(move_right):
            rw_rect = right_wall.getRect()
            if(col_check(cs_rect, rw_rect)):
                cs.setVel((0, 0))
            else:
                cs.setVel((5, 0))
        elif(move_left):
            lw_rect = left_wall.getRect()
            if(col_check(cs_rect, lw_rect)):
                cs.setVel((0, 0))
            else:
                cs.setVel((-5, 0))

        # Sprite grouping
        # Crystal Snail
        cs_curr_sprite = cs.getState()
        cs_group = pygame.sprite.Group(cs_curr_sprite)

        # Megaman dummy
        mm_curr_sprite = mm.getState()
        if mm_curr_sprite == None:
            pass
        else:
            mm_group = pygame.sprite.Group(mm_curr_sprite)

        # Obstructions (walls, floor, and ceiling)
        obs_group = pygame.sprite.Group(floor, left_wall, right_wall, ceiling)

        # Projectile group
        pr_group1 = pygame.sprite.Group(projectile1)
        pr_group2 = pygame.sprite.Group(projectile2)
        pr_group3 = pygame.sprite.Group(projectile3)

        # State loop
        if(cs.getState().getLoop()):
            cs_curr_sprite.loop()
        elif(not cs.getState().getLoop()):
            done = cs_curr_sprite.play()
            if(done):                        
                nextState = cs.getState().getnextState()
                if nextState == None:
                    pass
                else:
                    cs_curr_sprite.resetIndex()
                    cs.updateState(nextState)

        if mm_curr_sprite == None:
            pass
        else:
            if(mm.getState().getLoop()):
                mm_curr_sprite.loop()
            elif(not mm.getState().getLoop()):
                done = mm_curr_sprite.play()
                if(done):                        
                    nextState = mm.getState().getnextState()
                    if nextState == None:
                        pass
                    else:
                        mm_curr_sprite.resetIndex()
                        mm.updateState(nextState)
        
        projectile1.loop()
        projectile2.loop()
        projectile3.loop()
                
        # Special event trigger for Crystal Snail
        # Intro
        if cs.getState().getName() == "intro_roll1":
            gravity = True
            x, y, w, h = cs.getState().getRect()
            if y >= 100:
                gravity = False
                cs.setVel((0, 0))

        if cs.getState().getName() == "intro_roll2":
            gravity = True
            x, y, w, h = cs.getState().getRect()
            if y >= 100:
                gravity = False
                cs.setVel((0, 0))

        if cs.getState().getName() == "intro_bounce":
            gravity = True
            if bctr >= 100:
                cs.updateState(cs.findState("Intro"))
                x, y, w, h = cs_rect
                cs.move((x, y-11))
            
            if bctr == 50:
                bounce = True
            elif bctr == 60:
                bounce = False
            elif bctr == 70:
                bounce = True
            elif bctr == 75:
                bounce = False
            elif bctr == 80:
                bounce = True
            elif bctr == 83:
                bounce = False

            bctr += 1

        if cs.getState().getName() == "Intro":
            bctr = 0 # reset bounce counter
            gravity = True
            
                

        # Stand
        if cs.getState().getName() == "Stand":
            gravity = False
            ctr = 0 # reset shoot projectile counter
            sctr = 0 # reset staggered loop counter
            disp_txt1 = "Press 'ARROW DOWN' to Take Cover"
            disp_txt2 = "Press 'S' to Shoot Crystal"
            disp_txt4 = "Press 'D' to Summon Dummy"
            
        # Take cover
        if cs.getState().getName() == "Take_cover":
            disp_txt1 = "Press 'ARROW DOWN' to Open Cover"
            disp_txt2 = "Press 'R' to Launch"
        
        # Launch upwards
        nm = cs.getState().getName()
        holder_obs = floor
        x0, y0, xy0, xy0 = floor.getRect()
        if (nm == "Launch_upwards"):
            tmp_floor = fc.obstruction(0, 0, 0, 0)
            floor = tmp_floor
            gravity = False
            x1, y1 = cs.getLoc()
            if y1 <= (y0-130):
                cs.setVel((0, 0))
            else:
                cs.setVel((0, -5))
        
        # Launch towards target
        if cs.getState().getName() == "Launch_towards_target":
            gravity = False
            cs.getState().rotateImg(angle-90) # adjustments
            x, y = cs.getLoc() # CS position
            a, b, c, d = cs.getState().getRect()
            # getting the center of sprite
            x = x + c/2
            y = y + 15
            x = math.floor(x)
            y = math.floor(y)
            x1, y1 = pos # mouse position
            x1 = math.floor(x1)
            y1 = math.floor(y1)
            if x1 > x and y1 > y:
                cs.setVel((3, 3))
            elif x1 < x and y1 < y: 
                cs.setVel((-3, -3))
            elif x1 > x and y1 < y:
                cs.setVel((3, -3))
            elif x1 < x and y1 > y:
                cs.setVel((-3, 3))
            elif y1 > y and x1 == x:
                cs.setVel((0, 3))
            elif y1 < y and x1 == x:
                cs.setVel((0, -3))
            elif x1 > x and y1 == y:
                cs.setVel((3, 0))
            elif x1 < x and y1 == y:
                cs.setVel((-3, 0))
            elif x1 == x and y1 == y:
                cs.setVel((0, 0))
                cs.move((x1-(c/2), y1-15))
        
        # Roll
        if cs.getState().getName() == "Roll":
            gravity = False
            cs.setVel((0, 0))        
            disp_txt1 = "Press 'L' to Land"
            disp_txt2 = "Press 'C' to Charge Antennae"
            disp_txt3 = "Click with mouse to launch to destination"

        # Landing
        if cs.getState().getName() == "Landing":
            cs.findState("Charge_antennae").resetIndex()
            gravity = True
            if col_check(cs_rect, floor_rect):
                vx, vy = cs.getVel()
                cs.setVel((vx, 0))
                cs.updateState(cs.findState("Stand"))

        # Charge antennae
        if cs.getState().getName() == "Charge_antennae":
            gravity = False

        # Slowmo 
        if cs.getState().getName() == "Reroll_Charge_antennae":
            gravity = False
            slowmo = True
            

        if slowmo:
            if smctr >= 300:
                slowmo = False
            smctr += 1

        # Shoot projectile
        # gravity for projectile 1
        vx, vy = projectile1.getVel()
        vy += 0.5
        projectile1.setVel((vx, vy))
        # projectile 1 hitting obs
        if col_check(projectile1.getRect(), floor.getRect()):
            projectile1.setVel((0, 0))
            throwable1 = False
        elif col_check(projectile1.getRect(), left_wall.getRect()):
            projectile1.setVel((0, 0))
            throwable1 = False
        elif col_check(projectile1.getRect(), right_wall.getRect()):
            projectile1.setVel((0, 0))
            throwable1 = False
        elif col_check(projectile1.getRect(), ceiling.getRect()):
            projectile1.setVel((0, 0))
            throwable1 = False

        # gravity for projectile 2
        vx, vy = projectile2.getVel()
        vy += 0.5
        projectile2.setVel((vx, vy))
        # projectile 2 hitting obs
        if col_check(projectile2.getRect(), floor.getRect()):
            projectile2.setVel((0, 0))
            throwable2 = False
        elif col_check(projectile2.getRect(), left_wall.getRect()):
            projectile2.setVel((0, 0))
            throwable2 = False
        elif col_check(projectile2.getRect(), right_wall.getRect()):
            projectile2.setVel((0, 0))
            throwable2 = False
        elif col_check(projectile2.getRect(), ceiling.getRect()):
            projectile2.setVel((0, 0))
            throwable2 = False
        
        # gravity for projectile 3
        vx, vy = projectile3.getVel()
        vy += 0.1
        projectile3.setVel((vx, vy))
        # projectile 3 hitting obs
        if col_check(projectile3.getRect(), floor.getRect()):
            projectile3.setVel((0, 0))
            throwable3 = False
        elif col_check(projectile3.getRect(), left_wall.getRect()):
            projectile3.setVel((0, 0))
            throwable3 = False
        elif col_check(projectile3.getRect(), right_wall.getRect()):
            projectile3.setVel((0, 0))
            throwable3 = False
        elif col_check(projectile3.getRect(), ceiling.getRect()):
            projectile3.setVel((0, 0))
            throwable3 = False

        if cs.getState().getName() == "Shoot_projectile":
            gravity = False
                    
        # Throw transition state for shoot projectile
        if cs.getState().getName() == "Throw":
            gravity = False
            if ctr == 0:
                # projectile 1 = 45 deg
                # projectile 2 = 60 deg
                # projectile 3 = horizontal
                if cs.getFacing() == "right":
                    projectile1.setVel((5, -8))
                    projectile2.setVel((3, -12))
                    projectile3.setVel((6, -1))
                elif cs.getFacing() == "left":
                    projectile1.setVel((-5, -8))
                    projectile2.setVel((-3, -12))
                    projectile3.setVel((-6, -1))

                throwable1 = True
                throwable2 = True
                throwable3 = True
                ctr += 1
        
        # Staggered
        if cs.getState().getName() == "Staggered":
            gravity = True
            x, y = cs.getLoc()
            cs.move((x, y-2))
            if sctr >= 24:
                cs.updateState(cs.findState("Stand"))
            sctr += 1

        # Special event trigger for Megaman Dummy
        if mm_curr_sprite == None:
            pass
        else:
            # Intro
            if mm.getState().getName() == "Intro":
                dctr = 0
                mmgravity = True
            
            # Run
            # the facing of megaman is twisted (left = right and right = left), it's my fault lol
            # because the sprite sheet is facing the other way around
            if mm.getState().getName() == "Run":
                fctr = 0
                speed = 3 # running speed
                if cs.getState().getName() == "Launch_upwards":
                    vx, vy = mm.getVel()
                    mm.setVel((vx, 0))
                    mmgravity = False
                else:
                    mmgravity = True
                if mm.getFacing() == "right":
                    vx, vy = mm.getVel()
                    mm.setVel((-speed, vy))
                elif mm.getFacing() == "left":
                    vx, vy = mm.getVel()
                    mm.setVel((speed, vy))
            
            # Die
            if mm.getState().getName() == "Die":
                print("die ", mm.getState().getRect())
                x, y = mm.getLoc()
                mm.move((x, y-1))
                mmgravity = True
                mm.setVel((0, 0))
                if dctr >= 24:
                    mm.updateState(mm.findState("Dead"))
                dctr += 1
            
            # Dead & Respawn
            if mm.getState().getName() == "Dead":
                mmgravity = True
                mm.setVel((0, 0))
                dctr = 0 # reset loop counter
                # respawn x between 17 until 240 excluding cs position
                x, y, w, h = cs.getState().getRect()
                k, l, m, n = mm.findState("Intro").getRect()
                r = randRangeExcept(x, w, m, 17, 240)
                xval = random.choice(r)
                mm.move((xval, 50))
                mm.findState("Run").move((xval, 50)) # Fixed the respawn bug
                mm.updateState(mm.findState("Intro"))
            
            # Frozen
            if mm.getState().getName() == "Frozen":
                mmgravity = False
                mm.setVel((0, 0))
                if fctr >= 50:
                    mm.updateState(mm.findState("Run"))
                fctr += 1

            

        # Check functions
        # print(cs.getState().getName())
        # print(pygame.mouse.get_pos())

        # If CS collides with obstructions / collision detection
        cs_rect = cs.getState().getRect()
        floor_rect = floor.getRect()
        rw_rect = right_wall.getRect()
        lw_rect = left_wall.getRect()
        ceil_rect = ceiling.getRect()

        

        # CS with floor
        if(col_check(cs_rect, floor_rect)):
            gravity = False
            vx, vy = cs.getVel()
            cs.setVel((vx, 0))

        # CS with ceiling
        if(col_check(cs_rect, ceil_rect)):
            cs.setVel((0, 0))

        # CS with right wall    
        if col_check(cs_rect, rw_rect):
            cs.setVel((0, 0))
        
        # CS with left wall
        if col_check(cs_rect, lw_rect):
            cs.setVel((0, 0))

        # If MM dummy collides with obstructions / collision detection
        if mm_curr_sprite == None:
            pass
        else:
            mm_rect = mm.getState().getRect()

            # MM with floor
            if col_check(mm_rect, floor_rect):
                mmgravity = False
                vx, vy = mm.getVel()
                mm.setVel((vx, 0))
            
            # MM with right wall
            if col_check(mm_rect, rw_rect):
                # this facing direction is also due to the incorrect megaman spritesheet
                mm.setFacing("right")

            # MM with left wall
            if col_check(mm_rect, lw_rect):
                # this facing direction is also due to the incorrect megaman spritesheet
                mm.setFacing("left")
            
            # MM with ceiling
            if col_check(mm_rect, ceil_rect):
                mm.setVel((0, 0))

            # MM got hit by projectile
            pr1_rect = projectile1.getRect()
            pr2_rect = projectile2.getRect()
            pr3_rect = projectile3.getRect()
            if col_check(pr1_rect, mm_rect) or col_check(pr2_rect, mm_rect) or col_check(pr3_rect, mm_rect):
                mm.updateState(mm.findState("Frozen"))
            
            # MM and CS collide
            if cs.getState().getName() == "Stand" and mm.getState().getName() == "Run":
                if col_check(mm_rect, cs_rect):
                    cs.updateState(cs.findState("Staggered"))
            elif cs.getState().getName() == "Shoot_projectile" and mm.getState().getName() == "Run":
                if col_check(mm_rect, cs_rect):
                    cs.updateState(cs.findState("Staggered"))
            elif cs.getState().getName() == "Take_cover" and mm.getState().getName() == "Run":
                if col_check(mm_rect, cs_rect):
                    mm.updateState(mm.findState("Die"))
            elif cs.getState().getName() == "Launch_towards_target" and mm.getState().getName() == "Run":
                if col_check(mm_rect, cs_rect):
                    mm.updateState(mm.findState("Die"))
            

        # Special event trigger cont'd
        floor = holder_obs

        # applies gravity
        if bounce:
            vx, vy = cs.getVel()
            cs.setVel((vx, -5))
        else:
            if gravity:
                vx, vy = cs.getVel()
                cs.setVel((vx, 5))        
            
        if mmgravity:
            vx, vy = mm.getVel()
            mm.setVel((vx, 5))

        # Movement based on speed
        vx, vy = cs.getVel()
        x, y = cs.getLoc()
        x += vx
        y += vy
        cs.move((x, y))

        vx, vy = mm.getVel()
        x, y = mm.getLoc()
        if slowmo:
            x += vx/2
            y += vy/2
        else:
            x += vx
            y += vy
        if mm_curr_sprite == None:
            pass
        else:
            mm.move((x, y))

        vx, vy = projectile1.getVel()
        x, y = projectile1.getLoc()
        x += vx
        y += vy
        projectile1.move((x, y))

        vx, vy = projectile2.getVel()
        x, y = projectile2.getLoc()
        x += vx
        y += vy
        projectile2.move((x, y))

        vx, vy = projectile3.getVel()
        x, y = projectile3.getLoc()
        x += vx
        y += vy
        projectile3.move((x, y))

        # Make sure next sprite is in correct direction
        cs_curr_sprite.changeDirection(cs.getFacing())
        projectile1.changeDirection(cs.getFacing())
        projectile2.changeDirection(cs.getFacing())
        projectile3.changeDirection(cs.getFacing())
        if mm_curr_sprite == None:
            pass
        else:
            mm_curr_sprite.changeDirection(mm.getFacing())

        # Update screen
        screen.fill((255, 255, 255))
        if cs.getState().getName() == "Reroll_Charge_antennae":
            bg_rippled = fc.backGround("Resources/images/cut/bg_ripple.png", (disp_SIZE), (0, 0))
            screen.blit(bg_rippled.image, bg.rect)
        else:
            screen.blit(bg.image, bg.rect)
        cs_group.draw(screen)
        # To check whether megaman is dead or not
        if mm_curr_sprite == None:
            pass
        else:
            if mm.getState().getName() == "Dead":
                pass
            else:
                mm_group.draw(screen)
        # To draw projectile
        if throwable1:
            pr_group1.draw(screen)
        if throwable2:
            pr_group2.draw(screen)
        if throwable3:
            pr_group3.draw(screen)
        label1 = myfont.render(disp_txt1, 1, (255, 255, 0)) # yellow
        label2 = myfont.render(disp_txt2, 1, (255, 255, 0)) # yellow
        label3 = myfont.render(disp_txt3, 1, (255, 255, 0)) # yellow
        label4 = myfont.render(disp_txt4, 1, (255, 255, 0)) # yellow
        screen.blit(label1, (10, 200))
        screen.blit(label2, (10, 210))
        screen.blit(label3, (90, 200))
        screen.blit(label4, (110, 210))
        pygame.display.update()

        # FPS
        clock.tick(FPS)


main()
