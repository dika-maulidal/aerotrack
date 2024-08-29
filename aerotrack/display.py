def display_data(data, soup):
    # Menampilkan informasi pesawat
    print(f"\n\033[1mAircraft Information\033[0m")
    
    for key, value in data.items():
        print(f"{key}: {value}")
    
    # Mengambil dan menampilkan Registration History
    print("\n\033[1mRegistration History\033[0m")
    history_rows = soup.find_all('tr', class_=['row1', 'row2'])
    
    if history_rows:
        # Menampilkan header tabel
        print(f"\033[97m{'Date':<20} {'Owner':<30} {'Location'}\033[0m")
        print("\033[97m" + "-" * 70 + "\033[0m")
        
        for row in history_rows:
            columns = row.find_all('td')
            if len(columns) == 3:
                date = columns[0].get_text(strip=True)
                owner = columns[1].get_text(strip=True)
                location = columns[2].get_text(strip=True)
                # Menampilkan data dengan warna biru muda
                print(f"\033[94m{date:<20} {owner:<30} {location}\033[0m")
    else:
        print("\033[97mNo registration history found.\033[0m")