# ======================
# make by Dika Maulidal.
# ======================

import os
from aerotrack.ascii_art import display_ascii_art
from aerotrack.scraper import scrape_registration_data, scrape_flight_history

def main():
    display_ascii_art()
    
    tail_number = input("\033[96mEnter the tail number: \033[0m").upper().strip()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    display_ascii_art()
    scrape_registration_data(tail_number)
    scrape_flight_history(tail_number)

if __name__ == "__main__":
    main()