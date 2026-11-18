
class ReportManager:
    def __init__(self, rental_manager):
        self.rental_manager = rental_manager

    def number_of_active_rentals(self):
        return len(self.rental_manager.get_active_rentals())

    def number_of_all_rentals(self):
        return len(self.rental_manager.rentals)

    def completed_rentals_number(self):
        return len([rental for rental in self.rental_manager.rentals if rental.status == "Completed"])

    def total_revenue(self):
        return sum(rental.total_price + rental.late_fee for rental in self.rental_manager.rentals if rental.status == "Completed")

    def total_late_fees(self):
        return sum(rental.late_fee for rental in self.rental_manager.rentals if rental.status == "Completed")

    def most_rental_customer(self):
        customer_rental_count = {}
        for rental in self.rental_manager.rentals:
            if rental.customer_name in customer_rental_count:
                customer_rental_count[rental.customer_name] += 1
            else:
                customer_rental_count[rental.customer_name] = 1
        if not customer_rental_count:
            return None
        return max(customer_rental_count, key=customer_rental_count.get)

    def most_rented_bike(self):
        bike_rental_count = {}
        for rental in self.rental_manager.rentals:
            if rental.bike_id in bike_rental_count:
                bike_rental_count[rental.bike_id] += 1
            else:
                bike_rental_count[rental.bike_id] = 1
        if not bike_rental_count:
            return None
        return max(bike_rental_count, key=bike_rental_count.get)

    def average_rental_price(self):
        if not self.rental_manager.rentals:
            return 0
        return round(sum(rental.total_price for rental in self.rental_manager.rentals) / len(self.rental_manager.rentals), 2)