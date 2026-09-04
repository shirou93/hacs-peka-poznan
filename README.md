Integracja HACS pobierająca saldo poznańskiej tPortmonetki.

Po instalacji przez HACS dodaj integrację w **Ustawienia > Urządzenia i usługi > Dodaj integrację** i wyszukaj **PEKA tPortmonetka**. Login, hasło, nazwa sensora oraz częstotliwość odświeżania są wpisywane w GUI Home Assistanta. Integracja nie korzysta z konfiguracji YAML.

Repozytorium trzeba dodać w HACS>Integracje>Niestandardowe Repozytoria wklejając tam link: https://github.com/shirou93/hacs-peka-poznan

W przypadku błędów z dodaniem konta należy sprawdzić czy nie ma czasem założonego na profilu capcha. 
Jeśli jest, trzeba ją rozwiązać. Po zalogowaniu się z capcha dodanie konta powinno się powieść.

Migracja ze starej wersji musi zostać wykonana ręcznie tj. Trzeba usunąć wpisy YAML, a następnie dodać ponownie w GUI.