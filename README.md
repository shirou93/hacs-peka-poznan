Integracja HACS pobierajaca slado poznańskiej tPortmonetki.


Repozytorium trzeba dodać w HACS>Integracje>Niestandardowe Repozytoria wklejąc tam link: https://github.com/shirou93/hacs-peka-poznan

Przykład konfiguracji:

```
peka_tportmonetka:
  - name: Peka TPort Monetka Sensor 1
    login: your_username_1
    password: your_password_1
    scan_interval:
      hours: 1

  - name: Peka TPort Monetka Sensor 2
    login: your_username_2
    password: your_password_2
    scan_interval:
      hours: 2

```