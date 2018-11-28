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

import socket
import threading
from queue import Queue


HOST = "localhost" # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")
      
class PygameGame(object):

    def keyPressed(self, keyCode, modifier):
        msg = ''
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
                Functions.pickUp(self.player,self.player.c, self.player.counters)
                if type(self.player.item) == Classes.Food:
                    msg = 'up %s %s %s \n' %(self.player.item.type, 
                    self.player.item.chopped, self.player.item.chop)
            #Plate
            elif str(self.player.item) == 'Plate':
                if self.player.item.item != None:
                    Functions.putDown(self.player, self.player.c, self.player.counters)
                elif str(self.player.counters[self.player.c].item) == 'Pot' and \
                        self.player.item.dirty == False and \
                        self.player.counters[self.player.c].item.dish != None:
                    Functions.pickUp(self.player, self.player.c, self.player.counters)
                else:
                    Functions.putDown(self.player, self.player.c, self.player.counters)
            #Put down item
            elif self.player.item != None:
                Functions.putDown(self.player, self.player.c, self.player.counters)
                if type(self.player.counters[self.player.c].item) == Classes.Food:
                    msg = 'down %s %s %s \n' %(self.player.counters[self.player.c].item.type, 
                    self.player.counters[self.player.c].item.chopped, self.player.counters[self.player.c].item.chop)
        if (msg != ""):
            print ("sending: ", msg,)
            self.server.send(msg.encode())
            msg = ''       

    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_s or keyCode == pygame.K_w:
            self.player.d[1] = 0
        if keyCode == pygame.K_a or keyCode == pygame.K_d:
            self.player.d[0] = 0


    def timerFired(self, dt):
        msg = ''
        clock = pygame.time.Clock()
        clock_tick_rate= 20

        if self.player.d[1] == -1:
            self.player = Functions.move(self.player, 'down', self.player.counters)
            msg = 'move %d %d %d \n' % (self.player.x, self.player.y, self.player.c)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[1] == 1:
            self.player = Functions.move(self.player, 'up', self.player.counters)
            msg = 'move %d %d %d \n' % (self.player.x, self.player.y, self.player.c)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[0] == -1:
            self.player = Functions.move(self.player, 'left', self.player.counters)
            msg = 'move %d %d %d \n' % (self.player.x, self.player.y, self.player.c)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[0] == 1:
            self.player = Functions.move(self.player, 'right', self.player.counters)
            msg = 'move %d %d %d \n' % (self.player.x, self.player.y, self.player.c)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
            
        self.player.c = Functions.lookAtCounter(self.player, self.player.counters)
        
        if self.player.action == True:
            if type(self.player.counters[self.player.c]) == Classes.CuttingBoard:
                Functions.chop(self.player, self.player.c, self.player.counters)
                if type(self.player.counters[self.player.c].item) == Classes.Food and \
                self.player.counters[self.player.c].item.chopped == True:
                    self.player.action = False
            elif type(self.player.counters[self.player.c]) == Classes.Wash:
                Functions.wash(self.player, self.player.c, self.player.counters)
                if self.player.counters[self.player.c].plateCount == 0:
                    self.player.action = False
            elif str(self.player.item) == 'Extinguisher':
                Functions.extinguish(self.player, self.player.c, self.player.counters)

        Functions.cook(self.player.counters[35])
        Functions.cook(self.player.counters[33])
        
        if self.milliseconds > 1000:
            self.seconds += 1
            self.milliseconds -= 1000
            for i in range(len(self.player.counters[20].recipes)):
                if self.player.counters[20].recipes[i] != None:
                    self.player.counters[20].recipeTimes[i] += 1
            if (self.timer-self.seconds) % 30 == 0:
                for i in range(len(self.player.counters[20].recipes)):
                    if self.player.counters[20].recipes[i] == None:
                        self.player.counters[20].recipes[i] = Functions.generateRecipes()
                        break
                        
        self.milliseconds += clock.tick(clock_tick_rate)
        
        while (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]
            
            if command == '1' or command == '2':
                p = int(msg[0])
                command = msg[2]
                
            if (command == "myIDis"):
                myPID = msg[1]+msg[2]
                if myPID == 'Player1':
                    self.player = Classes.Player(400,250)
                    self.player.serverPlayer = 1
                else:
                    self.player = Classes.Player(650,250)
                    self.player.serverPlayer = 2
    
            elif (command == "newPlayer"):
                newPID = msg[1]+msg[2]
                if newPID == 'Player1' and self.other == None:
                    self.other = Classes.Player(400,250)
                    self.other.serverPlayer = 1
                else:
                    self.other = Classes.Player(650,250)
                    self.other.serverPlayer = 2
            elif self.other != None:
                if (command == "move") and self.player.serverPlayer != p:
                    dx = int(msg[3])
                    dy = int(msg[4])
                    dc = int(msg[5])
                    self.other.x = dx
                    self.other.y = dy
                    self.other.p = pygame.Rect(self.other.x, self.other.y, 
                    self.other.width, self.other.height)
                    self.other.lookX = self.other.x+self.other.width//4
                    self.other.lookY = self.other.y+self.other.height//2 
                    self.other.c = dc
        
                elif (command == "up") and self.player.serverPlayer != p :
                    self.player.counters[self.other.c].item = None
                    kind = msg[3]
                    if kind == ('onion' or 'potato' or 'carrot'):
                        chopped = msg[4]
                        if chopped == 'False':
                            chopped = False
                        else:
                            chopped = True
                        chop = int(msg[5])
                        self.other.item = Classes.Food(kind)
                        self.other.item.chopped = chopped
                        self.other.item.chop = chop
                        
                elif (command == "down") and self.player.serverPlayer != p :
                    print(msg)
                    kind = msg[3]
                    if kind == ('onion' or 'potato' or 'carrot'):
                        chopped = msg[4]
                        if chopped == 'False':
                            chopped = False
                        else:
                            chopped = True
                        chop = int(msg[5])
                        f = Classes.Food(kind)
                        f.chopped = chopped
                        f.chop = chop
                        self.player.counters[self.other.c].item = f
                        self.other.item = None
                        
            serverMsg.task_done()
                
    def redrawAll(self, screen):
        screen.blit(self.backgroundImage, (0,0))
        pygame.draw.rect(screen, (0,0,255), self.player.p)
        if self.other != None:
            pygame.draw.rect(screen, (0,255, 0), self.other.p)
            Functions.drawPlayer(self.other, screen, self.player.counters)
        Functions.drawPlayer(self.player, screen, self.player.counters)
            
        for counter in self.player.counters:
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
                    
        textsurface = self.myfont.render(str(self.player.counters[20].score), False, (0, 0, 0))
        screen.blit(textsurface,(40,500))

        textsurface1 = self.myfont.render(str(self.timer-self.seconds), False, (0, 0, 0))
        screen.blit(textsurface1,(900,490))


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, serverMsg, server, width=1000, height=600, fps=40, title="Overcooked"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.myfont = pygame.font.SysFont('Segoe UI Black', 30)
        screen = pygame.display.set_mode((1000,600))
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
        
        self.server = server
        self.serverMsg = serverMsg
        self.other = None
        
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1000,600))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
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

serverMsg = Queue(1000)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

game = PygameGame(serverMsg, server)
game.run()








