import pygame
import copy
import time

pygame.init()
pygame.font.init()


class Counter(object):
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = right-left
        self.height = bottom - top
        self.r = pygame.Rect(left, top, self.width, self.height)
        self.item = None

class FoodCrate(Counter):
    def __init__(self, left, top, right, bottom, type):
        super().__init__(left, top, right, bottom)
        self.food = type

class Trash(Counter):
    pass

class Serve(Counter):
    pass

class PlateReturn(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0

class Wash(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0

class WashReturn(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0


class CuttingBoard(Counter):
    pass

class Food(object):
    def __init__(self, type):
        self.type = type
        self.chopped = False
    
    def __repr__(self):
        return(self.type)
        
class Plate(object):
    def __init__(self):
        self.item = None
        self.dirty = False
    def __repr__(self):
        return('Plate')
        
class Stove(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.food1 = None
        self.food2 = None
        self.food3 = None
        
        self.dish = None
    
    def cook(self):
        food = [str(self.food1), str(self.food2), str(self.food3)]
        if food == ['onion', 'onion', 'onion']:
            self.dish = Food('onion soup')
            self.food1 = None
            self.food2 = None
            self.food3 = None
            
class Player(object):
    def __init__(self):
        self.x = 400
        self.y = 250
        self.size = 15
        self.speed = 10
        self.p = pygame.Rect(self.x, self.y, self.size, self.size)
        self.lookX = self.x+self.size//4
        self.lookY = self.y+self.size//2 
        self.direction = 'down'
        self.item = None
        self.score = 0

    def move(self, key, counters):
        if key == 'left':
            self.x -= self.speed
            self.lookX = self.x-self.size//2
            self.lookY = self.y+self.size//4
            self.direction = 'left'
        if key == 'right':
            self.x += self.speed
            self.lookX = self.x+self.size
            self.lookY = self.y+self.size//4
            self.direction = 'right'
        if key == 'up':
            self.y -= self.speed
            self.lookX = self.x+self.size//4
            self.lookY = self.y-self.size//2
            self.direction = 'up'
        if key == 'down':
            self.y += self.speed
            self.lookX = self.x+self.size//4
            self.lookY = self.y+self.size
            self.direction = 'down'
            
        for counter in counters:
            if self.detectCollision(self.x, self.y, self.size, counter):
                if key == 'left':
                    self.x += self.speed
                    
                if key == 'right':
                    self.x -= self.speed

                if key == 'up':
                    self.y += self.speed
                    
                if key == 'down':
                    self.y -= self.speed
        
        if self.x < 230 or self.x > 790:
            self.x = 400
            self.y = 250
                    
        self.look = pygame.Rect(self.lookX, self.lookY, self.size//2,
                                self.size//2)
        self.p = pygame.Rect(self.x, self.y, self.size, self.size)

            
    def detectCollision(self, px, py, psize, other):
        if other.left+other.width>=px >= other.left and \
           other.top + other.height >= py >= other.top:
            return True
            
        if other.left+other.width>=px+psize>=other.left and \
           other.top+other.height>=py>=other.top:
               return True
               
        if other.left+other.width>=px >= other.left and \
           other.top + other.height >= py+psize >= other.top:
            return True
            
        if other.left+other.width>=px+psize>=other.left and \
           other.top+other.height>=py+psize>=other.top:
               return True
            
        return False
    
    def lookAtCounter(self, counters, screen):
        for i in range(len(counters)):
            if self.detectCollision(self.lookX,self.lookY,self.size//2, 
                                    counters[i]):
                return i
        return -1
    
    def pickUp(self, c, counters):
        if c != -1:
            if type(counters[c]) == Stove: #Pick up dish from stove with plate
                if counters[c].dish != None and str(self.item) == 'Plate' and \
                self.item.dirty == False:
                    self.item.item = counters[c].dish
                    counters[c].dish = None
            else:
                if self.item == None: #Empty hands to pick up
                    if type(counters[c]) == PlateReturn: #Pick up dirty dish from return
                        if counters[c].plateCount != 0:
                            counters[c].plateCount -= 1                   
                            self.item = Plate()
                            self.item.dirty = True
                    elif type(counters[c]) == WashReturn: #Pick up clean dish from wash
                        if counters[c].plateCount != 0:
                            counters[c].plateCount -= 1                   
                            self.item = Plate()
                    else:
                        if counters[c].item != None: #Put up from counter
                            self.item = counters[c].item 
                            counters[c].item = None
                        elif type(counters[c]) == FoodCrate: #Pick up from food crate
                            self.item = copy.copy(counters[c].food)
                            self.item.chopped = False
                    
    
    def putDown(self, c, counters):
        if c != -1:
            if str(self.item) == 'Plate':  #Carrying plase
                if self.item.dirty == False: #Cannot use dirty plate
                    if self.item.item != None:
                        if type(counters[c]) == Serve: #Serve Food
                            if str(self.item.item) == 'onion soup':
                                self.item = None
                                counters[19].plateCount += 1
                                self.score += 1
                        elif type(counters[c]) == Stove:  #Put food on stove from plate
                            if self.item.item.chopped == True:
                                if counters[c].food1 == None:
                                    counters[c].food1 = self.item.item
                                    self.item.item = None
                                elif counters[c].food2 == None:
                                    counters[c].food2 = self.item.item
                                    self.item.item = None
                                elif counters[c].food3 == None:
                                    counters[c].food3 = self.item.item
                                    self.item.item = None
                        elif type(counters[c]) == Trash:  #Throw away food on plate
                            self.item.item = None
                else:
                    if type(counters[c]) == Wash:
                        self.item = None
                        counters[c].plateCount += 1
                #Put plate on empty counter
                if type(counters[c]) == Counter and counters[c].item == None: 
                    counters[c].item = self.item
                    self.item = None
                        
            elif self.item != None: #Carrying food
                if type(counters[c]) == Trash: #Put in Trash
                    self.item = None
                elif type(counters[c]) == Stove:  #Put food in stove
                    if self.item.chopped == True:
                        if counters[c].food1 == None:
                            counters[c].food1 = self.item
                            self.item = None
                        elif counters[c].food2 == None:
                            counters[c].food2 = self.item
                            self.item = None
                        elif counters[c].food3 == None:
                            counters[c].food3 = self.item
                            self.item = None
                        
                elif counters[c].item == None and \
                        type(counters[c]) != PlateReturn:  #Put on empty Counter
                    counters[c].item = self.item
                    self.item = None
                elif str(counters[c].item) == 'Plate' and \
                    counters[c].item.item == None: #Put on empty plate
                    counters[c].item.item = self.item
                    self.item = None
                
    def chop(self, c, counters):
        if type(counters[c]) == CuttingBoard and type(counters[c].item) == Food:
            counters[c].item.chopped = True
    
    def wash(self, c, counters):
        if type(counters[c]) == Wash and counters[c].plateCount != 0:
            counters[c].plateCount -= 1
            counters[c-1].plateCount += 1
            
def makeCounters():
    counters=[]
    #Left Top Right Bottom
    c1 = Counter(350, 380, 390, 415)
    c2 = Counter(390, 380, 440, 415)
    c3 = Counter(440, 380, 490, 415)
    c4 = Trash(490, 380, 540, 415)
    c5 = Counter(540, 380, 590, 415)
    c6 = Counter(590, 380, 640 ,415)
    c7 = Counter(640, 380, 685, 415)
    
    c8 = FoodCrate(495, 210, 530, 235, Food('onion'))
    c9 = Counter(495, 240, 532, 270)
    c10 = FoodCrate(495, 270, 535, 300, Food('carrot'))
    c11 = Counter(495, 300, 535, 340)
    c12 = FoodCrate(495, 340, 535, 380, Food('potato'))
    
    c13 = Counter(230, 465, 270, 510)
    c14 = Counter(270, 465, 335 , 510)
    c15 = WashReturn(335, 465, 385, 510)
    c16 = Wash(385, 465, 440, 510)
    c17 = Counter(440, 465, 490, 510)
    c18 = Counter(490, 465, 545, 510)
    c19 = Counter(545, 465, 600, 510)
    c20 = PlateReturn(600, 465, 645, 510)
    c21 = Serve(645, 465, 760, 510)
    c22 = Counter(760, 465, 810, 510)
    
    c23 = Counter(263, 337, 301, 376)
    c24 = Counter(270, 305, 309, 337)
    c25 = Counter(280, 265, 315, 305)
    c26 = Counter(291, 231, 323, 266)
    c27 = Counter(300, 207, 330, 230)
    
    c28 = CuttingBoard(340, 180, 375, 208)
    c29 = Counter(375, 180, 415, 208)
    c30 = CuttingBoard(415, 180, 455, 208)
    c31 = Counter(455, 180, 495, 208)
    c32 = Counter(495, 180, 535, 208)
    c33 = Counter(535, 180, 570, 208)
    c34 = Stove(570, 180, 610, 208)
    c35 = Counter(610, 180, 650, 208)
    c36 = Stove(650, 180, 690, 208)
    c37 = Counter(690, 180, 730, 208)
    
    counters.append(c1)
    counters.append(c2)
    counters.append(c3)
    counters.append(c4)
    counters.append(c5)
    counters.append(c6)
    counters.append(c7)
    counters.append(c8)
    counters.append(c9)
    counters.append(c10)
    counters.append(c11)
    counters.append(c12)
    counters.append(c13)
    counters.append(c14)
    counters.append(c15)
    counters.append(c16)
    counters.append(c17)
    counters.append(c18)
    counters.append(c19)
    counters.append(c20)
    counters.append(c21)
    counters.append(c22)
    counters.append(c23)
    counters.append(c24)
    counters.append(c25)
    counters.append(c26)
    counters.append(c27)
    counters.append(c28)
    counters.append(c29)
    counters.append(c30)
    counters.append(c31)
    counters.append(c32)
    counters.append(c33)
    counters.append(c34)
    counters.append(c35)
    counters.append(c36)
    counters.append(c37)
    
    counters[4].item = Plate()
    counters[5].item = Plate()
    
    return counters

def getColor(s):
        if s == 'carrot':
            return(214, 125, 5)
        elif s == 'potato':
            return(128,0,128)
        elif s == 'onion':
            return(255,248,220) 
        elif s == 'onion soup':
            return(0,0,0)    

def drawFood(screen, x,y,size, item):
    color = getColor(item.type)
    if item.chopped == False:
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, color, rect)
    else:
        pygame.draw.circle(screen, color, (x, y),size)
    
def playGame():
    animation_increment=10
    clock_tick_rate= 20
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    background_image = pygame.image.load("Images/Background1000NoPlates.jpg").convert()
    plateImage = pygame.image.load("Images/Plate.png").convert_alpha()
    dirtyPlateImage = pygame.image.load("Images/DirtyPlate.png").convert_alpha()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)


    dead = False
    p1 = Player()
    counters = makeCounters()
    c = -1
    
    seconds = 0
    milliseconds = 0
    timer = 360
    
    while(dead==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = True
        pressedKeys = pygame.key.get_pressed()
        
        if pressedKeys[pygame.K_x] == 1:
            pygame.quit()
        
        if pressedKeys[pygame.K_LEFT] == 1:
            p1.move('left', counters)
            c = p1.lookAtCounter(counters, screen)
            
        if pressedKeys[pygame.K_RIGHT] == 1:
            p1.move('right', counters)
            c = p1.lookAtCounter(counters, screen)

        if pressedKeys[pygame.K_UP] == 1:
            p1.move('up', counters)
            c = p1.lookAtCounter(counters, screen)

        if pressedKeys[pygame.K_DOWN] == 1:
            p1.move('down', counters)
            c = p1.lookAtCounter(counters, screen)
            
        if pressedKeys[pygame.K_q] == 1:
            if p1.item == None or str(p1.item) == 'Plate':
                p1.pickUp(c, counters)
        if pressedKeys[pygame.K_e] == 1:
            if p1.item != None:
                p1.putDown(c, counters)
        if pressedKeys[pygame.K_r] == 1:
            p1.chop(c, counters)
        if pressedKeys[pygame.K_t] == 1:
            p1.wash(c, counters)
        
        screen.blit(background_image, [0, 0])
        pygame.draw.rect(screen, (0,0,255), p1.p)

        if c != -1:
            counter = counters[c]
            pygame.draw.rect(screen, (0,255,0), counter.r)
                    
        if p1.item != None:
            if str(p1.item) == 'Plate':
                if p1.item.dirty == False:
                    screen.blit(plateImage,(p1.lookX,p1.lookY))
                else:
                    screen.blit(dirtyPlateImage, (p1.lookX, p1.lookY))
                if p1.item.item != None:
                    drawFood(screen, p1.lookX, p1.lookY, p1.size//2, p1.item.item)
            elif str(p1.item) == 'onion soup':
                drawFood(screen, p1.lookX, p1.lookY, p1.size, p1.item)
            else:
                drawFood(screen, p1.lookX, p1.lookY, p1.size//2, p1.item)
    
        for counter in counters:
            if type(counter) == Stove:
                counter.cook()
                if str(counter.dish) == 'onion soup':
                    dColor = (0,0,0)
                    dish = pygame.Rect(counter.left+counter.width//6,
                                    counter.top+counter.height//6, 
                                    p1.size,
                                    p1.size)
                    pygame.draw.rect(screen, dColor, dish)
                else:
                    if counter.food1 != None:
                        cColor = getColor(counter.food1.type)
                        pygame.draw.circle(screen, cColor, 
                            (counter.left+counter.width//4, 
                            counter.top+counter.height//6), p1.size//3)
                            
                    if counter.food2 != None:
                        cColor = getColor(counter.food2.type)
                        pygame.draw.circle(screen, cColor, 
                            (counter.left+counter.width//2, 
                            counter.top+counter.height//8), p1.size//3)
                            
                    if counter.food3 != None:
                        cColor = getColor(counter.food3.type)
                        pygame.draw.circle(screen, cColor, 
                            (counter.left+4*counter.width//5, 
                            counter.top+counter.height//6), p1.size//3)
            elif type(counter) == PlateReturn or type(counter) == Wash:
                if counter.plateCount != 0:
                    screen.blit(dirtyPlateImage,(counter.left,counter.top))
            elif type(counter) == WashReturn:
                if counter.plateCount != 0:
                    screen.blit(plateImage,(counter.left,counter.top))
            else:
                if counter.item != None:
                    if str(counter.item) == 'Plate':
                        if counter.item.dirty == False:
                            screen.blit(plateImage,(counter.left,counter.top))
                        else:
                            screen.blit(dirtyPlateImage,(counter.left,counter.top))
                        if counter.item.item != None:
                            drawFood(screen, counter.left+counter.width//2, 
                            counter.top+counter.height//4, p1.size//2,
                            counter.item.item)
                    else:
                        drawFood(screen, counter.left+counter.width//2, 
                            counter.top+counter.height//4, p1.size//2,
                            counter.item)
                            
        textsurface = myfont.render(str(p1.score), False, (0, 0, 0))
        screen.blit(textsurface,(40,500))
        
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        
        textsurface1 = myfont.render(str(timer-seconds), False, (0, 0, 0))
        screen.blit(textsurface1,(900,490))
        
        milliseconds += clock.tick(clock_tick_rate)
        
        pygame.display.flip()
