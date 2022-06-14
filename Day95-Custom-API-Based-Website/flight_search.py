import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "*********"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    # def __init__(self):
    #     self.city = city
    #     self.iatacode = "Testing"
    def get_destination_code(self, city_name):

        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey" : TEQUILA_API_KEY
        }

        params = {
            "term" : city_name,
            "location_types" : "city"
        }

        response = requests.get(url=location_endpoint, headers=headers, params=params)
        data = response.json()['locations']
        print(data)
        destination_code = data[0]['code']
        return destination_code

    def check_flights(self, origin_city_code, destination_city_code, departure_time, min_stay, max_stay, direction):
        flight_list = []


        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey" : TEQUILA_API_KEY
        }

        params = {
            "fly_from" : origin_city_code,
            "fly_to" : destination_city_code,
            "date_from" : departure_time.strftime("%d/%m/%Y"),
            "date_to" : departure_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from" : min_stay,
            "nights_in_dst_to" : max_stay,
            "flight_type" : direction,
            "one_for_city" : 0,
            "max_stopovers" : 0,
            "partner_market" : "us",
            "curr" : "USD"
        }


        response = requests.get(url=search_endpoint, headers=headers, params=params)

        try:
            data = response.json()['data']
            print(len(data))
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        for i in range(len(data)):
            if direction == "round":
                flight_data = FlightData(
                    price=data[i]['price'],
                    origin_city=data[i]['route'][0]['cityFrom'],
                    origin_airport=data[i]['route'][0]['cityCodeFrom'],
                    destination_city=data[i]['route'][0]['cityTo'],
                    destination_airport=data[i]['route'][0]['cityCodeTo'],
                    out_date=data[i]['route'][0]['local_departure'].split('T')[0],
                    return_date=data[i]['route'][1]['local_departure'].split('T')[0],
                    out_airline=data[i]['route'][0]['airline'],
                    return_airline=data[i]['route'][1]['airline']
                )
            else:
                flight_data = FlightData(
                    price=data[i]['price'],
                    origin_city=data[i]['route'][0]['cityFrom'],
                    origin_airport=data[i]['route'][0]['cityCodeFrom'],
                    destination_city=data[i]['route'][0]['cityTo'],
                    destination_airport=data[i]['route'][0]['cityCodeTo'],
                    out_date=data[i]['route'][0]['local_departure'].split('T')[0],
                    return_date="",
                    out_airline=data[i]['route'][0]['airline'],
                    return_airline=""
                )

            flight_list.append(flight_data)

            # print(f"{flight_data.out_date} ({flight_data.out_airline}) -> {flight_data.return_date} ({flight_data.return_airline}) : ${flight_data.price}

        return flight_list
