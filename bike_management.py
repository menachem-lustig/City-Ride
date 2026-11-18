from models import Bike


class BikeManagement:
    def __init__(self, bikes):
        self.bikes = bikes

    def get_bike_by_id(self, bike_id):
        for bike in self.bikes:
            if bike.bike_id == bike_id:
                return bike


    def get_all_bikes(self):
        return self.bikes

    def get_available_bikes(self):
        available_bikes = []
        for bike in self.bikes:
            if bike.is_available and bike.is_operational:
                available_bikes.append(bike)
        return available_bikes
    
    def uniq_bike_id(self):
            new_id = max((int(bike.bike_id[1:]) for bike in self.bikes),default=0) + 1
            return f"B{new_id:03d}"

        

    def add_bike(self, model, bike_type, hourly_price, daily_price, is_available=True, is_operational=True):
        bike_id = self.uniq_bike_id()
        new_bike = Bike(bike_id, model, bike_type, hourly_price, daily_price, is_available, is_operational)
        self.bikes.append(new_bike)


    def update_bike(self, bike_id, model=None, bike_type=None, hourly_price=None, daily_price=None):
        bike = self.get_bike_by_id(bike_id)
        if  not bike:
            print('bike not found')
            return
        if model:
            bike.model = model
        if bike_type:
            bike.bike_type = bike_type
        if hourly_price:
            bike.hourly_price = hourly_price
        if daily_price:
            bike.daily_price = daily_price
        print('updated successfully')
        return True


    def set_bike_operational(self, bike_id, is_operational):
        bike = self.get_bike_by_id(bike_id)
        if not bike:
            print('Not found')
            return
        bike.set_operational(is_operational)
        print('updated successfully')
        return True 
