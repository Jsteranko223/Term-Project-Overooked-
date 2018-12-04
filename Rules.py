import pygame

pygame.init()

def rules(players):
    screen = pygame.display.set_mode((1000,600))
    if players == 1:
        background = pygame.image.load("Images/RulesBackground.png")\
                    .convert_alpha()
    else:
        background = pygame.image.load("Images/Rules2Background.png")\
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