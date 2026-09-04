"""Client for the PEKA online account API."""

from __future__ import annotations

import aiohttp

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_LOGIN, CONF_PASSWORD

LOGIN_URL = "https://www.peka.poznan.pl/sop/authenticate?lang=pl"
CARDS_URL = "https://www.peka.poznan.pl/sop/account/cards?lang=pl"


class PekaApiError(Exception):
    """Raised when PEKA cannot return a balance."""


async def async_get_balance(hass, data: dict[str, str]) -> float:
    """Authenticate and return the first tPortmonetka balance."""
    session = async_get_clientsession(hass)

    try:
        async with session.post(
            LOGIN_URL,
            json={"username": data[CONF_LOGIN], "password": data[CONF_PASSWORD]},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as response:
            response.raise_for_status()
            login_data = await response.json()
            token = login_data.get("data")
            if not token:
                raise PekaApiError("Invalid PEKA credentials")

        async with session.get(
            CARDS_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as response:
            response.raise_for_status()
            cards_data = await response.json()

        return float(cards_data["data"][0]["tpurse"]["balance"])
    except (aiohttp.ClientError, KeyError, IndexError, TypeError, ValueError) as err:
        raise PekaApiError("Unable to read the PEKA balance") from err