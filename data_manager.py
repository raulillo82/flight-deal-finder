from auth import USER_SHEETY, TOKEN_SHEETY
import requests

PROJECT = "flightDeals"
SHEET1 = "price"
SHEET2 = "user"
#SHEETY free tier allows 200 request/month, 100 requests/sheet
url_sheety_prices = f"https://api.sheety.co/{USER_SHEETY}/{PROJECT}/{SHEET1}s"
url_sheety_users = f"https://api.sheety.co/{USER_SHEETY}/{PROJECT}/{SHEET2}s"
headers_sheety = {
        "Authorization": f"Bearer {TOKEN_SHEETY}",
        }

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destinations_data = {}

    def get_destinations_data(self):
        response = requests.get(url=url_sheety_prices, headers=headers_sheety).json()

        self.destinations_data = response["prices"]
        return(self.destinations_data)

    def update_destinations_data(self, update_city = {}):
        #If the optional parameter is empty, update everything
        if update_city == {}:
            print("Updating all cities IATA codes one by one")
            for city in self.destinations_data:
                #Mind the singular number of "price"
                iata_data = {"price": {"iataCode": city["iataCode"]}}
                url_put = f"{url_sheety_prices}/{city['id']}"
                response = requests.put(url=url_put,
                                        json=iata_data,
                                        headers=headers_sheety)
                print(response.text)
        #Otherwise, update the single city passed in the parameter
        else:
            print(f"Updating a single city IATA code: {update_city['city']}")
            #Mind the singular number of "price"
            iata_data = {"price": {"iataCode": update_city["iataCode"]}}
            url_put = f"{url_sheety_prices}/{update_city['id']}"
            response = requests.put(url=url_put, json=iata_data,
                                    headers=headers_sheety)
            print(response.text)

    def update_emails(self, fname, lname, email):
        print(f"Updating names database with {fname}'s email")
        #Mind the singular number of "price"
        user_data = {"user": {"firstName": fname,
                              "lastName": lname,
                              "email": email,}}
        url_post = url_sheety_users
        response = requests.post(url=url_post, json=user_data,
                                headers=headers_sheety)
        print(response.text)
