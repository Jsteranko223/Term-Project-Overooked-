import pygame

pygame.init()

def character():
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/BackgroundCharacter.png")\
                 .convert_alpha()

    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_x] == 1:
                play = True
            if pressedKeys[pygame.K_1] == 1:
                return('Snowman')
            if pressedKeys[pygame.K_2] == 1:
                return('Penguin')
            if pressedKeys[pygame.K_3] == 1:
                return('Alien')
            if pressedKeys[pygame.K_4] == 1:
                return('Yeti')
                
        screen.blit(background,(0,0))

        pygame.display.flip()
        