import pygame

pygame.init()

def rules():
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
    background = pygame.image.load("Images/RulesBackground.png")\
                 .convert_alpha()


    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_x] == 1:
                play = True
                
        screen.blit(background,(0,0))
        pygame.display.flip()