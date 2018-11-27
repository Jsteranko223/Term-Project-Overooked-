'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
import pygame
import time
import random
import Classes
import Functions

pygame.init()
pygame.font.init()


class PygameGame(object):

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_x:                    
            pygame.quit()

        if keyCode == pygame.K_s:
            self.player.d[1] = -1
            self.player.action = False
        if keyCode == pygame.K_w:
            self.player.d[1] = 1
            self.player.action = False
        if keyCode == pygame.K_a:
            self.player.d[0] = -1
            self.player.action = False
        if keyCode == pygame.K_d:
            self.player.d[0] = 1
            self.player.action = False
            
        if keyCode == pygame.K_e:
            self.player.action = True
            
        if keyCode == pygame.K_q:   
            #Pick up with hands
            if self.player.item == None:
                Functions.pickUp(self.player,self.player.c, self.counters)
            #Plate
            elif str(self.player.item) == 'Plate':
                if self.player.item.item != None:
                    Functions.putDown(self.player, self.player.c, self.counters)
                elif str(self.counters[self.player.c].item) == 'Pot' and \
                        self.player.item.dirty == False and \
                        self.counters[self.player.c].item.dish != None:
                    Functions.pickUp(self.player, self.player.c, self.counters)
                else:
                    Functions.putDown(self.player, self.player.c, self.counters)
            #Put down item
            elif self.player.item != None:
                Functions.putDown(self.player, self.player.c, self.counters)
    
    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_s or keyCode == pygame.K_w:
            self.player.d[1] = 0
        if keyCode == pygame.K_a or keyCode == pygame.K_d:
            self.player.d[0] = 0


    def timerFired(self, dt):
        
        clock = pygame.time.Clock()
        clock_tick_rate= 20

        if self.player.d[1] == -1:
            self.player = Functions.move(self.player, 'down', self.counters)
        if self.player.d[1] == 1:
            self.player = Functions.move(self.player, 'up', self.counters)
        if self.player.d[0] == -1:
            self.player = Functions.move(self.player, 'left', self.counters)
        if self.player.d[0] == 1:
            self.player = Functions.move(self.player, 'right', self.counters)
        self.player.c = Functions.lookAtCounter(self.player, self.counters)
        
        if self.player.action == True:
            if type(self.counters[self.player.c]) == Classes.CuttingBoard:
                Functions.chop(self.player, self.player.c, self.counters)
                if type(self.counters[self.player.c].item) == Classes.Food and \
                self.counters[self.player.c].item.chopped == True:
                    self.player.action = False
            elif type(self.counters[self.player.c]) == Classes.Wash:
                Functions.wash(self.player, self.player.c, self.counters)
                if self.counters[self.player.c].plateCount == 0:
                    self.player.action = False
            elif str(self.player.item) == 'Extinguisher':
                Functions.extinguish(self.player, self.player.c, self.counters)

        Functions.cook(self.counters[35])
        Functions.cook(self.counters[33])
        
        if self.milliseconds > 1000:
            self.seconds += 1
            self.milliseconds -= 1000
            for i in range(len(self.counters[20].recipes)):
                if self.counters[20].recipes[i] != None:
                    self.counters[20].recipeTimes[i] += 1
            if (self.timer-self.seconds) % 30 == 0:
                for i in range(len(self.counters[20].recipes)):
                    if self.counters[20].recipes[i] == None:
                        self.counters[20].recipes[i] = Functions.generateRecipes()
                        break
                        
        self.milliseconds += clock.tick(clock_tick_rate)
        
    def redrawAll(self, screen):
        screen.blit(self.backgroundImage, (0,0))
        pygame.draw.rect(screen, (0,0,255), self.player.p)
        
        if self.player.c != -1:
            counter = self.counters[self.player.c]
            pygame.draw.rect(screen, (255,230, 0), counter.r)
            
        if self.player.item != None:
            if str(self.player.item) == 'Plate':
                if self.player.item.dirty == False:
                    screen.blit(self.plateImage,(self.player.lookX,self.player.lookY))
                else:
                    screen.blit(self.dirtyPlateImage, (self.player.lookX, self.player.lookY))
                if self.player.item.item != None:
                    Functions.drawFood(screen, self.player.lookX, \
                    self.player.lookY, self.player.item.item, False)
                    if type(self.player.item.item) == Classes.Dish:
                        Functions.drawFood(screen, self.player.lookX-self.player.width//2, 
                        self.player.lookY-self.player.height*2, self.player.item.item.food1, True)
                        Functions.drawFood(screen, self.player.lookX+4*self.player.width//3, 
                        self.player.lookY-self.player.height*2, self.player.item.item.food2, True)
                        Functions.drawFood(screen, self.player.lookX-self.player.width//2, 
                        self.player.lookY, self.player.item.item.food3, True)
                    elif self.player.item.item.chop > 0 and self.player.item.item.chopped == False:
                        r = pygame.Rect(self.player.lookX-5, self.player.lookY-10, 
                                    self.player.item.item.chop, 10)
                        pygame.draw.rect(screen, (0,255,0), r)
                        
            elif str(self.player.item) == 'Pot':
                screen.blit(self.potImage,(self.player.lookX, self.player.lookY))
                Functions.drawFood(screen, self.player.lookX-self.player.height//2, 
                self.player.lookY-self.player.width*2, self.player.item.food1, True)
                Functions.drawFood(screen, self.player.lookX+4*self.player.height//3, 
                self.player.lookY-self.player.width*2, self.player.item.food2, True)
                Functions.drawFood(screen, self.player.lookX-self.player.height//2, 
                self.player.lookY, self.player.item.food3, True)
                
                if self.player.item.dish != None:
                   Functions.drawFood(screen, self.player.lookX, 
                   self.player.lookY, self.player.item.dish, False)

            elif str(self.player.item) == 'Extinguisher':
                    screen.blit(self.extinguisherImage,(self.player.lookX,self.player.lookY))
            else:
                Functions.drawFood(screen, self.player.lookX, self.player.lookY, self.player.item, False)
                if self.player.item.chop > 0 and self.player.item.chopped == False:
                    r = pygame.Rect(self.player.lookX-5, self.player.lookY-10, 
                                self.player.item.chop, 10)
                    pygame.draw.rect(screen, (0,255,0), r)
                        
                        
        for counter in self.counters:
            if type(counter) == Classes.PlateReturn or type(counter) == Classes.Wash:
                if counter.plateCount != 0:
                    screen.blit(self.dirtyPlateImage,(counter.left,counter.top))
                    if type(counter) == Classes.Wash and counter.wash > 0:
                        r = pygame.Rect(counter.left-5, counter.bottom+10, 
                                        counter.wash, 10)
                        pygame.draw.rect(screen, (0,255,0), r)
            elif type(counter) == Classes.WashReturn:
                if counter.plateCount != 0:
                    screen.blit(self.plateImage,(counter.left,counter.top))
            elif type(counter) == Classes.Serve:
                for i in range(len(counter.recipes)):
                    if counter.recipes[i] != None:
                        Functions.drawFood(screen, 8+90*i, 32, counter.recipes[i], True)
                        r = pygame.Rect(8+90*i, 32, 
                                    65-counter.recipeTimes[i], 10)
                        pygame.draw.rect(screen, (0,255,0), r)
                        if counter.recipeTimes[i] >= 65:
                            counter.recipes[i] = None
                            counter.recipeTimes[i] = 0 
                            counter.score -= 1
                            if counter.recipes.count(None) == 4:
                                counter.recipes[0] = Functions.generateRecipes()
                            for i in range(len(counter.recipes)-1):
                                if counter.recipes[i] == None and \
                                    counter.recipes[i+1] != None:
                                    counter.recipes[i] = counter.recipes[i+1]
                                    counter.recipes[i+1] = None
                                    counter.recipeTimes[i] = counter.recipeTimes[i+1]
                                    counter.recipeTimes[i+1] = 0
                            
            else:
                if counter.item != None:
                    if str(counter.item) == 'Plate': #Draw Plate on counter
                        if counter.item.dirty == False:
                            screen.blit(self.plateImage,(counter.left,counter.top))
                        else:
                            screen.blit(self.dirtyPlateImage,
                            (counter.left,counter.top))
                        if counter.item.item != None: #Food on plate on counter
                            Functions.drawFood(screen, counter.left, 
                            counter.top,counter.item.item, False)
                            if type(counter.item.item) == Classes.Dish:
                                drawFood(screen, counter.left-player.width//2, 
                                counter.top-player.height*2, 
                                counter.item.item.food1, True)
                                drawFood(screen, counter.left+4*player.width//3, 
                                counter.top-player.height*2, 
                                counter.item.item.food2, True)
                                drawFood(screen, counter.left-player.width//2, 
                                counter.top, counter.item.item.food3, True)
                            elif counter.item.item.chop > 0 and \
                               counter.item.item.chopped == False:
                                r = pygame.Rect(counter.left-5, counter.top-10, 
                                            counter.item.item.chop, 10)
                                pygame.draw.rect(screen, (0,255,0), r)
                            
                            
                                
                    elif str(counter.item) == 'Extinguisher':
                        screen.blit(self.extinguisherImage, 
                        (counter.left, counter.top))
                        
                    elif str(counter.item) == 'Pot':
                        screen.blit(self.potImage, (counter.left, counter.top-5))
                        if counter.item.fire > 40:
                            screen.blit(self.fireImage, (counter.left, counter.top-65))
                        else:
                            Functions.drawFood(screen, counter.left-counter.width//2, 
                            counter.top-counter.height, counter.item.food1, True)
                            Functions.drawFood(screen, counter.left+counter.width//2, 
                            counter.top-counter.height, counter.item.food2, True)
                            Functions.drawFood(screen, counter.left-counter.width//2, 
                            counter.top, counter.item.food3, True)
                            
                            if counter.item.dish != None:
                                Functions.drawFood(screen, counter.left, counter.top-5,
                                counter.item.dish, False)
                        
                    else:
                        Functions.drawFood(screen, counter.left, 
                            counter.top, counter.item, False)
                        if counter.item.chop > 0 and \
                           counter.item.chopped == False:
                            r = pygame.Rect(counter.left-5, counter.top-10, 
                                        counter.item.chop, 10)
                            pygame.draw.rect(screen, (0,255,0), r)
            if type(counter) == Classes.Stove:
                if str(counter.item) == 'Pot' and counter.item.food1 != None and \
                str(counter.item.food1) != 'fire' and counter.item.fire <= 40:
                    progress = 50*(1 - (counter.item.cook/counter.item.cookTime))
                    r = pygame.Rect(counter.left-5, counter.top-10, progress, 10)
                    pygame.draw.rect(screen, (0,255,0), r)
                    
        textsurface = self.myfont.render(str(self.counters[20].score), False, (0, 0, 0))
        screen.blit(textsurface,(40,500))

        textsurface1 = self.myfont.render(str(self.timer-self.seconds), False, (0, 0, 0))
        screen.blit(textsurface1,(900,490))


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1000, height=600, fps=40, title="Overcooked"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.myfont = pygame.font.SysFont('Segoe UI Black', 30)
        screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
        self.counters = Functions.makeCounters()
        self.backgroundImage = pygame.image.load("Images/BackgroundFinal.png").convert_alpha()
        self.plateImage = pygame.image.load("Images/Plate.png").convert_alpha()
        self.dirtyPlateImage = pygame.image.load("Images/DirtyPlate.png").convert_alpha()
        self.extinguisherImage = pygame.image.load("Images/ExtinguisherFinal.png")\
                            .convert_alpha()
        self.potImage = pygame.image.load("Images/Pot.png").convert_alpha()
        self.fireImage = pygame.image.load("Images/Fire.png").convert_alpha()
        self.player = Classes.Player(400,250)
        
        self.seconds = 0
        self.milliseconds = 0
        self.timer = 180


    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


game = PygameGame()
game.run()
