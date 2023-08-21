# hacs-peka-poznan
Integracja Home Assistant, która pobiera saldo poznańskiej tPortmonetki 

Przykład konfiguracji:

sensor:
  - platform: peka_tportmonetka
    sensors:
      - name: Peka TPortMonetka Sensor 2
        login: 'login'
        password: 'password'
        scan_interval:
          minutes: 60
      - name: Peka TPortMonetka Sensor 2
        login: 'natsumemidori15@gmail.com'
        password: 'Zaroweczka13'
        scan_interval:
          minutes: 30
		  
