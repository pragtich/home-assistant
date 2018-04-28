"""Config flow to configure MySensors gateways."""
import asyncio

from homeassistant import config_entries, data_entry_flow

from .const import (
    CONF_DEVICE, CONF_GATEWAY_TYPE, CONF_MQTT, CONF_TOPIC_IN_PREFIX, DOMAIN,
    ENTRY_GATEWAY, GATEWAY_SCHEMAS, SELECT_GATEWAY_SCHEMA)


@config_entries.HANDLERS.register(DOMAIN)
class MySensorsFlowHandler(data_entry_flow.FlowHandler):
    """Handle a MySensors config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize MySensors configuration flow."""
        self._gateway_schema = None
        self._gateway_type = None

    async def async_step_init(self, user_input=None):
        """Handle a flow start."""
        errors = {}
        if user_input is not None:
            gateway_type = user_input[CONF_GATEWAY_TYPE]
            self._gateway_type = gateway_type
            self._gateway_schema = GATEWAY_SCHEMAS[gateway_type]
            return await self.async_step_configure_gateway()

        return self.async_show_form(
            step_id='init',
            data_schema=SELECT_GATEWAY_SCHEMA,
            errors=errors,
        )

    async def async_step_configure_gateway(self, user_input=None):
        """Show form to user to configure gateway."""
        errors = {}
        if user_input is not None:
            return await self._create_entry(user_input)

        return self.async_show_form(
            step_id='configure_gateway',
            data_schema=self._gateway_schema,
            errors=errors,
        )

    async def async_step_import(self, import_info):
        """Import a new gateway as a config entry."""
        gateway_conf = import_info[ENTRY_GATEWAY]
        return await self._create_entry(gateway_conf)

    async def _create_entry(self, gateway_conf):
        """Return a config entry from a gateway config."""
        # Remove all other entries of gateways with same config.
        if self._gateway_type == CONF_MQTT:
            gateway_conf[CONF_DEVICE] = CONF_MQTT
        gateway_conf[CONF_GATEWAY_TYPE] = gateway_conf.get(
            CONF_GATEWAY_TYPE, self._gateway_type)
        same_entries = [
            entry.entry_id for entry
            in self.hass.config_entries.async_entries(DOMAIN)
            if entry.data[ENTRY_GATEWAY][CONF_DEVICE] == CONF_MQTT and
            entry.data[ENTRY_GATEWAY][CONF_TOPIC_IN_PREFIX] ==
            gateway_conf.get(CONF_TOPIC_IN_PREFIX) or
            entry.data[ENTRY_GATEWAY][CONF_DEVICE] != CONF_MQTT and
            entry.data[ENTRY_GATEWAY][CONF_DEVICE] ==
            gateway_conf[CONF_DEVICE]]

        if same_entries:
            await asyncio.wait([
                self.hass.config_entries.async_remove(entry_id)
                for entry_id in same_entries])

        return self.async_create_entry(
            title="MySensors gateway: {}".format(gateway_conf[CONF_DEVICE]),
            data={
                ENTRY_GATEWAY: gateway_conf,
            }
        )
