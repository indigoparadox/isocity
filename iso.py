#!/usr/bin/env python

import pygame
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

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

class WorldMapLine:
   items = []

   def __init__( self, world_map ):
      self.world_map = world_map

   def __getitem__( self, key ):
      return self.items[key + (self.world_map.size / 2)]

   def __setitem__( self, key, item ):
      self.items[key + (self.world_map.size / 2)] = item

   def append( self, item ):
      self.items.append( item )

class WorldMap:

   def __init__( self, size ):

      self.size = size

      self.tiles = WorldMapLine( self )
      for x in range( 0, self.size ):
         row = WorldMapLine( self )
         for y in range( 0, self.size ):
            row.append( None )
         assert( None != row )
         self.tiles.append( item=row )

   def __getitem__( self, key ):
      return self.tiles[key]

class City:

   buildings = []
   build_range = 0

   def __init__( self, world_map, treasury=0, pos=(0, 0) ):
      self.treasury = treasury
      self.pos = pos
      self.world_map = world_map

   #def get_building( self, x, y ):
   #   for b in self.buildings:
   #      if b.pos[X] == x and b.pos[Y] == y:
   #         return b
   #   return None

   def __getitem__( self, key ):
      bldg = self.world_map[key]
      if bldg and bldg.city == self:
         return bldg
      return None

   def add_building( self, building ):
      building.city = self
      self.buildings.append( building )

class Building:

   def __init__( self, zone, tax_income, pos=(0, 0) ):

      self.zone = zone
      self.tax_income = tax_income
      self.pos = pos
      self.icon = pygame.image.load( 'isocity/{}'.format( \
         BUILDING_GFX[zone][random.randint( \
         0, len( BUILDING_GFX[zone] ) - 1 )] ) )

def main():

   tax_timer_max = 100
   world_map_sz = 20
   
   pygame.init()
   screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
   running = True
   clock = pygame.time.Clock()

   # Create an empty new world map.
   tax_timer = 0
   tax_total = 0

   world_map = WorldMap( world_map_sz )
   city = City( world_map, pos=(world_map_sz / 2, world_map_sz / 2) )
   city.add_building( Building( BUILDING_RESIDENTIAL_LOW, 100 ) )
   
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

      tax_timer += 1
      if tax_timer > tax_timer_max:
         # Collect taxes and build a new building if we have enough.
         city.treasury += tax_total

      for row in world_map.tiles:
         assert( None != row )
         for tile in row:
            #if tile and tile.icon:
            #   screen.blit( tile.icon, (0, 0) )
            pass

      pygame.display.flip()

      clock.tick( 60 )

if '__main__' == __name__:
   main()

