import pygame
import time
import random
import Classes

pygame.init()
pygame.font.init()

def cook(p):
    if str(p.item) == 'Pot':
        if p.item.food1 != None and str(p.item.food1) != 'fire' and \
            p.item.fire <= 40:
            if p.item.cook > 0:
                p.item.cook -= 1
            if p.item.cook == 0:
                p.item.fire += 1
                food = [str(p.item.food1), str(p.item.food2), 
                        str(p.item.food3)]
                if food.count('onion') == 3:
                    p.item.dish = Classes.Dish('onion soup')
                    p.item.dish.food1 = Classes.Food(food[0])
                    p.item.dish.food2 = Classes.Food(food[1])
                    p.item.dish.food3 = Classes.Food(food[2])
                elif food.count('potato') == 1 and \
                        food.count('onion') == 1 and food.count('carrot') == 1:
                    p.item.dish = Classes.Dish('stew')
                    p.item.dish.food1 = Classes.Food(food[0])
                    p.item.dish.food2 = Classes.Food(food[1])
                    p.item.dish.food3 = Classes.Food(food[2])
    return p
                    
def move(p, key, counters):
    if key == 'left':
        p.x -= p.speed
        p.lookX = p.x-p.width//2
        p.lookY = p.y+p.height//4
        p.direction = 'left'
    if key == 'right':
        p.x += p.speed
        p.lookX = p.x+p.width
        p.lookY = p.y+p.height//4
        p.direction = 'right'
    if key == 'up':
        p.y -= p.speed
        p.lookX = p.x+p.width//4
        p.lookY = p.y-p.height//2
        p.direction = 'up'
    if key == 'down':
        p.y += p.speed
        p.lookX = p.x+p.width//4
        p.lookY = p.y+p.height
        p.direction = 'down'
        
    for counter in counters:
        if detectCollision(p, p.x, p.y, p.width, p.height, counter):
            if key == 'left':
                p.x += p.speed
                
            if key == 'right':
                p.x -= p.speed

            if key == 'up':
                p.y += p.speed
                
            if key == 'down':
                p.y -= p.speed
            
    if p.x < 235 or (p.y > 300 and p.x > 790) or \
        (p.y<300  and p.x > 740):
        p.x = 400
        p.y = 250
        if str(p.item) == 'Plate':
            counters[19].plateCount += 1
        elif str(p.item) == 'Extinguisher':
            if str(counters[30].item) == 'Plate':
                counters[19].plateCount += 1
            elif str(counters[30].item) == 'Pot':
                if counters[33].item == None:
                    counters[33].item = Classes.Pot()
                elif counters[35].item == None:
                    counters[35].item = Classes.Pot()
            counters[30].item = Classes.Extinguisher()
        elif str(p.item) == 'Pot':
            if counters[33].item == None:
                counters[33].item = Classes.Pot()
            elif counters[35].item == None:
                counters[35].item = Classes.Pot()
        p.item = None
                
    p.look = pygame.Rect(p.lookX, p.lookY, p.width//2,
                            p.height//2)
    p.p = pygame.Rect(p.x, p.y, p.width, p.height)
    
    return p

def detectCollision(p, px, py, pwidth, pheight, other):
    if type(other) == Classes.Player:
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

def lookAtCounter(p, counters):
    for i in range(len(counters)):
        if detectCollision(p,p.lookX,p.lookY,p.width//2, p.height//4, counters[i]):
            return i
    return -1

def pickUp(p, c, counters):
    if c != -1:
        #Pick up pot from stove
        if str(counters[c].item) == 'Pot' and p.item == None:
            if counters[c].item.fire < 40:
                p.item = counters[c].item
                counters[c].item = None
            #Pick up dish from stove with plate   
        elif str(p.item) == 'Plate' and \
        str(counters[c].item) == 'Pot' and \
        counters[c].item.dish != None and p.item.dirty == False and \
        counters[c].item.fire < 40: 
            p.item.item = counters[c].item.dish
            counters[c].item.dish = None
            counters[c].item.food1 = None
            counters[c].item.food2 = None
            counters[c].item.food3 = None
            counters[c].item.cook = 0
            counters[c].item.cookTime = 0
            counters[c].item.fire = 0
        else:
            if p.item == None: #Empty hands to pick up
            #Pick up dirty dish from return
                if type(counters[c]) == Classes.PlateReturn: 
                    if counters[c].plateCount != 0:
                        counters[c].plateCount -= 1                   
                        p.item = Classes.Plate()
                        p.item.dirty = True
                    #Pick up clean dish from wash       
                elif type(counters[c]) == Classes.WashReturn: 
                    if counters[c].plateCount != 0:
                        counters[c].plateCount -= 1                   
                        p.item = Classes.Plate()
                else:
                    #Pick up from counter
                    if counters[c].item != None: 
                        p.item = counters[c].item 
                        counters[c].item = None
                    #Pick up from food crate  
                    elif type(counters[c]) == Classes.FoodCrate: 
                        p.item = Classes.Food(str(counters[c].food))
                        p.item.chopped = False
                

def putDown(p, c, counters):
    if c != -1:
        if str(p.item) == 'Pot': #Carrying Pot
            if type(counters[c]) == Classes.Trash:
                p.item.dish  = None
                p.item.food1 = None
                p.item.food2 = None
                p.item.food3 = None
            elif str(counters[c].item) == 'Plate' and \
            counters[c].item.dirty == False and p.item.dish != None:
                counters[c].item.item = p.item.dish
                p.item.dish = None
                p.item.food1 = None
                p.item.food2 = None
                p.item.food3 = None
            elif counters[c].item == None:
                if type(counters[c]) == Classes.Counter or type(counters[c]) == Classes.Stove:
                    counters[c].item = p.item
                    p.item = None
        elif str(p.item) == 'Plate':  #Carrying plate
            if p.item.dirty == False: #Cannot use dirty plate
                if p.item.item != None:
                    if type(counters[c]) == Classes.Serve: #Serve Food
                        if type(p.item.item) == Classes.Dish:
                            #Check if dish was ordered
                            for i in range(len(counters[20].recipes)):
                                if str(p.item.item) == \
                                    str(counters[20].recipes[i]):
                                    counters[20].recipes[i] = None
                                    counters[20].recipeTimes[i] = 0
                                    counters[20].score += 1
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
                            p.item = None
                            counters[19].plateCount += 1
                                
                        #Put food on stove from plate       
                    elif type(counters[c]) == Classes.Stove:  
                        if str(counters[c].item) == 'Pot' and \
                            counters[c].item.fire < 40:
                            if p.item.item.chopped == True:
                                counters[c].item.cook += 100
                                counters[c].item.cookTime += 100
                                if counters[c].item.food1 == None:
                                    counters[c].item.food1 = p.item.item
                                    p.item.item = None
                                elif counters[c].item.food2 == None:
                                    counters[c].item.food2 = p.item.item
                                    p.item.item = None
                                elif counters[c].item.food3 == None:
                                    counters[c].item.food3 = p.item.item
                                    p.item.item = None
                                return True
                        #Throw away food on plate               
                    elif type(counters[c]) == Classes.Trash:  
                        p.item.item = None
                    #Food on plate to cutting board
                    elif type(counters[c]) == Classes.CuttingBoard:
                        counters[c].item = p.item.item
                        p.item.item = None
            else:
                if type(counters[c]) == Classes.Wash:
                    p.item = None
                    counters[c].plateCount += 1
            #Put plate on empty counter
            if type(counters[c]) == Classes.Counter and counters[c].item == None: 
                counters[c].item = p.item
                p.item = None
        elif str(p.item) == 'Extinguisher':
            #Put extinguisher on empty counter
            if type(counters[c]) == Classes.Counter and counters[c].item == None: 
                counters[c].item = p.item
                p.item = None
        elif p.item != None: #Carrying food
            if type(counters[c]) == Classes.Trash: #Put in Trash
                p.item = None
            if str(counters[c].item) == 'Pot' and \
                counters[c].item.fire < 40: #Put food in pot
                if p.item.chopped == True:
                    counters[c].item.cook += 100
                    counters[c].item.cookTime += 100
                    if counters[c].item.food1 == None:
                        counters[c].item.food1 = p.item
                        p.item = None
                    elif counters[c].item.food2 == None:
                        counters[c].item.food2 = p.item
                        p.item = None
                    elif counters[c].item.food3 == None:
                        counters[c].item.food3 = p.item
                        p.item = None
                    
            elif counters[c].item == None and \
                    type(counters[c]) != Classes.PlateReturn:  #Put on empty Counter
                counters[c].item = p.item
                p.item = None
            elif str(counters[c].item) == 'Plate' and \
                counters[c].item.item == None and \
                counters[c].item.dirty == False: #Put on empty plate
                counters[c].item.item = p.item
                p.item = None
            
def chop(p, c, counters):
    if p.item == None:
        if type(counters[c]) == Classes.CuttingBoard and \
            type(counters[c].item) == Classes.Food:
            if counters[c].item.chop < 50:
                counters[c].item.chop += 1
            else:
                counters[c].item.chopped = True
                
def wash(p, c, counters):
    if p.item == None:
        if type(counters[c]) == Classes.Wash and counters[c].plateCount != 0:
            counters[c].wash += 1
            if counters[c].wash == 50:
                counters[c].plateCount -= 1
                counters[c-1].plateCount += 1
                counters[c].wash = 0
                
def extinguish(p, c, counters):
    if str(counters[c].item) == 'Pot' and counters[c].item.fire > 40:
        counters[c].item = Classes.Pot()
        counters[c].item.food1 = Classes.Food('fire')
        counters[c].item.food2 = Classes.Food('fire')
        counters[c].item.food3 = Classes.Food('fire')
        
        
        
def makeCounters():
    counters=[]
    #Left Top Right Bottom
    c1 = Classes.Counter(350, 380, 390, 415)
    c2 = Classes.Counter(390, 380, 440, 415)
    c3 = Classes.Counter(440, 380, 490, 415)
    c4 = Classes.Trash(490, 380, 540, 415)
    c5 = Classes.Counter(540, 380, 590, 415)
    c6 = Classes.Counter(590, 380, 640 ,415)
    c7 = Classes.Counter(640, 380, 685, 415)
    
    c8 = Classes.FoodCrate(495, 210, 530, 235, Classes.Food('onion'))
    c9 = Classes.Counter(495, 240, 532, 270)
    c10 = Classes.FoodCrate(495, 270, 535, 300, Classes.Food('carrot'))
    c11 = Classes.Counter(495, 300, 535, 340)
    c12 = Classes.FoodCrate(495, 340, 535, 380, Classes.Food('potato'))
    
    c13 = Classes.Counter(230, 465, 270, 510)
    c14 = Classes.Counter(270, 465, 335 , 510)
    c15 = Classes.WashReturn(335, 465, 385, 510)
    c16 = Classes.Wash(385, 465, 440, 510)
    c17 = Classes.Counter(440, 465, 490, 510)
    c18 = Classes.Counter(490, 465, 545, 510)
    c19 = Classes.Counter(545, 465, 600, 510)
    c20 = Classes.PlateReturn(600, 465, 645, 510)
    c21 = Classes.Serve(645, 465, 760, 510)
    c22 = Classes.Counter(760, 465, 810, 510)
    
    c23 = Classes.Counter(263, 337, 301, 376)
    c24 = Classes.Counter(270, 305, 309, 337)
    c25 = Classes.Counter(280, 265, 315, 305)
    c26 = Classes.Counter(291, 231, 323, 266)
    c27 = Classes.Counter(300, 207, 330, 230)
    
    c28 = Classes.CuttingBoard(340, 180, 375, 208)
    c29 = Classes.Counter(375, 180, 415, 208)
    c30 = Classes.CuttingBoard(415, 180, 455, 208)
    c31 = Classes.Counter(455, 180, 495, 208)
    c32 = Classes.Counter(495, 180, 540, 208)
    c33 = Classes.Counter(540, 180, 570, 208)
    c34 = Classes.Stove(570, 180, 610, 208)
    c35 = Classes.Counter(610, 180, 650, 208)
    c36 = Classes.Stove(650, 180, 690, 208)
    c37 = Classes.Counter(690, 180, 730, 208)
    
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
    
    counters[4].item = Classes.Plate()
    counters[5].item = Classes.Plate()
    counters[30].item = Classes.Extinguisher()
    counters[33].item = Classes.Pot()
    counters[35].item = Classes.Pot()
    
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
        elif s == 'None':
            image = pygame.image.load("Images/Empty.png").convert_alpha()
        elif s == 'fire':
            image = pygame.image.load("Images/CookingFire.png").convert_alpha()

    else:
        if s == 'onion soup' or s == 'stew':
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
    lst = [Classes.Dish('onion soup'), Classes.Dish('stew')]
    return(lst[random.randint(0,1)])  
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        