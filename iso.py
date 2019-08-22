#!/usr/bin/env python

import pygame
import random

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

      city.world_map.tiles[pos[Y]][pos[X]] = self
      
      self.city = city
      self.zone = zone
      self.tax_income = tax_income
      self.pos = pos

      icon_s1 = pygame.image.load( 'isocity/{}'.format( \
         BUILDING_GFX[zone][random.randint( \
         0, len( BUILDING_GFX[zone] ) - 1 )] ) ).convert_alpha()
      icon_height = \
         BUILDING_W_PX * icon_s1.get_height() / icon_s1.get_width()

      icon_s2 = pygame.transform.scale( icon_s1, \
         (BUILDING_W_PX, icon_height) )

      self.icon = pygame.Surface( (BUILDING_W_PX, BUILDING_H_PX) )
      self.icon.fill( (255, 0, 255) )
      self.icon.blit( \
         icon_s2, (0, self.icon.get_height() - icon_s2.get_height()) )
      self.icon.set_colorkey( (255, 0, 255) )

def main():

   tax_timer_max = 100
   world_map_sz = 5
   
   pygame.init()
   screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
   running = True
   clock = pygame.time.Clock()

   # Create an empty new world map.
   tax_timer = 0
   tax_total = 0

   world_map = WorldMap( world_map_sz )
   city = City( world_map )
   city.add_building( Building( city, BUILDING_RESIDENTIAL_LOW, 100, \
      pos=(world_map_sz / 2, world_map_sz / 2) ) )
   city.add_building( Building( city, BUILDING_RESIDENTIAL_LOW, 100, \
      pos=(world_map_sz / 2, world_map_sz / 2 + 1) ) )
   city.add_building( Building( city, BUILDING_RESIDENTIAL_LOW, 100, \
      pos=(world_map_sz / 2, world_map_sz / 2 + 2) ) )
   city.add_building( Building( city, BUILDING_RESIDENTIAL_LOW, 100, \
      pos=(world_map_sz / 2 + 1, world_map_sz / 2) ) )

   #vx = SCREEN_WIDTH / 2
   #vy = -1 * (SCREEN_HEIGHT / 2)
   vx = 0
   vy = 0
   
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

      screen.fill( (0, 0, 0) )

      for row in world_map.tiles:
         for tile in row:
            if tile and tile.icon:
               x = tile.pos[X]
               y = tile.pos[Y]
               screen.blit( tile.icon, \
                  (((x - y) * BUILDING_W_PX / 2) + vx, \
                  ((x + y) * BUILDING_H_PX / 2) + vy) )

      pygame.display.flip()

      clock.tick( 60 )

if '__main__' == __name__:
   main()

