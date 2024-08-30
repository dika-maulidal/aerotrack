def display_aircraft_info(tail_number, data):
    if not data:
        print(f"\n\033[1mAircraft Information for {tail_number}\033[0m")
        print("Aircraft information not found.")
    else:
        print(f"\n\033[1mAircraft Information for {tail_number}\033[0m")
        for key, value in data.items():
            print(f"{key}: {value}")

def display_registration_history(history_rows):
    print("\n\033[1mRegistration History\033[0m")
    if history_rows:
        print(f"{'Date':<20} {'Owner':<30} {'Location'}")
        print("-" * 70)
        for row in history_rows:
            columns = row.find_all('td')
            if len(columns) == 3:
                date = columns[0].get_text(strip=True)
                owner = columns[1].get_text(strip=True)
                location = columns[2].get_text(strip=True)
                print(f"\033[94m{date:<20} {owner:<30} {location}\033[0m")
    else:
        print("Registration history not found.")

def display_flight_history(flight_rows):
    print("\n\033[1mFlight History\033[0m")
    if flight_rows:
        print(f"{'Date':<15} {'Departure':<15} {'Arrival':<15} {'Aircraft':<10} {'Duration':<10}")
        print("-" * 68)
        for row in flight_rows:
            columns = row.find_all('td')
            if len(columns) == 7:
                date = columns[0].get_text(strip=True)
                departure = columns[4].get_text(strip=True)
                arrival = columns[5].get_text(strip=True)
                aircraft = columns[1].get_text(strip=True)
                duration = columns[6].get_text(strip=True)
                print(f"\033[94m{date:<15} {departure:<15} {arrival:<15} {aircraft:<10} {duration:<10}\033[0m")
    else:
        print("Flight history not found.")