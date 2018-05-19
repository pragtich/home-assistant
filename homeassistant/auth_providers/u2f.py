"""Home Assistant auth provider."""
from collections import OrderedDict

import voluptuous as vol

from homeassistant import auth, data_entry_flow

from .homeassistant import HassAuthProvider, InvalidAuth

CONFIG_SCHEMA = auth.AUTH_PROVIDER_SCHEMA.extend({
}, extra=vol.PREVENT_EXTRA)


@auth.AUTH_PROVIDERS.register('u2f')
class U2FAuthProvider(HassAuthProvider):
    """Auth provider based on a local storage of users in HASS config dir."""

    DEFAULT_TITLE = 'Home Assistant U2F'


class LoginFlow(data_entry_flow.FlowHandler):
    """Handler for the login flow."""

    def __init__(self, auth_provider):
        """Initialize the login flow."""
        self._auth_provider = auth_provider

    async def async_step_init(self, user_input=None):
        """Handle the step of the form."""
        errors = {}

        if user_input is not None:
            try:
                await self._auth_provider.async_validate_login(
                    user_input['username'], user_input['password'])
            except InvalidAuth:
                errors['base'] = 'invalid_auth'

            if not errors:
                return self.async_create_entry(
                    title=self._auth_provider.name,
                    data=user_input
                )

        schema = OrderedDict()
        schema['username'] = str
        schema['password'] = str

        return self.async_show_form(
            step_id='init',
            data_schema=vol.Schema(schema),
            errors=errors,
        )
