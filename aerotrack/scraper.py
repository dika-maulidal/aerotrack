import requests
from bs4 import BeautifulSoup
from aerotrack.display import display_data

def scrape_registration_data(tail_number):
    flightaware_url = f"https://www.flightaware.com/resources/registration/{tail_number}"
    faa_url = f"https://registry.faa.gov/AircraftInquiry/Search/NNumberResult?nNumberTxt={tail_number}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Mengambil data dari FlightAware
    flightaware_response = requests.get(flightaware_url, headers=headers)
    if flightaware_response.status_code != 200:
        print(f"Failed to retrieve data from {flightaware_url}")
        return None
    
    soup = BeautifulSoup(flightaware_response.text, 'html.parser')
    data = {}
    
    # Mengambil data atribut registrasi
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
    
    # Mengambil data dari FAA
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
    
    display_data(data, soup)
