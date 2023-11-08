from auth import API_KEY_TEQUILA, CLIENT_ID_AMADEUS, CLIENT_SECRET_AMADEUS
from flight_data import FlightData
import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        pass

    def get_destination_airline(self, iata_code):
        #AMADEUS TEST API allows 10 requests per user per second
        url_amadeus_token = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers_token_amadeus = {
                "Content-Type": "application/x-www-form-urlencoded",
                }
        query_token = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID_AMADEUS,
                "client_secret": CLIENT_SECRET_AMADEUS,
                }
        token_amadeus = requests.post(url=url_amadeus_token,
                                      data=query_token,
                                      headers=headers_token_amadeus).json()["access_token"]
        url_amadeus_query = "https://test.api.amadeus.com/v1/reference-data/airlines"
        headers_amadeus_query = {
                "Authorization": f"Bearer {token_amadeus}",
                }
        query_airline_name = {
                "airlineCodes": iata_code,
                }
        response = requests.get(url=url_amadeus_query,
                                params=query_airline_name,
                                headers=headers_amadeus_query).json()
        airline = response["data"][0]["commonName"].title()#Also check "businessName"
        return airline

    def get_destination_city(self, iata_code):
        url_tequila = "https://api.tequila.kiwi.com"
        #TEQUILA API allows 30 request per minute
        url_get = f"{url_tequila}/locations/query"
        headers_tequila = {
                "apikey": API_KEY_TEQUILA,
                }
        query = {
                "term": iata_code,
                "location_types": "city",
                #Limit the query to one city,
                #anyway only looking into the first result:
                "limit": 1,
                }
        response = requests.get(url=url_get,
                                params=query,
                                headers=headers_tequila).json()
        city = response["locations"][0]["name"]
        return city

    def get_destination_code(self, city):
        url_tequila = "https://api.tequila.kiwi.com"
        #TEQUILA API allows 30 request per minute
        url_get = f"{url_tequila}/locations/query"
        headers_tequila = {
                "apikey": API_KEY_TEQUILA,
                }
        query = {
                "term": city,
                "location_types": "city",
                #Limit the query to one city,
                #anyway only looking into the first result:
                "limit": 1,
                }
        response = requests.get(url=url_get,
                                params=query,
                                headers=headers_tequila).json()
        code = response["locations"][0]["code"]
        return code

    def check_flights(self, origin_city, dest_city, from_date, to_date):
        url_tequila = "https://api.tequila.kiwi.com"
        #TEQUILA API allows 30 request per minute
        url_get = f"{url_tequila}/v2/search"
        headers_tequila = {
                "apikey": API_KEY_TEQUILA,
                }
        #Customize query according to https://tequila.kiwi.com/portal/docs/tequila_api/search_api
        query = {
                "fly_from": origin_city,
                "fly_to": dest_city,
                "date_from": from_date.strftime("%d/%m/%Y"),
                "date_to": to_date.strftime("%d/%m/%Y"),
                "flight_type": "round",
                "nights_in_dst_from": 2,
                "nights_in_dst_to": 7,
                "max_stopovers": 0,
                "curr": "EUR",
                #Some other interesting parameters:
                #"price_from": 0,
                #"price_to": max_price,
                #Looking for lowest price, more results make no sense
                #Commented as "one_for_city" already gives only one result
                #"limit": 1,
                "one_for_city": 1,
                }
        response = requests.get(url=url_get,
                                params=query,
                                headers=headers_tequila)
        #Expect IndexError exceptions when no results:
        try:
            data = response.json()["data"][0]
            self.best_price = response.json()["data"][0]["price"]
            self.from_city = response.json()["data"][0]["cityFrom"]
            self.to_city = response.json()["data"][0]["cityTo"]
        except IndexError:
            city = self.get_destination_city(dest_city)
            print(f"No flights found to {city}")
            flight_data = None
        else:
            airline_name = self.get_destination_airline(
                    data["route"][0]["airline"])
            flight_data = FlightData(
                    data["price"],
                    data["route"][0]["cityFrom"],
                    data["route"][0]["flyFrom"],
                    data["route"][0]["cityTo"],
                    data["route"][0]["flyTo"],
                    data["route"][0]["local_departure"].split("T")[0],
                    data["route"][1]["local_departure"].split("T")[0],
                    airline_name)
            print(f"{flight_data.from_city} - "
                  f"{flight_data.to_city}: "
                  f"{flight_data.best_price}€, "
                  f"out on {flight_data.out_date} and "
                  f"return on {flight_data.return_date} "
                  f"with {flight_data.airline}")
        return flight_data
