import requests
from bs4 import BeautifulSoup

def scrape_registration_data(tail_number):
    flightaware_url = f"https://www.flightaware.com/resources/registration/{tail_number}"
    faa_url = f"https://registry.faa.gov/AircraftInquiry/Search/NNumberResult?nNumberTxt={tail_number}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    flightaware_response = requests.get(flightaware_url, headers=headers)
    if flightaware_response.status_code != 200:
        print(f"Failed to retrieve data from {flightaware_url}")
        return None
    
    soup = BeautifulSoup(flightaware_response.text, 'html.parser')
    data = {}
    
    rows = soup.find_all('div', class_='row attribute-row')
    
    for row in rows:
        title = row.find('div', class_='title-text').get_text(strip=True)
        
        if title in ["Summary", "Registry Source", "Status", "Speed"]:
            continue
        
        value_div = row.find('div', class_='medium-3 columns')
        for br in value_div.find_all('br'):
            br.decompose()
        
        value = ' '.join(value_div.get_text(strip=True).split())
        
        if title == "Mode S Code":
            title = "ICAO"
            if '/' in value:
                value = value.split('/')[-1].strip()
        
        data[title] = f"\033[94m{value}\033[0m"
    
    faa_response = requests.get(faa_url, headers=headers)
    if faa_response.status_code != 200:
        print(f"Failed to retrieve data from {faa_url}")
        return None
    
    faa_soup = BeautifulSoup(faa_response.text, 'html.parser')
    
    manufacture_name = faa_soup.find('td', string="Manufacturer Name")
    model_name = faa_soup.find('td', string="Model")
    
    if manufacture_name:
        manufacture_value = manufacture_name.find_next_sibling('td').get_text(strip=True)
        data['Manufacturer Name'] = f"\033[94m{manufacture_value}\033[0m"
    
    if model_name:
        model_value = model_name.find_next_sibling('td').get_text(strip=True)
        data['Model'] = f"\033[94m{model_value}\033[0m"

    address_keys = ["Street", "City", "State", "County", "Zip Code", "Country"]
    for key in address_keys:
        address_element = faa_soup.find('td', string=key)
        if address_element:
            address_value = address_element.find_next_sibling('td').get_text(strip=True)
            data[key] = f"\033[94m{address_value}\033[0m"

    if not data:
        print(f"\n\033[1mAircraft Information for {tail_number}\033[0m")
        print("Aircraft information not found.")
    else:
        print(f"\n\033[1mAircraft Information for {tail_number}\033[0m")
        for key, value in data.items():
            print(f"{key}: {value}")
    
    print("\n\033[1mRegistration History\033[0m")
    history_rows = soup.find_all('tr', class_=['row1', 'row2'])
    
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

def scrape_flight_history(tail_number):
    flight_history_url = f"https://www.flightaware.com/live/flight/{tail_number}/history"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    flight_history_response = requests.get(flight_history_url, headers=headers)
    
    if flight_history_response.status_code != 200:
        print(f"Failed to retrieve flight history from {flight_history_url}")
        return None
    
    flight_soup = BeautifulSoup(flight_history_response.text, 'html.parser')
    
    flight_rows = flight_soup.find_all('tr', class_='smallActiverow1')
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