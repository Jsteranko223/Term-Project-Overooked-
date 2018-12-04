import pygame

pygame.init()
pygame.font.init()


def intro():
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/SplashBackground.png")\
                 .convert_alpha()

    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_x] == 1:
                play = True
            if pressedKeys[pygame.K_l] == 1:
                leaderboard()
                
        screen.blit(background,(0,0))

        pygame.display.flip()

def leaderboard():    
    import pygame
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/GameOver.png")\
                 .convert_alpha()
    myfont = pygame.font.SysFont('Segoe UI Black', 30)

    play = False
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[pygame.K_x] == 1:
                play = True
            try:
                file = (readFile('users.txt'))
                scores = {}
                end1 = -1
                for i in range(len(file)):
                    if file[i] == ':':
                        start = i
                        for j in range(i+2, len(file)):
                            if file[j] == '\n':
                                end2 = j
                                break
                        if file[end1+1:i] in scores:
                            if int(scores[file[end1+1:i]]) < int(file[i+2:end2]):
                                scores[file[end1+1:i]] = file[i+2:end2]
                        else:
                            scores[file[end1+1:i]] = file[i+2:end2]
                        end1 = end2
                highScore = 0
                highPlayer = ''
                count = 0
                leaderPlayers = ['','','','','']
                leaderScores = [0,0,0,0,0]
                while count < 4:
                    if len(scores) == 0:
                        break
                    for user in scores:
                        if int(scores[user]) > highScore:
                            highScore = int(scores[user])
                            highPlayer = user
                    leaderPlayers[count] = highPlayer
                    leaderScores[count] = highScore
                    del scores[highPlayer]
                    count += 1
                    highScore = 0
                    highPlayer = ''
                        
                screen.blit(background,(0,0))
                textsurface = myfont.render('High Scores:', False, (0, 0, 0))
                screen.blit(textsurface,(400,150))
                for i in range(len(leaderPlayers)):
                    if leaderScores[i] != 0:
                        if i == 0:
                            textsurface0 = myfont.render('1. ' + leaderPlayers[i] + ': ' +\
                            str(leaderScores[i])
                            , False, (0, 0, 0))
                            screen.blit(textsurface0,(400,200))
                        if i == 1:
                            textsurface1 = myfont.render('2. ' + leaderPlayers[i] + ': ' +\
                            str(leaderScores[i])
                            , False, (0, 0, 0))
                            screen.blit(textsurface1,(400,250))
                        if i == 2:
                            textsurface2 = myfont.render('3. ' + leaderPlayers[i] + ': ' +\
                            str(leaderScores[i])
                            , False, (0, 0, 0))
                            screen.blit(textsurface2,(400,300))
                        if i == 3:
                            textsurface3 = myfont.render('4. ' + leaderPlayers[i] + ': ' +\
                            str(leaderScores[i])
                            , False, (0, 0, 0))
                            screen.blit(textsurface3,(400,350))
                        if i == 4:
                            textsurface4 = myfont.render('5. ' + leaderPlayers[i] + ': ' +\
                            str(leaderScores[i])
                            , False, (0, 0, 0))
                            screen.blit(textsurface4,(400,400))
            except:
                screen.blit(background,(0,0))
                textsurface = myfont.render('No Scores Found', False, (0, 0, 0))
                screen.blit(textsurface,(400,150))
            
                
        pygame.display.flip()
        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    