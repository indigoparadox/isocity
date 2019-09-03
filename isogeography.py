
class WorldArea( object ):

   def __init__( self, world_map, limits ):
      self.world_map = world_map
      self.limits = limits

class WorldMap( object ):

   def __init__( self, size ):

      self.size = size

      self.tiles = []
      for x in range( 0, self.size ):
         row = []
         for y in range( 0, self.size ):
            row.append( None )
         self.tiles.append( row )

