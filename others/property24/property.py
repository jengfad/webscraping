class Property:  
    def __init__(self, 
    listing_name,
    total_price,
    listing_address,
    listing_title,
    listing_write_up,
    bedrooms,
    bathrooms,
    garages,
    garden,
    pets_allowed,
    listing_number,
    property_type,
    street_address,
    list_date,
    floor_area,
    lot_area,
    broker_name,
    url):
        self.listing_name=listing_name
        self.total_price=total_price
        self.listing_address=listing_address
        self.listing_title=listing_title
        self.listing_write_up=listing_write_up
        self.bedrooms=bedrooms
        self.bathrooms=bathrooms
        self.garages=garages
        self.garden=garden
        self.pets_allowed=pets_allowed
        self.listing_number=listing_number
        self.property_type=property_type
        self.street_address=street_address
        self.list_date=list_date
        self.floor_area=floor_area
        self.lot_area=lot_area
        self.broker_name=broker_name
        self.url=url

class Point_Of_Interest:
    def __init__(self,
    listing_number,
    category_name,
    item_name,
    distance):
        self.listing_number = listing_number
        self.category_name = category_name
        self.item_name = item_name
        self.distance = distance