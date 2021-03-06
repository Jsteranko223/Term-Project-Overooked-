import pygame
import time
import random

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
    def __repr__(self):
        return(self.food)

class PlateReturn(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0

class Wash(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0
        self.wash = 0

class WashReturn(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.plateCount = 0
        
class Stove(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.item = Pot()
        
    def cook(self):
        if str(self.item) == 'Pot':
            if self.item.food1 != None and str(self.item.food1) != 'fire' and \
               self.item.fire <= 40:
                if self.item.cook > 0:
                    self.item.cook -= 1
                if self.item.cook == 0:
                    self.item.fire += 1
                    food = [str(self.item.food1), str(self.item.food2), 
                            str(self.item.food3)]
                    if food.count('onion') == 3:
                        self.item.dish = Dish('onion soup')
                        self.item.dish.food1 = Food(food[0])
                        self.item.dish.food2 = Food(food[1])
                        self.item.dish.food3 = Food(food[2])
                    elif food.count('potato') == 1 and \
                         food.count('onion') == 1 and food.count('carrot') == 1:
                        self.item.dish = Dish('stew')
                        self.item.dish.food1 = Food(food[0])
                        self.item.dish.food2 = Food(food[1])
                        self.item.dish.food3 = Food(food[2])
                    elif food.count('potato') == 2 and \
                            food.count('carrot') == 1:
                        self.item.dish = Classes.Dish('potatocarrot')
                        self.item.dish.food1 = Classes.Food(food[0])
                        self.item.dish.food2 = Classes.Food(food[1])
                        self.item.dish.food3 = Classes.Food(food[2])
            
class Trash(Counter):
    pass

class Serve(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.recipes = [generateRecipes(), None, None, None]
        self.recipeTimes = [0,0,0,0]
        self.score = 0

class CuttingBoard(Counter):
    pass
    
class Dish(object):
    def __init__(self,type):
        self.type = type
        self.food1 = None
        self.food2 = None
        self.food3 = None
        self.chopped = False
    def __repr__(self):
        return(self.type)
    
class Food(object):
    def __init__(self, type):
        self.type = type
        self.chopped = False
        self.chop = 0
        
    def __repr__(self):
        return(self.type)
        
class Plate(object):
    def __init__(self):
        self.item = None
        self.dirty = False
    def __repr__(self):
        return('Plate')

class Pot(object):
    def __init__(self):
        self.item = None
        self.food1 = None
        self.food2 = None
        self.food3 = None
        self.fire = 0
        self.dish = None
        self.cook = 0
        self.cookTime = 0
            
    def __repr__(self):
        return('Pot')
        
class Extinguisher(object):
    def __init__(self):
        pass
    def __repr__(self):
        return('Extinguisher')
            
            

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 10
        self.p = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lookX = self.x+self.width//4
        self.lookY = self.y+self.height//2 
        self.direction = 'down'
        self.item = None
        self.action = False
        self.c = -1
        self.character = (0,0,255)
        self.dash = False
        self.s = ''
        self.playerNumber = ''

    def move(self, key, counters, player):
        if self.dash == True:
            modifier = 4
        else:
            modifier = 1
        if key == 'left':
            self.x -= self.speed*modifier
            self.lookX = self.x-self.width//2
            self.lookY = self.y+self.height//4
            self.direction = 'left'
        if key == 'right':
            self.x += self.speed*modifier
            self.lookX = self.x+self.width
            self.lookY = self.y+self.height//4
            self.direction = 'right'
        if key == 'up':
            self.y -= self.speed*modifier
            self.lookX = self.x+self.width//4
            self.lookY = self.y-self.height//2
            self.direction = 'up'
        if key == 'down':
            self.y += self.speed*modifier
            self.lookX = self.x+self.width//4
            self.lookY = self.y+self.height
            self.direction = 'down'
            
        for counter in counters:
            if self.detectCollision(self.x, self.y, self.width, self.height, counter):
                if key == 'left':
                    self.x += self.speed*modifier
                    
                if key == 'right':
                    self.x -= self.speed*modifier

                if key == 'up':
                    self.y += self.speed*modifier
                    
                if key == 'down':
                    self.y -= self.speed*modifier
        
        if self.detectCollision(self.x, self.y, self.width,self.height, player):
            if key == 'left':
                self.x += self.speed*modifier
                
            if key == 'right':
                self.x -= self.speed*modifier

            if key == 'up':
                self.y += self.speed*modifier
                
            if key == 'down':
                self.y -= self.speed*modifier
                
        if self.x < 240 or (self.y > 500 and self.x > 790) or (self.y <500 and self.x > 750) or \
        (self.y<300  and self.x > 725): 
            self.x = 400
            self.y = 250
            if self.playerNumber == 'a':
                self.x = 400
                self.y = 250
                if self.detectCollision(self.x, self.y, self.width,
                    self.height, player):
                    self.x = 650
                    self.y = 250
            elif self.playerNumber == 'b':
                self.x = 650
                self.y = 250
                if self.detectCollision(self.x, self.y, self.width,
                    self.height, player):
                    self.x = 400
                    self.y = 250
                
            if str(self.item) == 'Plate':
                counters[19].plateCount += 1
            elif str(self.item) == 'Extinguisher':
                if str(counters[30].item) == 'Plate':
                    counters[19].plateCount += 1
                elif str(counters[30].item) == 'Pot':
                    if counters[33].item == None:
                        counters[33].item = Pot()
                    elif counters[35].item == None:
                        counters[35].item = Pot()
                counters[30].item = Extinguisher()
            elif str(self.item) == 'Pot':
                if counters[33].item == None:
                    counters[33].item = Pot()
                elif counters[35].item == None:
                    counters[35].item = Pot()
            self.item = None
                    
        self.look = pygame.Rect(self.lookX, self.lookY, self.width//2,
                                self.height//2)
        self.p = pygame.Rect(self.x, self.y, self.width, self.height)

    def detectCollision(self, px, py, pwidth, pheight, other):
        if type(other) == Player:
            if other.x+other.width >= px and px >= other.x and \
            other.y + other.height >= py and py >= other.y:
                return True
                
            if other.x+other.width >= px+pwidth and px+pwidth >= other.x and \
            other.y+other.height >= py and py >=other.y:
                return True
                
            if other.x+other.width>= px and px >= other.x and \
            other.y + other.height >= py+pheight and py+pheight >= other.y:
                return True
                
            if other.x+other.width >= px+pwidth and px+pwidth >= other.x and \
            other.y+other.height >= py+pheight and py+pheight >= other.y:
                return True
        else:
            if other.left+other.width >= px and px >= other.left and \
            other.top + other.height >= py and py >= other.top:
                return True
                
            if other.left+other.width >= px+pwidth and px+pwidth >= other.left and \
            other.top+other.height >= py and py >=other.top:
                return True
                
            if other.left+other.width>= px and px >= other.left and \
            other.top + other.height >= py+pheight and py+pheight >= other.top:
                return True
                
            if other.left+other.width >= px+pwidth and px+pwidth >= other.left and \
            other.top+other.height >= py+pheight and py+pheight >= other.top:
                return True
            
        return False
    
    def lookAtCounter(self, counters, screen):
        for i in range(len(counters)):
            if self.detectCollision(self.lookX,self.lookY,self.width//2, 
                                    self.height//4, counters[i]):
                return i
        return -1
    
    def pickUp(self, c, counters):
        if c != -1:
            #Pick up pot from stove
            if str(counters[c].item) == 'Pot' and self.item == None:
                if counters[c].item.fire < 40:
                    self.item = counters[c].item
                    counters[c].item = None
             #Pick up dish from stove with plate   
            elif str(self.item) == 'Plate' and \
            str(counters[c].item) == 'Pot' and \
            counters[c].item.dish != None and self.item.dirty == False and \
            counters[c].item.fire < 40: 
                self.item.item = counters[c].item.dish
                counters[c].item.dish = None
                counters[c].item.food1 = None
                counters[c].item.food2 = None
                counters[c].item.food3 = None
                counters[c].item.cook = 0
                counters[c].item.cookTime = 0
                counters[c].item.fire = 0
            else:
                if self.item == None: #Empty hands to pick up
                #Pick up dirty dish from return
                    if type(counters[c]) == PlateReturn: 
                        if counters[c].plateCount != 0:
                            counters[c].plateCount -= 1                   
                            self.item = Plate()
                            self.item.dirty = True
                     #Pick up clean dish from wash       
                    elif type(counters[c]) == WashReturn: 
                        if counters[c].plateCount != 0:
                            counters[c].plateCount -= 1                   
                            self.item = Plate()
                    else:
                        #Pick up from counter
                        if counters[c].item != None: 
                            self.item = counters[c].item 
                            counters[c].item = None
                        #Pick up from food crate  
                        elif type(counters[c]) == FoodCrate: 
                            self.item = Food(str(counters[c].food))
                            self.item.chopped = False
                    
    
    def putDown(self, c, counters):
        if c != -1:
            if str(self.item) == 'Pot': #Carrying Pot
                if type(counters[c]) == Trash:
                    self.item.dish  = None
                    self.item.food1 = None
                    self.item.food2 = None
                    self.item.food3 = None
                elif str(counters[c].item) == 'Plate' and \
                counters[c].item.dirty == False and self.item.dish != None:
                    counters[c].item.item = self.item.dish
                    self.item.dish = None
                    self.item.food1 = None
                    self.item.food2 = None
                    self.item.food3 = None
                elif counters[c].item == None:
                    if type(counters[c]) == Counter or type(counters[c]) == Stove:
                        counters[c].item = self.item
                        self.item = None
            elif str(self.item) == 'Plate':  #Carrying plate
                if self.item.dirty == False: #Cannot use dirty plate
                    if self.item.item != None:
                        if type(counters[c]) == Serve: #Serve Food
                            if type(self.item.item) == Dish:
                                #Check if dish was ordered
                                for i in range(len(counters[20].recipes)):
                                    if str(self.item.item) == \
                                       str(counters[20].recipes[i]):
                                        if counters[20].recipeTimes[i] > 45:
                                            counters[20].score += 1
                                        elif counters[20].recipeTimes[i] > 30:
                                            counters[20].score += 2
                                        elif counters[20].recipeTimes[i] > 15:
                                            counters[20].score += 3
                                        else:
                                            counters[20].score += 4
                                        counters[20].recipes[i] = None
                                        counters[20].recipeTimes[i] = 0
                                        #Add new recipe
                                        if counters[20].recipes.count(None) == 4:
                                            counters[20].recipes[0] = generateRecipes()
                                        for i in range(len(counters[20].recipes)-1):
                                            if counters[20].recipes[i] == None and \
                                               counters[20].recipes[i+1] != None:
                                                counters[20].recipes[i] = \
                                                counters[20].recipes[i+1]
                                                counters[20].recipes[i+1] = None
                                                counters[20].recipeTimes[i] = \
                                                counters[20].recipeTimes[i+1]
                                                counters[20].recipeTimes[i+1] = 0 
                                        break
                                self.item = None
                                counters[19].plateCount += 1
                                    
                         #Put food on stove from plate       
                        elif type(counters[c]) == Stove:  
                            if str(counters[c].item) == 'Pot' and \
                               counters[c].item.fire < 40:
                                if self.item.item.chopped == True:
                                    if counters[c].item.food1 == None:
                                        counters[c].item.food1 = self.item.item
                                        self.item.item = None
                                        counters[c].item.cook += 100
                                        counters[c].item.cookTime += 100
                                        counters[c].item.fire = 0
                                    elif counters[c].item.food2 == None:
                                        counters[c].item.food2 = self.item.item
                                        counters[c].item.fire = 0
                                        self.item.item = None
                                        counters[c].item.cook += 100
                                        counters[c].item.cookTime += 100
                                    elif counters[c].item.food3 == None:
                                        counters[c].item.food3 = self.item.item
                                        counters[c].item.fire = 0
                                        self.item.item = None
                                        counters[c].item.cook += 100
                                        counters[c].item.cookTime += 100
                                        
                         #Throw away food on plate               
                        elif type(counters[c]) == Trash:  
                            self.item.item = None
                        #Food on plate to cutting board
                        elif type(counters[c]) == CuttingBoard:
                            counters[c].item = self.item.item
                            self.item.item = None
                else:
                    if type(counters[c]) == Wash:
                        self.item = None
                        counters[c].plateCount += 1
                #Put plate on empty counter
                if type(counters[c]) == Counter and counters[c].item == None: 
                    counters[c].item = self.item
                    self.item = None
            elif str(self.item) == 'Extinguisher':
                #Put extinguisher on empty counter
                if type(counters[c]) == Counter and counters[c].item == None: 
                    counters[c].item = self.item
                    self.item = None
            elif self.item != None: #Carrying food
                if type(counters[c]) == Trash: #Put in Trash
                    self.item = None
                if str(counters[c].item) == 'Pot' and \
                   counters[c].item.fire < 40: #Put food in pot
                    if self.item.chopped == True:
                        if counters[c].item.food1 == None:
                            counters[c].item.food1 = self.item
                            counters[c].item.fire = 0
                            self.item = None
                            counters[c].item.cook += 100
                            counters[c].item.cookTime += 100
                        elif counters[c].item.food2 == None:
                            counters[c].item.food2 = self.item
                            counters[c].item.fire = 0
                            counters[c].item.cook += 100
                            counters[c].item.cookTime += 100
                            self.item = None
                        elif counters[c].item.food3 == None:
                            counters[c].item.food3 = self.item
                            counters[c].item.fire = 0
                            counters[c].item.cook += 100
                            counters[c].item.cookTime += 100
                            self.item = None
                        
                elif counters[c].item == None and \
                        type(counters[c]) != PlateReturn:  #Put on empty Counter
                    counters[c].item = self.item
                    self.item = None
                elif str(counters[c].item) == 'Plate' and \
                    counters[c].item.item == None and \
                    counters[c].item.dirty == False: #Put on empty plate
                    counters[c].item.item = self.item
                    self.item = None
                
    def chop(self, c, counters):
        if self.item == None:
            if type(counters[c]) == CuttingBoard and \
               type(counters[c].item) == Food:
                if counters[c].item.chop < 50:
                    counters[c].item.chop += 1
                else:
                    counters[c].item.chopped = True
                    
    def wash(self, c, counters):
        if self.item == None:
            if type(counters[c]) == Wash and counters[c].plateCount != 0:
                counters[c].wash += 1
                if counters[c].wash == 50:
                    counters[c].plateCount -= 1
                    counters[c-1].plateCount += 1
                    counters[c].wash = 0
                    
    def extinguish(self, c, counters):
        if str(counters[c].item) == 'Pot' and counters[c].item.fire > 40:
            counters[c].item = Pot()
            counters[c].item.food1 = Food('fire')
            counters[c].item.food2 = Food('fire')
            counters[c].item.food3 = Food('fire')

                
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
    c32 = Counter(495, 180, 540, 208)
    c33 = Counter(540, 180, 570, 208)
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
    counters[30].item = Extinguisher()
    counters[33].item = Pot()
    counters[35].item = Pot()
    
    return counters    
        
def getImage(s, chopped, raw):
    if raw == False:
        if s == 'onion':
            image = pygame.image.load("Images/CookingOnion.png")\
                    .convert_alpha()
        elif s == 'carrot':
            image = pygame.image.load("Images/CookingCarrot.png")\
                    .convert_alpha()
        elif s == 'potato':
            image = pygame.image.load("Images/CookingPotato.png")\
                    .convert_alpha()
        elif s == 'onion soup':
            image = pygame.image.load("Images/RecipeOnionSoup.png").convert_alpha()
        elif s == 'stew':
            image = pygame.image.load("Images/RecipeStew.png").convert_alpha()
        elif s == 'potatocarrot':
            image = pygame.image.load("Images/RecipePotatoCarrot.png").convert_alpha()
        elif s == 'None':
            image = pygame.image.load("Images/Empty.png").convert_alpha()
        elif s == 'fire':
            image = pygame.image.load("Images/CookingFire.png").convert_alpha()

    else:
        if s == 'onion soup' or s == 'stew' or s == 'potatocarrot':
            image = pygame.image.load("Images/OnionSoup.png").convert_alpha()
        elif s == 'onion':
            if chopped == False:
                image = pygame.image.load("Images/Onion.png").convert_alpha()
            else:
                image = pygame.image.load("Images/ChoppedOnion.png")\
                        .convert_alpha()
        elif s == 'potato':
            if chopped == False:
                image = pygame.image.load("Images/Potato.png").convert_alpha()
            else:
                image = pygame.image.load("Images/ChoppedPotato.png")\
                        .convert_alpha()
        elif s == 'carrot':
            if chopped == False:
                image = pygame.image.load("Images/Carrot.png").convert_alpha()
            else:
                image = pygame.image.load("Images/ChoppedCarrot.png")\
                        .convert_alpha()
    return image
        
def drawFood(screen, x,y, item, stove):
    if stove == True:
        if (str(item)) == 'None':
            image = getImage('None', False, False)
        else:
            image = getImage(item.type, False, False)
    else:
        if item.chopped == False:
            image = getImage(item.type, False, True)
        else:
            image = getImage(item.type, True, True)
    screen.blit(image, (x,y))
    

def generateRecipes():
    lst = [Dish('onion soup'), Dish('stew'), Dish('potatocarrot')]
    return(lst[random.randint(0,2)])
   
def playGame(playerCount, character):
    clock_tick_rate= 20
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    backgroundImage = pygame.image.load("Images/BackgroundFinal.png")\
                      .convert_alpha()
    plateImage = pygame.image.load("Images/Plate.png").convert_alpha()
    dirtyPlateImage = pygame.image.load("Images/DirtyPlate.png").convert_alpha()
    extinguisherImage = pygame.image.load("Images/ExtinguisherFinal.png")\
                        .convert_alpha()
    potImage = pygame.image.load("Images/Pot.png").convert_alpha()
    fireImage = pygame.image.load("Images/Fire.png").convert_alpha()


    myfont = pygame.font.SysFont('Segoe UI Black', 30)

    dead = False
    p1a = Player(400,250)
    p1b = Player(600,250)
    player = p1a
    other = p1b
    players = [p1a, p1b]
    p1a.s = character
    s = "Images/"+p1a.s+"Right.png"
    p1a.character = pygame.image.load(s).convert_alpha()
    
    if character == ('Snowman'):
        p1b.s = 'Penguin'
        p1b.character = pygame.image.load("Images/PenguinRight.png")\
                            .convert_alpha()
    else:
        p1b.s = 'Snowman'
        p1b.character = pygame.image.load("Images/SnowmanRight.png")\
                            .convert_alpha()
    p1a.playerNumber = 'a'
    p1b.playerNumber = 'b'

    counters = makeCounters()
    
    switch = False
    action = False
    
    seconds = 0
    milliseconds = 0
    timer = 180
    pygame.mixer.music.load('Images/music.wav')
    pygame.mixer.music.play(-1)
    while(dead==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:                    
                    #Pick up with hands
                    if player.item == None:
                        player.pickUp(player.c, counters)
                    #Plate
                    elif str(player.item) == 'Plate':
                        if player.item.item != None:
                            player.putDown(player.c, counters)
                        elif str(counters[player.c].item) == 'Pot' and \
                             player.item.dirty == False and \
                             counters[player.c].item.dish != None:
                            player.pickUp(player.c, counters)
                        else:
                            player.putDown(player.c, counters)
                    #Put down item
                    elif player.item != None:
                        player.putDown(player.c, counters)
                    action = False
                if event.key == pygame.K_r:
                    if player == p1a:
                        player = p1b
                        other = p1a
                    else:
                        player = p1a
                        other = p1b
                    switch = False
                    player.c = player.lookAtCounter(counters, screen)
                elif event.key == pygame.K_SPACE:
                    player.dash = True

        
        pressedKeys = pygame.key.get_pressed()
        
        screen.blit(backgroundImage, (0,0))

        if pressedKeys[pygame.K_x] == 1 or (timer-seconds) <= 0:
            break
        if pressedKeys[pygame.K_LEFT] == 1 or pressedKeys[pygame.K_a] == 1:
            player.move('left', counters, other)
            player.c = player.lookAtCounter(counters, screen)
            player.action = False
            s = "Images/"+player.s+"Left.png"
            player.character = pygame.image.load(s).convert_alpha()
            
        if pressedKeys[pygame.K_RIGHT] == 1 or pressedKeys[pygame.K_d] == 1:
            player.move('right', counters, other)
            player.c = player.lookAtCounter(counters, screen)
            player.action = False
            s = "Images/"+player.s+"Right.png"
            player.character = pygame.image.load(s).convert_alpha()

        if pressedKeys[pygame.K_UP] == 1 or pressedKeys[pygame.K_w] == 1:
            player.move('up', counters, other)
            player.c = player.lookAtCounter(counters, screen)
            player.action = False

        if pressedKeys[pygame.K_DOWN] == 1 or pressedKeys[pygame.K_s] == 1:
            player.move('down', counters, other)
            player.c = player.lookAtCounter(counters, screen)
            player.action = False
                
        if pressedKeys[pygame.K_e] == 1:
            player.action = True
        
        player.dash = False
            
        for p in players:    
            if p.action == True:
                if type(counters[p.c]) == CuttingBoard:
                    p.chop(p.c, counters)
                    if type(counters[p.c].item) == Food and counters[p.c].item.chopped == True:
                        action = False
                elif type(counters[p.c]) == Wash:
                    p.wash(p.c, counters)
                    if counters[p.c].plateCount == 0:
                        action = False
                elif str(p.item) == 'Extinguisher':
                    p.extinguish(p.c, counters)
                    aciton = False
        if player.c != -1:
            counter = counters[player.c]
            pygame.draw.rect(screen, (255,230, 0), counter.r)   
            
        for counter in counters:
            if type(counter) == PlateReturn or type(counter) == Wash:
                if counter.plateCount != 0:
                    screen.blit(dirtyPlateImage,(counter.left,counter.top))
                    if type(counter) == Wash and counter.wash > 0:
                        r = pygame.Rect(counter.left-5, counter.bottom+10, 
                                        counter.wash, 10)
                        pygame.draw.rect(screen, (0,255,0), r)
            elif type(counter) == WashReturn:
                if counter.plateCount != 0:
                    screen.blit(plateImage,(counter.left,counter.top))
            elif type(counter) == Serve:
                for i in range(len(counter.recipes)):
                    if counter.recipes[i] != None:
                        drawFood(screen, 8+90*i, 32, counter.recipes[i], True)
                        r = pygame.Rect(8+90*i, 32, 
                                    65-counter.recipeTimes[i], 10)
                        pygame.draw.rect(screen, (0,255,0), r)
                        if counter.recipeTimes[i] >= 65:
                            counter.recipes[i] = None
                            counter.recipeTimes[i] = 0 
                            counter.score -= 1
                            if counter.recipes.count(None) == 4:
                                counter.recipes[0] = generateRecipes()
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
                            screen.blit(plateImage,(counter.left,counter.top))
                        else:
                            screen.blit(dirtyPlateImage,
                            (counter.left,counter.top))
                        if counter.item.item != None: #Food on plate on counter
                            drawFood(screen, counter.left, 
                            counter.top,counter.item.item, False)
                            if type(counter.item.item) == Dish:
                                drawFood(screen, counter.left-player.width//4, 
                                counter.top-player.height, 
                                counter.item.item.food1, True)
                                drawFood(screen, counter.left+4*player.width//6, 
                                counter.top-player.height, 
                                counter.item.item.food2, True)
                                drawFood(screen, counter.left-player.width//4, 
                                counter.top, counter.item.item.food3, True)
                            elif counter.item.item.chop > 0 and \
                               counter.item.item.chopped == False:
                                r = pygame.Rect(counter.left-5, counter.top-10, 
                                            counter.item.item.chop, 10)
                                pygame.draw.rect(screen, (0,255,0), r)
                            
                            
                                
                    elif str(counter.item) == 'Extinguisher':
                        screen.blit(extinguisherImage, 
                        (counter.left, counter.top))
                        
                    elif str(counter.item) == 'Pot':
                        screen.blit(potImage, (counter.left, counter.top-5))
                        if counter.item.fire > 40:
                            screen.blit(fireImage, (counter.left, counter.top-65))
                        else:
                            drawFood(screen, counter.left-counter.width//2, 
                            counter.top-counter.height, counter.item.food1, True)
                            drawFood(screen, counter.left+counter.width//2, 
                            counter.top-counter.height, counter.item.food2, True)
                            drawFood(screen, counter.left-counter.width//2, 
                            counter.top, counter.item.food3, True)
                            
                            if counter.item.dish != None:
                                drawFood(screen, counter.left, counter.top-5,
                                counter.item.dish, False)
                        
                    else:
                        drawFood(screen, counter.left, 
                            counter.top, counter.item, False)
                        if counter.item.chop > 0 and \
                           counter.item.chopped == False:
                            r = pygame.Rect(counter.left-5, counter.top-10, 
                                        counter.item.chop, 10)
                            pygame.draw.rect(screen, (0,255,0), r)
            if type(counter) == Stove:
                counter.cook()
                if str(counter.item) == 'Pot' and \
                counter.item.food1 != None and \
                str(counter.item.food1) != 'fire':
                    if counter.item.fire > 0 and counter.item.fire < 40:
                        progress = 50*(1 - (counter.item.fire/40))
                        r = pygame.Rect(counter.left-5, counter.top-10, 
                        progress, 10)
                        pygame.draw.rect(screen, (255,0,0), r)
                    elif counter.item.fire <= 40:
                        progress = 50*(1 - (counter.item.cook/counter.item.\
                        cookTime))
                        r = pygame.Rect(counter.left-5, counter.top-10, 
                        progress, 10)
                        pygame.draw.rect(screen, (0,255,0), r)
                
        screen.blit(p1a.character,(p1a.x-25,p1a.y-25))
        screen.blit(p1b.character,(p1b.x-25,p1b.y-25))

        
        
            
        for p in players:
            if p.item != None:
                if str(p.item) == 'Plate':
                    if p.item.dirty == False:
                        screen.blit(plateImage,(p.lookX,p.lookY))
                    else:
                        screen.blit(dirtyPlateImage, (p.lookX, p.lookY))
                    if p.item.item != None:
                        drawFood(screen, p.lookX, p.lookY, p.item.item, False)
                        if type(p.item.item) == Dish:
                            drawFood(screen, p.lookX-p.width//4, 
                            p.lookY-p.height, p.item.item.food1, True)
                            drawFood(screen, p.lookX+4*p.width//6, 
                            p.lookY-p.height, p.item.item.food2, True)
                            drawFood(screen, p.lookX-p.width//4, 
                            p.lookY, p.item.item.food3, True)
                        elif p.item.item.chop > 0 and p.item.item.chopped == False:
                            r = pygame.Rect(p.lookX-5, p.lookY-10, 
                                        p.item.item.chop, 10)
                            pygame.draw.rect(screen, (0,255,0), r)
                            
                elif str(p.item) == 'Pot':
                    screen.blit(potImage,(p.lookX, p.lookY))
                    drawFood(screen, p.lookX-p.height//4, 
                    p.lookY-p.width, p.item.food1, True)
                    drawFood(screen, p.lookX+4*p.height//6, 
                    p.lookY-p.width, p.item.food2, True)
                    drawFood(screen, p.lookX-p.height//4, 
                    p.lookY, p.item.food3, True)
                    
                    if p.item.dish != None:
                        drawFood(screen, p.lookX, p.lookY, p.item.dish, False)
    
                elif str(p.item) == 'Extinguisher':
                        screen.blit(extinguisherImage,(p.lookX,p.lookY))
                else:
                    drawFood(screen, p.lookX, p.lookY, p.item, False)
                    if p.item.chop > 0 and p.item.chopped == False:
                        r = pygame.Rect(p.lookX-5, p.lookY-10, 
                                    p.item.chop, 10)
                        pygame.draw.rect(screen, (0,255,0), r)
                
    
                    
                            
        textsurface = myfont.render(str(counters[20].score), False, (0, 0, 0))
        screen.blit(textsurface,(52,500))
        
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
            for i in range(len(counters[20].recipes)):
                if counters[20].recipes[i] != None:
                    counters[20].recipeTimes[i] += 1
            if (timer-seconds) % 30 == 0:
                for i in range(len(counters[20].recipes)):
                    if counters[20].recipes[i] == None:
                        counters[20].recipes[i] = generateRecipes()
                        break
        
        textsurface1 = myfont.render(str(timer-seconds), False, (0, 102, 0))
        screen.blit(textsurface1,(900,488))

        milliseconds += clock.tick(clock_tick_rate)
        
        pygame.display.flip()
    return(counters[20].score)