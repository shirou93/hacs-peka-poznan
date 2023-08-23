Integracja HACS pobierająca saldo poznańskiej tPortmonetki.


Repozytorium trzeba dodać w HACS>Integracje>Niestandardowe Repozytoria wklejąc tam link: https://github.com/shirou93/hacs-peka-poznan

Przykład konfiguracji:

```
sensor:
  - platform: peka_tportmonetka
    sensors:
      - name: Peka TPortMonetka Sensor 2
        login: 'login'
        password: 'password'
        scan_interval:
          minutes: 60
      - name: Peka TPortMonetka Sensor 2
        login: 'login'
        password: 'password'
        scan_interval:
          minutes: 30

```