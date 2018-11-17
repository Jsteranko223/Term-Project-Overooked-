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

        textsurface1 = myfont.render(str('Press x to Play'), False, (0, 0, 0))
        textsurface2 = myfont.render(str('Press q to Pick Up'), False, (0, 0, 0))
        textsurface3 = myfont.render(str('Press e to Put Down'), False, (0, 0, 0))
        textsurface4 = myfont.render(str('Press r to Chop'), False, (0, 0, 0))
        textsurface5 = myfont.render(str('Press t to Wash'), False, (0, 0, 0))
        


        screen.blit(textsurface1,(400,200))
        screen.blit(textsurface2,(400,250))
        screen.blit(textsurface3,(400,300))
        screen.blit(textsurface4,(400,350))
        screen.blit(textsurface5,(400,400))

        
        clock.tick(clock_tick_rate)
        
        
        pygame.display.flip()

