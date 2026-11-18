class PricingManager:
    def calculate_price(self, bike, start_datetime, expected_return_datetime):
        duration = (expected_return_datetime - start_datetime).total_seconds()
        hours = duration // 3600
        if duration % 3600 > 0:
            hours += 1
        if hours < 24:
            return hours * bike.hourly_price
        else:
            return bike.daily_price * (hours // 24) + bike.hourly_price * (hours % 24)

    def calculate_late_fee(self, expected_return_datetime, actual_return_datetime):
        late = (actual_return_datetime - expected_return_datetime).total_seconds()
        if late <= 0:
            return 0
        elif late <= 3600:
            return 20
        elif late <= 10800:
            return 50
        else:
            return 100

        
        
        
        
