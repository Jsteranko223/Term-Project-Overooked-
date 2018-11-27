import pygame
import time
import random
import Functions

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
        
    def cook(self, screen):
        if str(self.item) == 'Pot':
            if self.item.food1 != None and str(self.item.food1) != 'fire' and \
               self.item.fire <= 40:
                if self.item.cook > 0:
                    self.item.cook -= 1
                progress = 50*(1 - (self.item.cook/self.item.cookTime))
                r = pygame.Rect(self.left-5, self.top-10, progress, 10)
                pygame.draw.rect(screen, (0,255,0), r)
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
            
class Trash(Counter):
    pass

class Serve(Counter):
    def __init__(self, left, top, right, bottom):
        super().__init__(left, top, right, bottom)
        self.recipes = [Functions.generateRecipes(), None, None, None]
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
        self.width = 15
        self.height = 15
        self.speed = 10
        self.p = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lookX = self.x+self.width//4
        self.lookY = self.y+self.height//2 
        self.direction = 'down'
        self.item = None
        self.action = False
        self.c = -1
        self.d = [0,0]
        
        
        
        
        
        
        