Przyklad konfiguracji:

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