import csv
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
from fontTools.misc.cython import returns

def flight_schedule(first=False) -> dict:

    if first:
        print(f"Flight schedule loaded...")

    schedule = {}

    with open("pilot_data.csv", "r") as file:

        reader = csv.reader(file, delimiter=";")

        for row in reader:

            pilot_id = row[0]

            schedule[pilot_id] = {
                'name': row[1],
                'flight_id': row[2],
                'coord': row[3],
                'start_time': row[4],
                'end_time': row[5]
            }

    if not first:
        for pilot_id, details in schedule.items():
            print(f"Pilot {pilot_id} name is {details['name']} they are scheduled to fly on {details['start_time']}")

    return schedule

def display_flight_time(schedule: dict):

    pilot_id = input("Type the pilot id for the start date/time are you wanting to see?")

    if pilot_id in schedule:

        name = schedule[pilot_id]["name"]

        start_time = schedule[pilot_id]["start_time"]

        print(f"{name} has a scheduled flight for {start_time}")

    else:
        print("sorry that pilot was not found")

def validate_time(check_in_time: str) -> bool:
    try:
        datetime.strptime(check_in_time, "%H:%M:%S")

        print("Time is valid")
        return True

    except ValueError:
        print("Invalid time format")
        return False

def check_in(pilot_id: str, schedule: dict, time_checked_in: str):

        if pilot_id not in schedule:
            print("Pilot ID not found")
            return

        scheduled_time = schedule[pilot_id]["start_time"]

        scheduled_time_obj = datetime.strptime(scheduled_time.split(" ")[1], "%H:%M:%S")
        check_in_time_obj = datetime.strptime(time_checked_in, "%H:%M:%S")

        one_hour_before = scheduled_time_obj - timedelta(hours=1)

        if check_in_time_obj <= one_hour_before:
            print("You have checked in successfully")
        else:
            print("You have checked in late")
            logging_late_check_in(pilot_id)

def logging_late_check_in(pilot_id: str):
    msg = "checked in late"

    with open("late_checkin.csv", "a") as file:

        file.write(f"{pilot_id};{msg}\n")

    print("You logged in late.")

def haversine(coord1: str, coord2: str) -> float:

    lat1, lon1 = map(float, coord1.split(","))

    lat2, lon2 = map(float, coord2.split(","))

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    #earth radius in km
    R = 6371
    distance = R * c
    return distance


def detect_conflict(pilot1: str, pilot2: str, schedule: dict):

    coord1 = schedule[pilot1]["coord"]
    flight_id1 = schedule[pilot1]["flight_id"]
    start_time1 = schedule[pilot1]["start_time"]

    coord2 = schedule[pilot2]["coord"]
    flight_id2 = schedule[pilot2]["flight_id"]
    start_time2 = schedule[pilot2]["start_time"]

    distance = haversine(coord1, coord2)

    if distance < 500 and start_time1 == start_time2:
        print(
            f"Conflict detected between pilot {pilot1} (Flight {flight_id1}) and pilot {pilot2} (Flight {flight_id2}) "
            f"at {coord1} and {coord2}. Distance: {distance:.2f} km."
        )
    else:
        print("No conflict detected.")

def main():
    schedule = flight_schedule(first=True)
    while True:
        choice = int(input("Flight Control & Scheduling of Pilots\n"
                           "1. Show flight schedule\n"
                           "2. Check flight start time for a pilot\n"
                           "3. Pilot check in\n"
                           "4. Detect conflict for flights\n"
                           "5. Exit\n"))
        match choice:
            case 1:
                flight_schedule(first=False)
            case 2:
                display_flight_time(schedule)

            case 3:
                pilot_id = input("Please enter the pilot's id for check in: ")
                check_in_time = input("What time are they checking in? ")

                if validate_time(check_in_time):  # Only proceed if time is valid
                    check_in(pilot_id, schedule, check_in_time)
                else:
                    print("Incorrect format. Enter it as HH:MM:SS.")

            case 4:
                pilot_id1 = input("Please enter the pilot's id")
                pilot_id2 = input("Please enter the second pilot's id")
                detect_conflict(pilot_id1, pilot_id2, schedule)

            case 5:
                break

            case _:
                print("Incorrect choice entered")

if __name__ == '__main__':
    main()
