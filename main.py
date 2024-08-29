# ======================
# make by Dika Maulidal.
# ======================

from aerotrack.ascii_art import display_ascii_art
from aerotrack.scraper import scrape_registration_data

def main():
    display_ascii_art()
    tail_number = input("\033[96mEnter the tail number: \033[0m")
    scrape_registration_data(tail_number)

if __name__ == "__main__":
    main()