from pathlib import Path
import json
from models import Bike,Rental


class DataManager:
    def __init__(self,bikes_file =Path(__file__).parent / "bikes.json" , rentals_file=Path(__file__).parent / "rentals.json"):
        self.bikes_file = bikes_file
        self.rentals_file = rentals_file

    def load_bikes(self):
        with open(self.bikes_file, "r", encoding="utf-8") as file:
            bikes = json.load(file)
        return [Bike.from_dict(bike) for bike in bikes]

    def load_rentals(self):
        with open(self.rentals_file, "r", encoding="utf-8") as file:
            rentals = json.load(file)
        return [Rental.from_dict(rental ) for rental in rentals]


    def save_bikes(self,bikes):
        dict_bikes = [bike.to_dict() for bike in bikes]
        with open(self.bikes_file, "w", encoding="utf-8") as file:
            json.dump(dict_bikes, file, indent=2, ensure_ascii=False)

    def save_rentals(self, rentals):
        dict_rentals = [rental.to_dict() for rental in rentals]
        with open(self.rentals_file, "w", encoding="utf-8") as file:
            json.dump(dict_rentals, file, indent=2, ensure_ascii=False)