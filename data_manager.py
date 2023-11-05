from auth import USER_SHEETY, TOKEN_SHEETY
import requests

PROJECT = "flightDeals"
SHEET = "price"
#SHEETY free tier allows 200 request/month, 100 requests/sheet
url_sheety = f"https://api.sheety.co/{USER_SHEETY}/{PROJECT}/{SHEET}s"
headers_sheety = {
        "Authorization": f"Bearer {TOKEN_SHEETY}",
        }

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destinations_data = {}

    def get_destinations_data(self):
        response = requests.get(url=url_sheety,
                                headers=headers_sheety).json()

        self.destinations_data = response["prices"]
        return(self.destinations_data)

    def update_destinations_data(self, update_city = {}):
        #If the optional parameter is empty, update everything
        if update_city == {}:
            print("Updating all cities IATA codes one by one")
            for city in self.destinations_data:
                #Mind the singular number of "price"
                iata_data = {"price": {"iataCode": city["iataCode"]}}
                url_put = f"{url_sheety}/{city['id']}"
                response = requests.put(url=url_put,
                                        json=iata_data,
                                        headers=headers_sheety)
                print(response.text)
        #Otherwise, update the single city passed in the parameter
        else:
            print(f"Updating a single city IATA code: {update_city['city']}")
            #Mind the singular number of "price"
            iata_data = {"price": {"iataCode": update_city["iataCode"]}}
            url_put = f"{url_sheety}/{update_city['id']}"
            response = requests.put(url=url_put, json=iata_data,
                                    headers=headers_sheety)
            print(response.text)
