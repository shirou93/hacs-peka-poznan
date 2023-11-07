Integracja HACS pobierająca saldo poznańskiej tPortmonetki.


Repozytorium trzeba dodać w HACS>Integracje>Niestandardowe Repozytoria wklejając tam link: https://github.com/shirou93/hacs-peka-poznan

Ważne: Nie używamy cudzysłowów w konfiguracji sensorów.


Przykład konfiguracji:

```
sensor:
  - platform: peka_tportmonetka
    sensors:
      - name: Peka TPortMonetka Sensor 1
        login: login
        password: password
        scan_interval:
          minutes: 60
      - name: Peka TPortMonetka Sensor 2
        login: login
        password: password
        scan_interval:
          minutes: 30

```
W przypadku wskazania 0PLN trzeba sprawdzić czy nie ma czasem założonego na profilu capcha. 
Jeśli jest trzeba je rozwiązać. Sensor przy następnej aktualizacji powinien zacząć ponownie pobierać saldo.