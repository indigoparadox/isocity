#!/usr/bin/env python

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main():
   
   pygame.init()
   screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
   running = True
   clock = pygame.time.Clock()
   
   while running:

      # Get input state to apply below.
      for event in pygame.event.get():
         if pygame.QUIT == event.type:
            running = False
         elif pygame.KEYDOWN == event.type:
            if pygame.K_ESCAPE == event.key:
               running = False
            elif pygame.K_RIGHT == event.key:
               pass
            elif pygame.K_LEFT == event.key:
               pass
            elif pygame.K_SPACE == event.key:
               pass
         elif pygame.KEYUP == event.type:
            pass

      pygame.display.flip()

      clock.tick( 60 )

if '__main__' == __name__:
   main()

