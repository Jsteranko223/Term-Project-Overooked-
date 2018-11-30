'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
#Sockets handleServerMsg and socket implemtation is from sockets demo
import pygame
import time
import random
import Classes
import Functions
import Intro
import PlayGame
import Rules
import GameModeSelection
import GameOver
import Character

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
            GameOver.gameover(self.player.counters[20].score)
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
                    
                elif type(self.player.item) == Classes.Extinguisher:
                    msg = 'up %s \n' %(self.player.item)
                    
                elif type(self.player.item) == Classes.Pot:
                    #Pick up pot with dish in it
                    if self.player.item.dish != None:
                        msg = 'up %s %s %s %s %s %s \n' %(self.player.item, 
                        self.player.item.dish, self.player.item.food1, 
                        self.player.item.food2, self.player.item.food3, 
                        self.player.item.fire) 
                    #Pick up pot with no dish in it
                    else:
                        msg = 'up %s %s %s %s %s %s %s \n' %(self.player.item, 
                        self.player.item.food1, self.player.item.food2, 
                        self.player.item.food3, self.player.item.cook,
                        self.player.item.cookTime, self.player.item.fire) 
                elif type(self.player.item) == Classes.Plate:
                    #Pick up empty plate
                    if self.player.item.item == None:
                        msg = 'up %s %s \n' %(self.player.item, self.player.item.dirty)
                    #Pick up plate with food on it
                    elif type(self.player.item.item) == Classes.Food:
                        msg = 'up %s %s %s %s \n' %(self.player.item, 
                        self.player.item.item.type, self.player.item.item.chopped, 
                        self.player.item.item.chop)
                    #Pick up plate with dish on it
                    elif type(self.player.item.item) == Classes.Dish:
                        msg = 'up %s %s %s %s %s \n' %(self.player.item,
                        self.player.item.item.type, self.player.item.item.food1, 
                        self.player.item.item.food2, self.player.item.item.food3)
                         
                    
            #Plate
            elif str(self.player.item) == 'Plate':
                #Put down plate with something on it
                if self.player.item.item != None:
                    #Serve food
                    if type(self.player.counters[self.player.c]) == Classes.Serve:
                        if type(self.player.item.item) == Classes.Dish:
                            Functions.putDown(self.player, self.player.c, self.player.counters)
                            msg = 'down %s serve %s \n' %(self.player.item, 
                            self.player.counters[20].score)
                    #Throw away food on plate
                    elif type(self.player.counters[self.player.c]) == Classes.Trash:
                            Functions.putDown(self.player, self.player.c, self.player.counters)
                            msg = 'down %s trash %s \n' %(self.player.item, 
                            self.player.item.dirty)
                    else:
                        Functions.putDown(self.player, self.player.c, self.player.counters)
                        
                        #put down plate with food on it
                        if type(self.player.counters[self.player.c].item.item) == Classes.Food:
                            msg = 'down %s %s %s %s \n' \
                            %(self.player.counters[self.player.c].item,
                            self.player.counters[self.player.c].item.item.type,
                            self.player.counters[self.player.c].item.item.chopped,
                            self.player.counters[self.player.c].item.item.chop)
                        #Put down plate with dish on it
                        elif type(self.player.counters[self.player.c].item.item) == Classes.Dish:
                            msg = 'down %s %s %s %s %s \n' \
                            %(self.player.counters[self.player.c].item, 
                            self.player.counters[self.player.c].item.item.type, 
                            self.player.counters[self.player.c].item.item.food1,
                            self.player.counters[self.player.c].item.item.food2,
                            self.player.counters[self.player.c].item.item.food3)
                    
                #Pick up meal from pot with plate
                elif str(self.player.counters[self.player.c].item) == 'Pot' and \
                        self.player.item.dirty == False and \
                        self.player.counters[self.player.c].item.dish != None:
                    Functions.pickUp(self.player, self.player.c, self.player.counters)
                    msg = 'up %s %s %s %s %s \n' %(self.player.item, 
                    self.player.item.item.type, self.player.item.item.food1,
                    self.player.item.item.food2, self.player.item.item.food3)
                    
                #Put down empty plate
                else:
                    #Dirty plate in wash
                    if type(self.player.counters[self.player.c]) == Classes.Wash:
                        if type(self.player.item) == Classes.Plate and self.player.item.dirty == True:
                            Functions.putDown(self.player, self.player.c, self.player.counters)
                            msg = 'down %s wash %s %s \n' \
                            %(self.player.item, self.player.counters[self.player.c].plateCount, 
                                self.player.counters[self.player.c].wash)
                    #Plate on counter
                    elif type(self.player.counters[self.player.c]) == Classes.Counter:
                        Functions.putDown(self.player, self.player.c, self.player.counters)
                        msg = 'down %s %s \n' \
                        %(self.player.counters[self.player.c].item, 
                            self.player.counters[self.player.c].item.dirty)
                    
                                        
            #Put down item
            elif self.player.item != None:
                #Throw food in trash
                if type(self.player.counters[self.player.c]) == Classes.Trash:
                        Functions.putDown(self.player, self.player.c, self.player.counters)
                        msg = 'down %s trash \n' %(self.player.item)
                else:
                    Functions.putDown(self.player, self.player.c, self.player.counters)
                    #Food on counter
                    if type(self.player.counters[self.player.c].item) == Classes.Food:
                        msg = 'down %s %s %s \n' %(self.player.counters[self.player.c].item.type, 
                        self.player.counters[self.player.c].item.chopped,
                        self.player.counters[self.player.c].item.chop)
                    #Extinguisher on counter
                    elif type(self.player.counters[self.player.c].item) == Classes.Extinguisher:
                        msg = 'down %s \n' %(self.player.counters[self.player.c].item)
                    #Food in pot
                    elif type(self.player.counters[self.player.c].item) == Classes.Pot:
                        if self.player.counters[self.player.c].item.dish != None:
                            msg = 'down %s %s %s %s %s %s \n' %(self.player.counters[self.player.c].item, 
                            self.player.counters[self.player.c].item.dish, 
                            self.player.counters[self.player.c].item.food1, 
                            self.player.counters[self.player.c].item.food2,
                            self.player.counters[self.player.c].item.food3, 
                            self.player.counters[self.player.c].item.fire) 
                        else:
                            msg = 'down %s %s %s %s %s %s %s \n' %(self.player.counters[self.player.c].item, 
                            self.player.counters[self.player.c].item.food1,
                            self.player.counters[self.player.c].item.food2, 
                            self.player.counters[self.player.c].item.food3,
                            self.player.counters[self.player.c].item.cook,
                            self.player.counters[self.player.c].item.cookTime,
                            self.player.counters[self.player.c].item.fire) 
                    elif type(self.player.counters[self.player.c].item) == Classes.Plate:
                            #Put food on plate
                            if type(self.player.counters[self.player.c].item.item) == Classes.Food:
                                msg = 'down %s %s %s %s \n' \
                                %(self.player.counters[self.player.c].item,
                                self.player.counters[self.player.c].item.item.type,
                                self.player.counters[self.player.c].item.item.chopped,
                                self.player.counters[self.player.c].item.item.chop)
                        
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
            self.player, fall = Functions.move(self.player, 'down', self.player.counters)
            msg = 'move %d %d %d %s\n' % (self.player.x, self.player.y, self.player.c,fall)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[1] == 1:
            self.player, fall = Functions.move(self.player, 'up', self.player.counters)
            msg = 'move %d %d %d %s\n' % (self.player.x, self.player.y, self.player.c,fall)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[0] == -1:
            self.player, fall = Functions.move(self.player, 'left', self.player.counters)
            msg = 'move %d %d %d %s\n' % (self.player.x, self.player.y, self.player.c,fall)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
                
        if self.player.d[0] == 1:
            self.player, fall = Functions.move(self.player, 'right', self.player.counters)
            msg = 'move %d %d %d %s\n' % (self.player.x, self.player.y, self.player.c,fall)
            if (msg != ""):
                print ("sending: ", msg,)
                self.server.send(msg.encode())
                msg = ''
            
        self.player.c = Functions.lookAtCounter(self.player, self.player.counters)
        
        if self.player.action == True:
            if type(self.player.counters[self.player.c]) == Classes.CuttingBoard:
                Functions.chop(self.player, self.player.c, self.player.counters)
                if type(self.player.counters[self.player.c].item) == Classes.Food:
                    msg = 'chop %s %s %s \n' %(self.player.counters[self.player.c].item,
                    self.player.counters[self.player.c].item.chopped, 
                    self.player.counters[self.player.c].item.chop)
                    if (msg != ""):
                        print ("sending: ", msg,)
                        self.server.send(msg.encode())
                        msg = ''
                if type(self.player.counters[self.player.c].item) == Classes.Food and \
                self.player.counters[self.player.c].item.chopped == True:
                    self.player.action = False
            elif type(self.player.counters[self.player.c]) == Classes.Wash:
                Functions.wash(self.player, self.player.c, self.player.counters)
                if self.player.counters[self.player.c].plateCount != 0:
                    msg = 'wash %s %s \n' \
                    %(self.player.counters[self.player.c].plateCount,
                      self.player.counters[self.player.c].wash)
                    if (msg != ""):
                        print ("sending: ", msg,)
                        self.server.send(msg.encode())
                        msg = ''
                
                if self.player.counters[self.player.c].plateCount == 0:
                    self.player.action = False
            elif str(self.player.item) == 'Extinguisher':
                Functions.extinguish(self.player, self.player.c, self.player.counters)

        Functions.cook(self.player.counters[35])
        Functions.cook(self.player.counters[33])
        
        if self.player.counters[20].milliseconds > 1000:
            self.player.counters[20].seconds += 1
            self.player.counters[20].milliseconds -= 1000
            for i in range(len(self.player.counters[20].recipes)):
                if self.player.counters[20].recipes[i] != None:
                    self.player.counters[20].recipeTimes[i] += 1
            if (self.player.counters[20].timer-self.player.counters[20].seconds) % 30 == 0:
                for i in range(len(self.player.counters[20].recipes)):
                    if self.player.counters[20].recipes[i] == None:
                        self.player.counters[20].recipes[i] = Functions.generateRecipes()
                        break
                        
        self.player.counters[20].milliseconds += clock.tick(clock_tick_rate)
        
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
                    
                s = "Images/"+self.character+".png"
                self.player.character = pygame.image.load(s).convert_alpha()
                    
    
            elif (command == "newPlayer"):
                newPID = msg[1]+msg[2]
                msg = ('char %s \n') %(self.character)
                if (msg != ""):
                    print ("sending: ", msg,)
                    self.server.send(msg.encode())
                    msg = ''
                    
                if newPID == 'Player1' and self.other == None:
                    self.other = Classes.Player(400,250)
                    self.other.serverPlayer = 1
                
                else:
                    self.other = Classes.Player(650,250)
                    self.other.serverPlayer = 2
                    
                    msg = ('time %d %d %d %s \n') %(self.player.counters[20].timer,
                    self.player.counters[20].seconds, 
                    self.player.counters[20].milliseconds, self.player.counters[20].recipes[0])
                    if (msg != ""):
                        print ("sending: ", msg,)
                        self.server.send(msg.encode())
                        msg = ''
                           
            elif command == 'char':
                if int(msg[0]) != self.player.serverPlayer:
                    s = "Images/"+msg[3]+".png"
                    self.other.character = pygame.image.load(s).convert_alpha()
                    
                    
            elif command =='time':
                self.player.counters[20].timer = int(msg[3])
                self.player.counters[20].seconds = int(msg[4])+1
                self.player.counters[20].milliseconds = int(msg[5])
                self.player.counters[20].recipes[0] = Classes.Dish(msg[6])
            elif self.other != None:
                if (command == "move") and self.player.serverPlayer != p:
                    dx = int(msg[3])
                    dy = int(msg[4])
                    dc = int(msg[5])
                    fall = msg[6]
                    self.other.x = dx
                    self.other.y = dy
                    self.other.p = pygame.Rect(self.other.x, self.other.y, 
                    self.other.width, self.other.height)
                    self.other.lookX = self.other.x+self.other.width//4+5
                    self.other.lookY = self.other.y+self.other.height//2+5
                    self.other.c = dc
                    if fall != 'None':
                        self.other.item = None
                        if fall == 'Plate':
                            self.player.counters[19].plateCount += 1
                        elif fall == 'Extinguisher':    
                            if str(self.player.counters[30].item) == 'Plate':
                                self.player.counters[19].plateCount += 1
                            elif str(self.player.counters[30].item) == 'Pot':
                                if self.player.counters[33].item == None:
                                    self.player.counters[33].item = Classes.Pot()
                                elif self.player.counters[35].item == None:
                                    self.player.counters[35].item = Classes.Pot()
                            self.player.counters[30].item = Classes.Extinguisher()
                        elif fall == 'Pot':
                            if self.player.counters[33].item == None:
                                self.player.counters[33].item = Classes.Pot()
                            elif self.player.counters[35].item == None:
                                self.player.counters[35].item = Classes.Pot()
                        
        
                elif (command == "up") and self.player.serverPlayer != p :
                    self.player.counters[self.other.c].item = None
                    kind = msg[3]
                    if kind == 'onion' or kind == 'potato' or kind == 'carrot':
                        chopped = msg[4]
                        if chopped == 'False':
                            chopped = False
                        else:
                            chopped = True
                        chop = int(msg[5])
                        self.other.item = Classes.Food(kind)
                        self.other.item.chopped = chopped
                        self.other.item.chop = chop
                    elif kind == ('Extinguisher'):
                        self.other.item = Classes.Extinguisher()
                    elif kind == ('Pot'):
                        if len(msg) == 10: #No dish
                            f1 = msg[4]
                            f2 = msg[5]
                            f3 = msg[6]
                            cook = msg[7]
                            cookTime = msg[8]
                            fire = msg[9]
                            self.other.item = Classes.Pot()
                            if f1 != 'None':
                                self.other.item.food1 = Classes.Food(f1)
                                if f2 != 'None':
                                    self.other.item.food2 = Classes.Food(f2)
                                    if f3 != 'None':
                                        self.other.item.food3 = Classes.Food(f3)
                            self.other.item.cook = int(cook)
                            self.other.item.cookTime = int(cookTime)
                            self.other.item.fire = int(fire)
                        else: #Dish in Pot
                            d = msg[4]
                            f1 = msg[5]
                            f2 = msg[6]
                            f3 = msg[7]
                            fire = msg[8]
                            self.other.item = Classes.Pot()
                            self.other.dish = Classes.Dish(d)
                            self.other.item.food1 = Classes.Food(f1)
                            self.other.item.food2 = Classes.Food(f2)
                            self.other.item.food3 = Classes.Food(f3)
                            self.other.item.dish.food1 = Classes.Food(f1)
                            self.other.item.dish.food2 = Classes.Food(f2)
                            self.other.item.dish.food3 = Classes.Food(f3)
                            self.other.item.fire = int(fire)
                    elif kind == 'Plate':
                        print(msg)
                        #Pick up empty plate
                        if msg[4] == 'True' or msg[4] == 'False':
                            dirty = msg[4]
                            self.other.item = Classes.Plate()
                            if dirty == 'True':
                                self.other.item.dirty = True
                            if type(self.player.counters[self.other.c]) == Classes.WashReturn:
                                self.player.counters[self.other.c].plateCount -= 1
                        #Pick up plate with food on it
                        elif msg[4] == 'onion' or msg[4] == 'potato' or msg[4] == 'carrot':
                            chopped = msg[5]
                            if chopped == 'False':
                                chopped = False
                            else:
                                chopped = True
                            chop = int(msg[6])
                            self.other.item = Classes.Plate()
                            self.other.item.item = Classes.Food(msg[4])
                            self.other.item.item.chopped = chopped
                            self.other.item.item.chop = chop
                        #Dish from pot with plate
                        else:
                            d = msg[4]
                            f1 = msg[5]
                            f2 = msg[6]
                            f3 = msg[7]
                            self.player.counters[self.other.c].item = Classes.Pot()
                            self.other.item = Classes.Plate()
                            self.other.item.item = Classes.Dish(d)
                            if f1 != 'None':
                                self.other.item.item.food1 = Classes.Food(f1)
                                if f2 != 'None':
                                    self.other.item.item.food2 = Classes.Food(f2)
                                    if f3 != 'None':
                                        self.other.item.item.food3 = Classes.Food(f3)
                            
                elif (command == "down") and self.player.serverPlayer != p :
                    print(msg)
                    kind = msg[3]
                    if kind == 'onion' or kind == 'potato' or kind == 'carrot':
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
                    elif kind == ('Extinguisher'):
                        self.player.counters[self.other.c].item = Classes.Extinguisher()
                        self.other.item = None
                    elif kind == ('Pot'):
                        if msg[4] == 'trash':
                            self.other.item = Classes.Pot()
                        elif len(msg) == 10: #No dish
                            f1 = msg[4]
                            f2 = msg[5]
                            f3 = msg[6]
                            cook = msg[7]
                            cookTime = msg[8]
                            fire = msg[9]
                            self.other.item = None
                            self.player.counters[self.other.c].item = Classes.Pot()
                            if f1 != 'None':
                                self.player.counters[self.other.c].item.food1 = Classes.Food(f1)
                                if f2 != 'None':
                                    self.player.counters[self.other.c].item.food2 = Classes.Food(f2)
                                    if f3 != 'None':
                                        self.player.counters[self.other.c].item.food3 = Classes.Food(f3)
                            self.player.counters[self.other.c].item.cook = int(cook)
                            self.player.counters[self.other.c].item.cookTime = int(cookTime)
                            self.player.counters[self.other.c].item.fire = int(fire)
                            self.other.item = None
                        else: #Dish in Pot
                            d = msg[4]
                            f1 = msg[5]
                            f2 = msg[6]
                            f3 = msg[7]
                            fire = msg[8]
                            self.player.counters[self.other.c].item = Classes.Pot()
                            self.player.counters[self.other.c].dish = Classes.Dish(d)
                            self.player.counters[self.other.c].item.food1 = Classes.Food(f1)
                            self.player.counters[self.other.c].item.food2 = Classes.Food(f2)
                            self.player.counters[self.other.c].item.food3 = Classes.Food(f3)
                            self.player.counters[self.other.c].item.dish.food1 = Classes.Food(f1)
                            self.player.counters[self.other.c].item.dish.food2 = Classes.Food(f2)
                            self.player.counters[self.other.c].item.dish.food3 = Classes.Food(f3)
                            self.player.counters[self.other.c].item.fire = int(fire)
                            self.other.item = None
                    elif kind == 'Plate':
                        if msg[4] == 'trash':
                            dirty = msg[4]
                            self.other.item = Classes.Plate()
                            if dirty == 'True':
                                self.other.item.dirty = True
                        else:
                            self.other.item = None
                            if msg[4] == 'True' or msg[4] == 'False':
                                dirty = msg[4]
                                self.player.counters[self.other.c].item = Classes.Plate()
                                if dirty == 'True':
                                    self.player.counters[self.other.c].item.dirty = True
                            elif msg[4] == 'onion' or msg[4] == 'potato' or msg[4] == 'carrot':
                                chopped = msg[5]
                                if chopped == 'False':
                                    chopped = False
                                else:
                                    chopped = True
                                chop = int(msg[6])
                                self.player.counters[self.other.c].item = Classes.Plate()
                                self.player.counters[self.other.c].item.item = Classes.Food(msg[4])
                                self.player.counters[self.other.c].item.item.chopped = chopped
                                self.player.counters[self.other.c].item.item.chop = chop
                            else:
                                d = msg[4]
                                f1 = msg[5]
                                f2 = msg[6]
                                f3 = msg[7]
                                self.player.counters[self.other.c].item = Classes.Plate()
                                self.player.counters[self.other.c].item.item = Classes.Dish(d)
                                if f1 != 'None':
                                    self.player.counters[self.other.c].item.item.food1 = Classes.Food(f1)
                                    if f2 != 'None':
                                        self.player.counters[self.other.c].item.item.food2 = Classes.Food(f2)
                                        if f3 != 'None':
                                            self.player.counters[self.other.c].\
                                            item.item.food3 = Classes.Food(f3)
                    elif kind == 'None':
                        if msg[4] == 'trash':
                            self.other.item = None
                        if msg[4] == 'serve':
                            self.other.item = None
                            score = msg[5]
                            self.player.counters[20].score = score
                            self.player.counters[19].plateCount += 1  
                        elif msg[4] == 'wash':
                            self.other.item = None
                            count = int(msg[5])
                            wash = int(msg[6])
                            self.player.counters[15].plateCount = count
                            self.player.counters[15].wash = wash
                elif (command == "chop") and self.player.serverPlayer != p:
                    chopped = msg[4]
                    if chopped == 'False':
                        chopped = False
                    else:
                        chopped = True
                    chop = int(msg[5])
                    self.player.counters[self.other.c].item.chopped = chopped
                    self.player.counters[self.other.c].item.chop = chop
                elif command == 'wash' and self.player.serverPlayer != p:
                    count = int(msg[3])
                    wash = int(msg[4])+1
                    self.player.counters[15].plateCount = count
                    self.player.counters[15].wash = wash
                    if self.player.counters[15].wash == 50:
                        self.player.counters[15].plateCount -= 1
                        self.player.counters[14].plateCount += 1
                        self.player.counters[15].wash = 0
                    

            serverMsg.task_done()
                
    def redrawAll(self, screen):
        screen.blit(self.backgroundImage, (0,0))
        screen.blit(self.player.character, (self.player.x-25, self.player.y-25))
        if self.other != None:
            if self.other.character != None:
                screen.blit(self.other.character, (self.other.x-25, self.other.y-25))
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
                                drawFood(screen, counter.left-player.width//4, 
                                counter.top-player.height, 
                                counter.item.item.food1, True)
                                drawFood(screen, counter.left+2*player.width//3, 
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

        textsurface1 = self.myfont.render(str(self.player.counters[20].timer-self.player.counters[20].seconds), False, (0, 0, 0))
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
       

        self.server = server
        self.serverMsg = serverMsg
        self.other = None
        
    def run(self):
        Intro.intro()
        players = GameModeSelection.gameModeSelection()
        if players == 1:
            character = Character.character()
            Rules.rules()
            score = PlayGame.playGame(1, character)
            GameOver.gameover(score)
        else:
            self.character = Character.character()
            Rules.rules()
            self.player = Classes.Player(400,250)
            
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode((1000,600))
            # set the title of the window
            pygame.display.set_caption(self.title)
            # stores all the keys currently being held down
            self._keys = dict()
            s = "Images/"+self.character+".png"
            self.player.character = pygame.image.load(s).convert_alpha()
            

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










