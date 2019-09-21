
from isogeography import WorldMap, WorldArea
from isoresource import Resource, Converter, Receiver

class City( WorldArea, Receiver ):

    buildings = []
    build_range = 0

    def __init__( self, world_map, limits, treasury=0 ):
        super( City, self ).__init__( world_map, limits )
        self.treasury = treasury

    def add_building( self, building ):
        building.city = self
        self.buildings.append( building )

    def collect_tax( self ):
        tax_total = 0
        for building in self.buildings:
            tax_total += building.tax_income
        return tax_total

    def simulate( self ):
        for bldg in self.buildings:
            bldg.simulate()

