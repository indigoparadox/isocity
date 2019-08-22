#!/usr/bin/env python

import pygame
import random
import logging

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BUILDING_W_PX = 32
BUILDING_H_PX = 64

X = 0
Y = 1

BUILDING_RESIDENTIAL_LOW = 1
BUILDING_RESIDENTIAL_HIGH = 2
BUILDING_COMMERCIAL_LOW = 3
BUILDING_COMMERCIAL_HIGH =4

BUILDING_GFX = [
   ['house 2.png', 'house 1.png'],
   ['building 10.png', 'building 9.png', 'building 8.png'],
   ['cafe.png', 'restaurant.png', 'shop.png'],
   ['building 7.png', 'building 6.png', 'building 5.png', 'building 4.png']
]

class WorldMap:

   def __init__( self, size ):

      self.size = size

      self.tiles = []
      for x in range( 0, self.size ):
         row = []
         for y in range( 0, self.size ):
            row.append( None )
         self.tiles.append( row )

class City:

   buildings = []
   build_range = 0

   def __init__( self, world_map, treasury=0 ):
      self.treasury = treasury
      self.world_map = world_map

   def add_building( self, building ):
      building.city = self
      self.buildings.append( building )

class Building:

   def __init__( self, city, zone, tax_income, pos=(0, 0) ):

      assert( None == city.world_map.tiles[pos[Y]][pos[X]] )

      self.logger = logging.getLogger( 'building' )

      city.world_map.tiles[pos[Y]][pos[X]] = self
      
      self.city = city
      self.zone = zone
      self.tax_income = tax_income
      self.pos = pos

      icon_path = 'isocity/{}'.format( random.choice( BUILDING_GFX[zone] ) )
      self.logger.debug( 'creating building from: {}'.format( icon_path ) )
      icon_s1 = pygame.image.load( icon_path ).convert_alpha()
      icon_height = \
         BUILDING_W_PX * icon_s1.get_height() / icon_s1.get_width()
      self.logger.debug( 'building image height: {}'.format( icon_height ) )

      icon_s2 = pygame.transform.scale( icon_s1, \
         (BUILDING_W_PX, icon_height) )

      self.icon = pygame.Surface( (BUILDING_W_PX, BUILDING_H_PX) )
      self.icon.fill( (255, 0, 255) )
      self.icon.blit( \
         icon_s2, (0, self.icon.get_height() - icon_s2.get_height()) )
      self.icon.set_colorkey( (255, 0, 255) )

def main():

   logging.basicConfig( level=logging.DEBUG )
   logger = logging.getLogger( 'main' )

   tax_timer_max = 100
   world_map_sz = 5
   
   pygame.init()
   screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
   running = True
   clock = pygame.time.Clock()

   # Create an empty new world map.
   tax_timer = 0
   tax_total = 0

   logger.debug( 'creating city...' )
   world_map = WorldMap( world_map_sz )
   city = City( world_map )
   for i in range( 0, 3 ):
      city.add_building( Building( city, BUILDING_RESIDENTIAL_LOW, 100, \
         pos=(world_map_sz / 2, world_map_sz / 2 + i) ) )

   vx = SCREEN_WIDTH / 2
   vy = SCREEN_HEIGHT / 3
   
   while running:

      # Get input state to apply below.
      for event in pygame.event.get():
         if pygame.QUIT == event.type:
            running = False
         elif pygame.KEYDOWN == event.type:
            if pygame.K_ESCAPE == event.key:
               running = False
            elif pygame.K_RIGHT == event.key:
               vx -= 10
            elif pygame.K_LEFT == event.key:
               vx += 10
            elif pygame.K_UP == event.key:
               vy += 10
            elif pygame.K_DOWN == event.key:
               vy -= 10
            elif pygame.K_SPACE == event.key:
               pass
         elif pygame.KEYUP == event.type:
            pass

      tax_timer += 1
      if tax_timer > tax_timer_max:
         # Collect taxes and build a new building if we have enough.
         city.treasury += tax_total
         tax_timer = 0
         logger.info( 'tax collected; now: {}'.format( city.treasury ) )

      screen.fill( (0, 0, 0) )

      for row in world_map.tiles:
         for tile in row:
            if tile and tile.icon:
               x = tile.pos[X]
               y = tile.pos[Y]

               # These offsets make some assumptions about tile dimensions and
               # layout.
               screen_x = int( (((x - y) * BUILDING_W_PX / 2) + vx ) )
               screen_y = int( ((x + y) * BUILDING_H_PX / 5) + vy )

               screen.blit( tile.icon, (screen_x, screen_y) )
               pygame.draw.rect( screen, (255, 0, 0),
                  [screen_x, screen_y, BUILDING_W_PX, BUILDING_H_PX], 1 )
                  

      pygame.display.flip()

      clock.tick( 60 )

if '__main__' == __name__:
   main()

