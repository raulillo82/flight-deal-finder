#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from datetime import datetime as dt
from datetime import timedelta

#Bilbao as closest airport with high traffic
#FROM = "BIO"
#Using London for testing purposes
#FROM = "LON"

#Uncomment next block to use "400 km from Vitoria-Gasteiz"
DISTANCE = 400
COORDS_VITORIA = (42.846859, -2.671590)
FROM = f"{COORDS_VITORIA[0]}-{COORDS_VITORIA[1]}-{DISTANCE}km"

#Get the existing info from Google Sheets
data_manager = DataManager()
destinations_data = data_manager.get_destinations_data()

#Check if any destination does not have an IATA code for the city
if any(destination["iataCode"] == "" for destination in destinations_data):
    for destination in destinations_data:
        #Only update the IATA code if it is empty
        #Reason is to "save" in the very limited requests/month
        if destination["iataCode"] == "":
            #Use tequila API to search for the code
            search = FlightSearch()
            print(f"Searching IATA code for {destination['city']}")
            iata_code = search.get_destination_code(destination["city"])
            #Write the code into Google Sheets, updating the row
            destination["iataCode"] = iata_code
            print(f"Saving code {iata_code} into Google Sheets")
            data_manager.update_destinations_data(destination)

tomorrow = (dt.now()+timedelta(days=1))#.strftime("%d/%m/%Y")
six_months_from_today = (dt.now()+timedelta(days=180))#.strftime("%d/%m/%Y")

#Check for flights:
flight_search = FlightSearch()
notification = NotificationManager()
emails_to_list = (input("Send notifications also to mailing list [Y/N]?: ").lower() == "y")
print(emails_to_list)
for destination in destinations_data:
    flight = flight_search.check_flights(
            FROM, destination["iataCode"],
            tomorrow, six_months_from_today)
    #Send notification only if price is within budget in Google Sheets:
    if flight != None and flight.best_price <= destination["lowestPrice"]:
        print("Price within budget, sending telegram notification\n")
        message = f"Low price alert! Only {flight.best_price}€ to fly "
        message += f"from {flight.from_city}-{flight.from_airport} "
        message += f"to {flight.to_city}-{flight.to_airport}, "
        message += f"from {flight.out_date} to {flight.return_date} "
        message += f"with {flight.airline}"
        if flight.stop_overs == 2:
            message += f", via {flight.via_city_inbound}"
            if flight.via_city_inbound != flight.via_city_return:
                message += f" inbound and via {flight.via_city_return} return."
            else:
                message += "."
        else:
            message += "."
        notification.telegram_bot_sendtext(message)
        if emails_to_list:
            emails = [element["email"] for element in data_manager.get_emails()]
            #names = [element["firstName"] for element in data_manager.get_emails()]
            mail_message = f"Subject:Cheap flight alert!\n\n"
            mail_message += message
            mail_message = mail_message.encode("utf-8")
            notification.send_email(mail_message, emails)
    else:
        print("Price out of budget or no results found\n")

