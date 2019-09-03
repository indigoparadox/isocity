
import logging

class Creator( object ):

   def __init__( self ):
      self.resources = {}
      self.logger = logging.getLogger( 'creator' )

   def pop_res( self, res_name, count ):
      if res_name in self.resources:
         if count <= self.resources[res_name]:
            self.resources[res_name] -= count
            assert 0 <= self.resources[res_name]
            return count
         else:
            diff = count - self.resources[res_name]
            self.resources[res_name] = 0
            return diff
      else:
         return 0

class Receiver( object ):

   def __init__( self ):
      self.resources = {}
      self.logger = logging.getLogger( 'receiver' )

   def push_res( self, res_name, count ):
      if not res_name in self.resources:
         self.resources.update( {res_name: count} )
      else:
         self.resources[res_name] += count


class Converter( Creator, Receiver ):

   class _Conversion( object ):
      def __init__( self, rcvr, res_in, res_out, ticks_mod, consume=False ):
         assert isinstance( res_in, tuple )
         assert isinstance( res_out, tuple )
         self.res_in = res_in[0]
         self.res_in_count = res_in[1]
         self.res_out = res_out[0]
         self.res_out_count = res_out[1]
         self.ticks_mod = ticks_mod
         self.consume = consume
         self.receiver = rcvr

   def __init__( self ):
      super( Converter, self ).__init__()
      self.ticks = 0
      self.conversions = []
      self.logger = logging.getLogger( 'converter' )

   def add_conversion( self, res_in, res_out, ticks_mod, consume=True ):
      cvt = Converter._Conversion( res_in, res_out, ticks_mod, consume )
      self.conversions.append( cvt )

   def simulate( self ):
      self.ticks += 1
      for cvt in self.conversions:
         if self.ticks % cvt.ticks_mod:
            if cvt.consume:
               if self.pop_res( cvt.res_in, cvt.res_in_count ):
                  cvt.rcvr.push_res( cvt.res_out, cvt.res_out_count )
            else:
               if self.resources[cvt.res_in] >= cvt.res_in_count:
                  cvt.rcvr.push_res( cvt.res_out, cvt.res_out_count )

class Resource( object ):

   def __init__( self ):
      pass

