"""Config flow for PoolStation integration."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientResponseError
from pypoolstation import Account  # , AuthenticationException
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, TOKEN

# from homeassistant.helpers.aiohttp_client import async_get_clientsession


_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Poolstation."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=DATA_SCHEMA, errors=errors
            )

        account = Account(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])

        try:
            _LOGGER.info("#### poolstation: About to attempt login!!!!")
            token = await account.login()
        except ClientResponseError:
            # errors["base"] = "cannot_connect"
            _LOGGER.info("#### poolstation: Login failed")
            errors[
                "base"
            ] = "invalid_auth"  # TODO: Not all errors should be considered auth errors
        # except AuthenticationException:
        #     errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            _LOGGER.info("#### poolstation: Login failed")
            _LOGGER.info(f"#### poolstation: user_input is {user_input}")
            await self.async_set_unique_id(user_input[CONF_EMAIL])
            self._abort_if_unique_id_configured()
            _LOGGER.info(f"#### poolstation: token is {token}")
            return self.async_create_entry(
                title=user_input[CONF_EMAIL],
                data={TOKEN: token},
            )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
