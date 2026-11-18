from data_manager import DataManager
from bike_management import BikeManagement
from rental_management import RentalManagement
from pricing_manager import PricingManager 
from report_manager import ReportManager
from validators import valid_bike_type, valid_float, valid_date, valid_time, valid_str
from models import Rental

class CityRideSystem:
    def __init__(self):
        self.data_manager = DataManager()
        self.bikes = self.data_manager.load_bikes()
        self.rentals = self.data_manager.load_rentals()
        self.bike_management = BikeManagement(self.bikes)
        self.pricing_manager = PricingManager()
        self.rental_management = RentalManagement(self.bike_management, self.rentals, self.pricing_manager)
        self.report_manager = ReportManager(self.rental_management)

    def save_data(self):
        self.data_manager.save_bikes(self.bikes)
        self.data_manager.save_rentals(self.rentals)

    
    def main_menu(self):
        print("""
        ================================
                CITY RIDE MAIN MENU
        ================================
        1. Bike management
        2. Rental management
        3. Reports
        4. Exit
        """)


    def bikes_menu(self):
        print("""
        ================================
                BIKES MENU
        ================================
        1. Show all bikes
        2. Search for a bike by ID
        3. Show available bikes
        4. Add a new bike
        5. Update existing bike details
        6. Change bike operational status
        7. Back to main menu
        """)

    def bikes_main(self):
        active = True
        while active:
            self.bikes_menu()
            choice = valid_str('Choose an option: ')
            match choice:
                case '1':
                    for bike in self.bikes:
                        print(bike.to_dict())
                        print('-------------------')
                case '2':
                    bike_id = valid_str('Enter bike ID: ').upper()
                    bike = self.bike_management.get_bike_by_id(bike_id)
                    if bike:
                        print(bike.to_dict())
                    else:
                        print('Bike not found.')
                case '3':
                    available_bikes = self.bike_management.get_available_bikes()
                    if not available_bikes:
                        print('No available bikes at the moment.')
                    else:
                        for bike in available_bikes:
                            print(bike.to_dict())
                            print('-------------------')
                case '4':
                    model = valid_str('Enter bike model: ')
                    bike_type = valid_bike_type()
                    hourly_price = valid_float('Enter hourly price: ')
                    daily_price = valid_float('Enter daily price: ')
                    if daily_price < hourly_price :
                        print('Daily price cannot be less than hourly price.')
                        continue
                    self.bike_management.add_bike(model, bike_type, hourly_price, daily_price)
                    self.save_data()
                    print('Bike added successfully.')
                case '5':
                    bike_id = valid_str('Enter bike ID to update: ').upper()
                    bike = self.bike_management.get_bike_by_id(bike_id)
                    if not bike:
                        print('Bike not found.')
                        continue
                    choice = input('Which detail do you want to update? (model/type/hourly_price/daily_price): ').lower()
                    if choice == 'model':
                        new_model = valid_str('Enter new model: ')
                        self.bike_management.update_bike(bike_id, model=new_model)
                    elif choice == 'type':
                        new_type = valid_bike_type()
                        self.bike_management.update_bike(bike_id, bike_type=new_type)
                    elif choice == 'hourly_price':
                        new_hourly_price = valid_float('Enter new hourly price: ')
                        if new_hourly_price > bike.daily_price:
                            print('Hourly price cannot be greater than daily price.')
                            continue
                        self.bike_management.update_bike(bike_id, hourly_price=new_hourly_price)
                    elif choice == 'daily_price':
                        new_daily_price = valid_float('Enter new daily price: ')
                        if new_daily_price < bike.hourly_price:
                            print('Daily price cannot be less than hourly price.')
                            continue
                        self.bike_management.update_bike(bike_id, daily_price=new_daily_price)
                    else:
                        print('Invalid detail.')
                        continue
                    print('Bike updated successfully.')
                    self.save_data()
                case '6':  
                    bike_id = valid_str('Enter bike ID to change operational status: ').upper()
                    new_status = input('Enter new operational status (True/False): ').lower()
                    if new_status in ['true', 'false']:
                        is_operational = new_status == 'true'
                        success, message = self.rental_management.update_bike_operational_status(bike_id, is_operational)
                        print(message)
                        if success:
                            self.save_data()
                    else:
                        print('Invalid status. Please enter True or False.')
                case '7':
                    active = False
                case _:
                    print('Invalid option.')

    def rentals_menu(self):
        print("""
        ================================
                RENTALS MENU   
        ================================
        1. Create a new rental
        2. Search for a rental by ID   
        3. Search for rentals by customer name
        4. Show all active rentals
        5. Return a bike
        6. Back to main menu
        """)

    def rentals_main(self):
        active = True
        while active:
            self.rentals_menu()
            choice = valid_str('Choose an option: ')
            match choice:
                case '1':
                    customer_name = valid_str('Enter customer name: ')
                    bike_id = valid_str('Enter bike ID: ').upper()
                    expected_return_date = valid_date()
                    excepted_return_datetime = valid_time(expected_return_date)
                    success, result = self.rental_management.create_rental(bike_id, excepted_return_datetime,customer_name)
                    if success:
                        print('Rental created successfully.')
                        if isinstance(result, Rental):
                            print(result.to_dict())
                        self.save_data()
                    else:
                        print(f'Error creating rental: {result}')
                case '2':
                    rental_id = valid_str('Enter rental ID: ').upper()
                    rental = self.rental_management.get_rental_by_id(rental_id)
                    if rental:
                        print(rental.to_dict())
                    else:
                        print('Rental not found.')
                case '3':
                    customer_name = valid_str('Enter customer name: ')
                    rentals = self.rental_management.get_rentals_by_customer(customer_name)
                    if rentals:
                        for rental in rentals:
                            print(rental.to_dict())
                            print('-------------------')
                    else:
                        print('No rentals found for this customer.')
                case '4':
                    active_rentals = self.rental_management.get_active_rentals()
                    if active_rentals:
                        for rental in active_rentals:
                            print(rental.to_dict())
                            print('-------------------')
                    else:
                        print('No active rentals at the moment.')
                case '5':
                    rental_id = valid_str('Enter rental ID to return bike: ').upper()
                    success, result = self.rental_management.return_bike(rental_id)
                    if success:
                        print('Bike returned successfully.')
                        if isinstance(result, Rental):
                            print(result.to_dict())
                        self.save_data()
                    else:
                        print(f'Error returning bike: {result}')
                case '6':
                    active = False
                case _:
                    print('Invalid option. Please try again.')

    def reports_menu(self):
        print("""
        ================================
                REPORTS MENU  
        ================================
        1. Number of active rentals
        2. Number of all rentals   
        3. Number of completed rentals
        4. Total revenue
        5. Total late fees
        6. Customer with the most rentals
        7. Bike with the most rentals
        8. Average rental price
        9. Back to main menu
        """)

    def reports_main(self):
        active = True
        while active:
            self.reports_menu()
            choice = valid_str('Choose an option: ')
            match choice:
                case '1':
                    print(f'Number of active rentals: {self.report_manager.number_of_active_rentals()}')
                case '2':
                    print(f'Number of all rentals: {self.report_manager.number_of_all_rentals()}')
                case '3':
                    print(f'Number of completed rentals: {self.report_manager.completed_rentals_number()}')
                case '4':
                    print(f'Total revenue: ₪{self.report_manager.total_revenue():.2f}')
                case '5':
                    print(f'Total late fees: ₪{self.report_manager.total_late_fees():.2f}')
                case '6':
                    customer = self.report_manager.most_rental_customer()
                    if customer:
                        print(f'Customer with the most rentals: {customer}')
                    else:
                        print('No rentals found.')
                case '7':
                    bike_id = self.report_manager.most_rented_bike()
                    if bike_id:
                        bike = self.bike_management.get_bike_by_id(bike_id)
                        if bike:
                            print(f'Bike with the most rentals: {bike.to_dict()}')
                        else:
                            print('Bike not found.')
                    else:
                        print('No rentals found.')
                case '8':
                    print(f'Average rental price: ₪{self.report_manager.average_rental_price():.2f}')
                case '9':
                    active = False
                case _:
                    print('Invalid option. Please try again.')

    def run(self):
        active = True
        while active:
            self.main_menu()
            choice = valid_str('Choose an option: ')
            match choice:
                case '1':
                    self.bikes_main()
                case '2':
                    self.rentals_main()
                case '3':
                    self.reports_main()
                case '4':
                    print('Exiting the system. Goodbye!')
                    active = False
                case _:
                    print('Invalid option. Please try again.')

if __name__ == "__main__":
    system = CityRideSystem()
    system.run()