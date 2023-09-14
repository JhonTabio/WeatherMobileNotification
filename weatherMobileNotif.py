"""
    Daily Weather Mobile Messanger

    By: Jhon Tabio
"""
import http.client
import json
import smtplib
import sched

from datetime import datetime, timedelta
from time import sleep
from threading import Timer

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
    connection.request("GET", f"/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,windspeed_10m,winddirection_10m,weathercode", headers={"Host": host})

    response = connection.getresponse() # Retrieve a response from the connection request
    html = response.read() # Read in the payload

    jsonInfo = json.loads(html) # Load a json file from a string

    return jsonInfo

def parseJSON(json: dict) -> str:
    hourly = json["hourly"]["time"]

    # Convert UTC -> EST
    time_12 = json["current_weather"]["time"][0:11] + "16:00"
    time_3 = json["current_weather"]["time"][0:11] + "19:00"
    time_5 = json["current_weather"]["time"][0:11] + "21:00"
    time_10 = json["current_weather"]["time"][0:11] + "01:00"

    ret = "\n---Current Time--------------\n"
    ret += "Temp: %.2fF / %.2fC\nWind: %s @ %s\nWeather: %s" % (convertCelsiusToFahrenheit(json["current_weather"]["temperature"]), json["current_weather"]["temperature"], json["current_weather"]["winddirection"], json["current_weather"]["windspeed"], WEATHER_CODES.get(json["current_weather"]["weathercode"]))

    ret += "\n---12pm---------------------\n"
    ret += "Temp: %.2fF / %.2fC\nWind: %s @ %s\nWeather: %s" % (convertCelsiusToFahrenheit(json["hourly"]["temperature_2m"][hourly.index(time_12)]), json["hourly"]["temperature_2m"][hourly.index(time_12)], json["hourly"]["winddirection_10m"][hourly.index(time_12)], json["hourly"]["windspeed_10m"][hourly.index(time_12)], WEATHER_CODES.get(json["hourly"]["weathercode"][hourly.index(time_12)]))

    ret += "\n---3pm----------------------\n"
    ret += "Temp: %.2fF / %.2fC\nWind: %s @ %s\nWeather: %s" % (convertCelsiusToFahrenheit(json["hourly"]["temperature_2m"][hourly.index(time_3)]), json["hourly"]["temperature_2m"][hourly.index(time_3)], json["hourly"]["winddirection_10m"][hourly.index(time_3)], json["hourly"]["windspeed_10m"][hourly.index(time_3)], WEATHER_CODES.get(json["hourly"]["weathercode"][hourly.index(time_3)]))

    ret += "\n---5pm----------------------\n"
    ret += "Temp: %.2fF / %.2fC\nWind: %s @ %s\nWeather: %s" % (convertCelsiusToFahrenheit(json["hourly"]["temperature_2m"][hourly.index(time_5)]), json["hourly"]["temperature_2m"][hourly.index(time_5)], json["hourly"]["winddirection_10m"][hourly.index(time_5)], json["hourly"]["windspeed_10m"][hourly.index(time_5)], WEATHER_CODES.get(json["hourly"]["weathercode"][hourly.index(time_5)]))

    ret += "\n--10pm----------------------\n"
    ret += "Temp: %.2fF / %.2fC\nWind: %s @ %s\nWeather: %s" % (convertCelsiusToFahrenheit(json["hourly"]["temperature_2m"][hourly.index(time_10)]), json["hourly"]["temperature_2m"][hourly.index(time_10)], json["hourly"]["winddirection_10m"][hourly.index(time_10)], json["hourly"]["windspeed_10m"][hourly.index(time_10)], WEATHER_CODES.get(json["hourly"]["weathercode"][hourly.index(time_10)]))

    return ret

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


def sendMessage(user: str, password: str, recipient: str, header: str, msg: str):
    try:
        send = "From: %s\nTo:%s\nSubject: Daily Weather Notification (%s)\n%s" % (user, recipient, header, msg)

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(user, password)
        server.sendmail(user, recipient, send)
    except Exception:
        print("ERROR: There was an error formatting the Email.")
    finally:
        server.quit()

def getSecondDelay() -> float:
    date = datetime.today()
    updated_date = date.replace(day=date.day, hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = updated_date - date
    return delta_t.total_seconds()

def main():
    ucfLongitude, ucfLatitude = 81.2001, 28.6024
    info = validateInfo()

    sendMessage(info[0][0], info[0][1], info[1][0], "UCF", parseJSON(getJSONInfo(ucfLongitude, ucfLatitude)))

if __name__ == "__main__":
    while True:
        main()
        sleep(getSecondDelay())
