'''
Raycast client test
Created on 2010-10-08
@author: Artsimboldo
'''

import raycast
import pygame
from pygame.locals import *
from itertools import product

__DEBUG__ = True
__maxFPS__ = 100
__nodeSize__ = 32

#-----------------------------------------------------------------------------
class View():
    '''
    classdocs
    '''
    colorBackground = 50, 50, 50
    colorGround = 100, 100, 100
    colorWall = 0, 0, 0
    colorOrigin = 200, 50, 50

    colorBlack = 0, 0, 0
    colorRed = 250,0,0
    colorGreen = 0,250,0
    colorBlue = 0,0,250
    
    colorLUT = {0:colorGround, 1:colorWall}
    
    map = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
           [0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    #----------------------------------------------------------------------
    def __init__(self, title):
        '''
        Constructor
        '''
        # init view
        pygame.init()
        pygame.display.set_caption(title)
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.screenSize = self.width * __nodeSize__, self.height * __nodeSize__
        self.screen = pygame.display.set_mode(self.screenSize)
        self.origin = self.width / 2 - 1, self.height / 2 - 1

        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.colorBackground)
        
        self.ray = []
        
    #----------------------------------------------------------------------
    # put game update code here
    def update(self):
        if self.mouseButtonLeft:
            mouse = self.mousePosition[0] / __nodeSize__, self.mousePosition[1] / __nodeSize__
            self.ray = raycast.rayCast2(self.origin, mouse)

    #----------------------------------------------------------------------
    # put drawing code here
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for j in range(self.height):
            for i in range(self.width):
                if raycast.isVisible2(self.origin, (i,j), self.map):
                    pygame.draw.rect(self.screen, self.colorLUT[self.map[i][j]], (i * __nodeSize__, j * __nodeSize__, __nodeSize__ - 1, __nodeSize__ - 1))

        pygame.draw.rect(self.screen, self.colorOrigin, (self.origin[0] * __nodeSize__, self.origin[1] * __nodeSize__, __nodeSize__ - 1, __nodeSize__ - 1))
        
        x1, y1 = None, None
        offset = __nodeSize__ >> 1
        for (i,j) in self.ray:
            x2, y2 = i * __nodeSize__, j * __nodeSize__
            x2 += offset
            y2 += offset
            if (x1 and y1):
                pygame.draw.line(self.screen, self.colorRed, (x1,y1), (x2,y2), 4)
            x1, y1 = x2, y2
                       
        pygame.display.flip()

    #----------------------------------------------------------------------
    # the main game loop
    def mainLoop(self):
        pygame.mouse.set_visible(True)
        clock = pygame.time.Clock()
        oldfps = 0
        exit = False
        while not exit:
            # calculate framerate
            clock.tick(__maxFPS__)
            newfps = int(clock.get_fps())
            if newfps is not oldfps:
                print "fps = ", clock.get_fps()
                oldfps = newfps
                
            # handle events
            self.mouseButtonLeft, self.mouseButtonRight = False, False
            self.mousePosition = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit = True
                    
                elif event.type == KEYDOWN and event.key is K_ESCAPE:
                    exit = True
                
                elif event.type == MOUSEBUTTONDOWN and event.button is 1:
                    self.mouseButtonLeft = True

                elif event.type == MOUSEBUTTONDOWN and event.button is 2:
                    self.mouseButtonRight = True
                    
            # update 
            self.update()
            
            # display
            self.draw()

        pygame.quit()

if __name__ == '__main__':
    view = View("test raycast")
    view.mainLoop()
