from datetime import datetime


class Bike:
    def __init__(self, bike_id, model, bike_type, hourly_price, daily_price, is_available, is_operational):
        self.__bike_id = bike_id
        self.model = model
        self.bike_type = bike_type
        self.hourly_price = hourly_price
        self.daily_price = daily_price
        self.__is_operational = is_operational
        if not is_operational:
            self.__is_available = False
        else:
            self.__is_available = is_available

    def set_available(self, status):
        if not self.__is_operational and status:
            raise ValueError("Cannot set bike as available when it is not operational.")
        self.__is_available = status

    def set_operational(self, status):
        self.__is_operational = status
        self.__is_available = status 
    @property
    def bike_id(self):
        return self.__bike_id
    @property
    def is_available(self):
        return self.__is_available
    @property
    def is_operational(self):
        return self.__is_operational
    

    def to_dict(self):
        return {
            "bike_id": self.__bike_id,
            "model": self.model,
            "bike_type": self.bike_type,
            "hourly_price": self.hourly_price,
            "daily_price": self.daily_price,
            "is_available": self.__is_available,
            "is_operational": self.__is_operational
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            bike_id=data["bike_id"],
            model=data["model"],
            bike_type=data["bike_type"],
            hourly_price=data["hourly_price"],
            daily_price=data["daily_price"],
            is_available=data["is_available"],
            is_operational=data["is_operational"]
        )


class Rental:
    def __init__(self, rental_id, customer_name, bike_id, start_datetime, expected_return_datetime,
                 actual_return_datetime, total_price, late_fee, status):
        self.__rental_id = rental_id
        self.__bike_id = bike_id
        self.__customer_name = customer_name
        self.__start_datetime = start_datetime
        self.__expected_return_datetime = expected_return_datetime
        self.__actual_return_datetime = actual_return_datetime
        self.__total_price = total_price
        self.__late_fee = late_fee
        self.__status = status
    @property
    def rental_id(self):
        return self.__rental_id
    @property
    def bike_id(self):
        return self.__bike_id
    @property
    def customer_name(self):
        return self.__customer_name
    @property
    def start_datetime(self):
        return self.__start_datetime
    @property
    def expected_return_datetime(self):
        return self.__expected_return_datetime
    @property
    def actual_return_datetime(self):
        return self.__actual_return_datetime
    @property
    def total_price(self):
        return self.__total_price
    @property
    def late_fee(self):
        return self.__late_fee
    @property
    def status(self):
        return self.__status
    

    def complete_rental(self, return_datetime, late_fee):
        if self.__status != 'Completed':
            self.__actual_return_datetime = return_datetime
            self.__late_fee = late_fee
            self.__status = "Completed"

    def date_to_string(self, date):
        if date is None:
            return None
        if isinstance(date, datetime):
            return date.strftime("%Y-%m-%dT%H:%M:%S")
        return str(date)

    def to_dict(self):
        return {
            "rental_id": self.__rental_id,
            "bike_id": self.__bike_id,
            "customer_name": self.__customer_name,
            "start_datetime": self.date_to_string(self.__start_datetime),
            "expected_return_datetime": self.date_to_string(self.__expected_return_datetime),
            "actual_return_datetime": self.date_to_string(self.__actual_return_datetime),
            "total_price": self.__total_price,
            "late_fee": self.__late_fee,
            "status": self.__status
        }

    @classmethod
    def string_to_date(cls, date_string):
        if date_string is None:
            return None
        try:
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None

    @classmethod
    def from_dict(cls, data):
        return cls(
            rental_id=data["rental_id"],
            bike_id=data["bike_id"],
            customer_name=data["customer_name"],
            start_datetime=cls.string_to_date(data["start_datetime"]),
            expected_return_datetime=cls.string_to_date(data["expected_return_datetime"]),
            actual_return_datetime=cls.string_to_date(data["actual_return_datetime"]),
            total_price=data["total_price"],
            late_fee=data["late_fee"],
            status=data["status"]
        )