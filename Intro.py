import pygame

pygame.init()
pygame.font.init()


def intro():
    animation_increment=10
    clock_tick_rate= 20
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000,600), pygame.FULLSCREEN)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    play = False
    
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            if pressedKeys[pygame.K_x] == 1:
                play = True
                
        screen.fill((255,255,255))

        textsurface = myfont.render(str('Splash Screen'), False, (0, 0, 0))
        screen.blit(textsurface,(500,500))
        
        clock.tick(clock_tick_rate)
        
        
        pygame.display.flip()

