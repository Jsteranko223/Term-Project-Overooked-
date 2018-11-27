import pygame

pygame.init()

def gameover(scores):
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
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
                
        screen.blit(background,(0,0))
        textsurface1 = myfont.render('Game Over', False, (0, 0, 0))
        screen.blit(textsurface1,(400,250))
        textsurface2 = myfont.render('Score: ' + str(scores), False, (0, 0, 0))
        screen.blit(textsurface2,(420,300))
        pygame.display.flip()
        
    pygame.quit()