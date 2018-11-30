import pygame

pygame.init()

def gameModeSelection():
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/ModeBackground.png")\
                 .convert_alpha()

    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_1] == 1:
                return(1)
            elif pressedKeys[pygame.K_2] == 1:
                return(2)
                
        screen.blit(background,(0,0))
        pygame.display.flip()