"""
    Daily Weather Mobile Messanger

    By: Jhon Tabio
"""
import http.client
import json
import smtplib
import os

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow Fall",
    73: "Moderate Snow Fall",
    75: "Heavy Snow Fall",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail"}

def convertCelsiusToFahrenheit(temp: float) -> float:
    return (temp * (9 / 5) + 32)

def getJSONInfo(longitude: float, latitude: float) -> dict:
    host = "api.open-meteo.com" # Friendly online API
    connection = http.client.HTTPConnection(host) # Establish a connection with the host
    # Push a 'GET' request to the URL
    connection.request("GET", f"/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m", headers={"Host": host})

    response = connection.getresponse() # Retrieve a response from the connection request
    html = response.read() # Read in the payload

    jsonInfo = json.loads(html) # Load a json file from a string

    #print(jsonInfo)

    return jsonInfo

def parseJSON(json: dict):
    print("Temperature ", convertCelsiusToFahrenheit(json.get("current_weather").get("temperature")), " F / ", json.get("current_weather").get("temperature"), " C")
    #print("Timezone: ", json.get("timezone_abbreviation"))
    print("Timezone: ", json["timezone_abbreviation"])
    print("Windspeed: ", json.get("current_weather").get("windspeed"))
    print("Winddirection: ", json.get("current_weather").get("winddirection"))
    print("Weather code: ", WEATHER_CODES.get(json.get("current_weather").get("weathercode")), " (", json.get("current_weather").get("weathercode"), ")")

# Take in PII information
# TODO: Change this up and use a proper database in the future (JSON[?])
def validateInfo() -> []:
    email_credentials = []
    try:
        email = open("src/emailInfo.txt", 'r')
        email_credentials = email.read().split('\n')
        email_credentials.pop()
    except FileNotFoundError:
        print("ERROR: The email login info was not found.")
    finally:
        email.close()
    
    recipient_info = None

    try:
        recipient = open("src/recipient.txt", 'r')
        recipient_info = recipient.read().split('\n')
        recipient_info.pop()
    except FileNotFoundError:
        print("ERROR: The recipient(s) info was not found.")
    finally:
        recipient.close()

    return [email_credentials, recipient_info]


def sendMessage():
    print("test")

def main():
    ucfLongitude, ucfLatitude = 81.2001, 28.6024
    info = validateInfo()

    print(info)
    #json = getJSONInfo(ucfLongitude, ucfLatitude)

    #parseJSON(json)

if __name__ == "__main__":
    main()
    print("Completed")
