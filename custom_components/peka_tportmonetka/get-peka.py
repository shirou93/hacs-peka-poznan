#!/usr/bin/python3
import requests
import json
import sys

def peka_balance(login,password):
    #rozpoczenie sesji
    session = requests.Session()
    login=f"{login}"
    password=f"{password}"
    login_payload = {
        "password": password,
        "username": login
    }

    # URL logowania
    login_url = "https://www.peka.poznan.pl/sop/authenticate?lang=pl"

    # Wysyłanie żądania logowania
    response = session.post(login_url, json=login_payload)

    # Sprawdzenie odpowiedzi serwera
    if response.status_code == 200:
        access_token = json.loads(response.text)["data"]
        get_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        session.headers.update(get_headers)
        get_url = "https://www.peka.poznan.pl/sop/account/cards?lang=pl&t=1692522853"
        get_response = session.get(get_url)
        
        if get_response.status_code == 200:
            # Wyświetlenie danych
            data = get_response.json()
            balance = data['data'][0]['tpurse']['balance']
            print(balance)
    session.close()
if __name__ == "__main__":
    try:
        peka_balance(sys.argv[1],sys.argv[2])
    except:
        sys.exit()