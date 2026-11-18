from models import Rental
from datetime import datetime


class RentalManagement:
    def __init__(self, bike_management, rentals, pricing_manager):
        self.bike_management = bike_management
        self.rentals = rentals
        self.pricing_manager = pricing_manager

    def uniq_rental_id(self):
        new_id = max((int(rental.rental_id[1:]) for rental in self.rentals), default=0) + 1
        return f"R{new_id:03d}"

    def get_rental_by_id(self, rental_id):
        for rental in self.rentals:
            if rental.rental_id == rental_id:
                return rental


    def get_active_rentals(self):
        active_rentals = []
        for rental in self.rentals:
            if rental.status == "Active":
                active_rentals.append(rental)
        return active_rentals

    def get_rentals_by_customer(self, customer_name):
        return[rental for rental in self.rentals if rental.customer_name == customer_name]


    def is_bike_available(self, bike_id):
        bike = self.bike_management.get_bike_by_id(bike_id)
        if not bike:
            return False
        return bike.is_available and bike.is_operational

    def update_bike_operational_status(self, bike_id, is_operational):
        bike = self.bike_management.get_bike_by_id(bike_id)
        if not bike:
            return (False, "Bike not found")
        
        for rental in self.get_active_rentals():
            if rental.bike_id == bike_id:
                return (False, "Cannot change operational status while bike has an active rental")
        
        self.bike_management.set_bike_operational(bike_id, is_operational)
        return (True, "Operational status updated successfully")

    def create_rental(self,bike_id,expected_return_datetime,customer_name):
        bike = self.bike_management.get_bike_by_id(bike_id)
        if not bike:
            return (False, 'Bike not found')
        if not bike.is_operational:
            return (False,'Bike not operational')
        if not bike.is_available:
            return (False,'Bike not available')
        start_datetime = datetime.now()
        if expected_return_datetime <= start_datetime:
            return (False, 'Expected return datetime must be after start datetime')
        rental_id = self.uniq_rental_id()
        total_price = self.pricing_manager.calculate_price(bike,start_datetime,expected_return_datetime)
        rental = Rental(rental_id, customer_name, bike_id, start_datetime, expected_return_datetime, None, total_price, 0.0, "Active")
        self.rentals.append(rental)
        bike.set_available(False)
        return (True, rental)

    def return_bike(self,rental_id,):
        rental = self.get_rental_by_id(rental_id)
        if not rental:
            return (False, 'Rental not found')
        if rental.status != "Active":
            return (False, 'Rental is not active')
        bike = self.bike_management.get_bike_by_id(rental.bike_id)
        if not bike:
            return (False, 'Bike not found')
        actual_return_datetime = datetime.now()
        late_fee = self.pricing_manager.calculate_late_fee(rental.expected_return_datetime, actual_return_datetime)
        rental.complete_rental(actual_return_datetime, late_fee)
        if bike.is_operational:
            try:
                bike.set_available(True)
            except ValueError as e:
                return (False, str(e))
        return (True, rental)
