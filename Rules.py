import pygame

pygame.init()
pygame.font.init()

def rules():
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
    rulesFont = pygame.font.SysFont('Comic Sans MS', 30)
    titleFont = pygame.font.SysFont('Comic Sans MS', 45)
    background = pygame.image.load("Images/RulesBackground.png").convert_alpha()


    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_x] == 1:
                play = True
                
        screen.blit(background,(0,0))
        
        textsurface0 = titleFont.render(str('How to Play'), False, (0, 0, 0))
        textsurface1 = rulesFont.render(str('Press x to Play'), False, (0, 0, 0))
        textsurface2 = rulesFont.render(str('Press q to Pick Up'), False, (0, 0, 0))
        textsurface3 = rulesFont.render(str('Press e to Put Down'), False, (0, 0, 0))
        textsurface4 = rulesFont.render(str('Press r to Chop'), False, (0, 0, 0))
        textsurface5 = rulesFont.render(str('Press t to Wash'), False, (0, 0, 0))
        screen.blit(textsurface0, (375, 140))
        screen.blit(textsurface1,(375,200))
        screen.blit(textsurface2,(375,250))
        screen.blit(textsurface3,(375,300))
        screen.blit(textsurface4,(375,350))
        screen.blit(textsurface5,(375,400))
                
        pygame.display.flip()