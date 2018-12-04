
def username():
    import pygame 
    
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1000,600))
    background = pygame.image.load("Images/GameOver.png")\
                 .convert_alpha()
    myfont = pygame.font.SysFont('Segoe UI Black', 30)
    play = False
    name = ''
    while(play==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = True
                
            pressedKeys = pygame.key.get_pressed()

            for i in range(len(pressedKeys)):
                if pressedKeys[i] == 1 and len(name) < 10:
                    if 64 < i-32 and i-32 < 91:
                        name += chr(i-32)
                    elif 47 < i and i < 58:
                        name += chr(i)
            if pressedKeys[pygame.K_BACKSPACE] == 1:
                name = name[:-1]
            if pressedKeys[pygame.K_RETURN] == 1 and len(name) > 0:
                return(name)
                
        screen.blit(background,(0,0))
        textsurface1 = myfont.render('Enter Username: ', False, (0, 0, 0))
        screen.blit(textsurface1,(400,200))
        textsurface2 = myfont.render(name, False, (0, 0, 0))
        screen.blit(textsurface2,(415,250))
        textsurface3 = myfont.render('Press Enter To Submit Name', False, (0, 0, 0))
        screen.blit(textsurface3,(330,300))
 
        pygame.display.flip()
        
    pygame.quit()

    

















