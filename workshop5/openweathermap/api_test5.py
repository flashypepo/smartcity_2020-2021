"""
demo openweather API-request
2020-1102 PP new - version 5 - OOP versie
"""
from lib.openweathermap import OpenWeaterMap

if __name__ == "__main__":
    #city_name = "Almere Stad"
    city_name = "Bussum"

    country_code = "NL"
    print(f"Weersrapport voor {city_name} in {country_code}:")

    service = OpenWeaterMap(city_name, country_code)

    # haal op de weersgegeven voor city_name
    t, temp_min, temp_max = service.temperatures()
    wind_speed = service.windspeed()
    description = service.description()

    # toon de weersgegevesn in console
    print("Beschrijving: {}".format(description))
    print ("Max.temperatuur: {:4.2f}\u00b0C".format(temp_max))
    print ("Wind snelheid: {:4.2f} m/s".format(wind_speed))
