import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 40.058323 # My latitude 40.058323
MY_LONG = -74.405663 # My longitude -74.405663

My_EMAIL = "kimbu2004@naver.com"
MY_PASSWORD = None
smtp_name = "stmp.naver.com"
smtp_port = 465

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if sunset <= time_now.hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("stmp.naver.com")
        connection.starttls()
        connection.login(My_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=My_EMAIL,
            to_addrs="kimbk678@gmail.com",
            msg="The ISS is above you in the sky. Look at the sky"
        )




