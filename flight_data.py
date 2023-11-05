class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self,
                 price,
                 origin_city,
                 origin_airport,
                 destination_city,
                 destination_airport,
                 out_date,
                 return_date):
        self.best_price = price
        self.from_city = origin_city
        self.to_city = destination_city
        self.from_airport = origin_airport
        self.to_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

