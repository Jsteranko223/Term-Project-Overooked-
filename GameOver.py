import pygame
pygame.init()
pygame.font.init()


def gameover(scores, name):
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/GameOver.png")\
                 .convert_alpha()
    myfont = pygame.font.SysFont('Segoe UI Black', 30)
    play = False
    start = False
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[pygame.K_x] == 1:
                play = True
                start = True
                
                
        screen.blit(background,(0,0))
        textsurface1 = myfont.render('Game Over', False, (0, 0, 0))
        screen.blit(textsurface1,(400,250))
        textsurface2 = myfont.render('Score: ' + str(scores), False, (0, 0, 0))
        screen.blit(textsurface2,(425,300))

        pygame.display.flip()
    writeUserName(scores, name)
    if start == True:
        return True
    else:
        pygame.quit()
    

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
def writeUserName(score, name):
    text = ('%s: %d \n') %(name, score)
    with open("users.txt", "a") as myfile:
        myfile.write(text)
        myfile.close()

    pygame.quit()
    
