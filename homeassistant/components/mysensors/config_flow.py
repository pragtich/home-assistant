"""Config flow to configure MySensors gateways."""
import asyncio
import logging

import voluptuous as vol

from homeassistant import config_entries, data_entry_flow

from .const import (
    CONF_DEVICE, CONF_GATEWAY_TYPE, CONF_MQTT, CONF_PERSISTENCE_FILE,
    CONF_SERIAL, CONF_TCP, CONF_TOPIC_IN_PREFIX, DOMAIN, ENTRY_GATEWAY,
    GATEWAY_SCHEMA, GATEWAY_SCHEMAS, SELECT_GATEWAY_SCHEMA)
from .errors import PersistenceFileInvalid, SerialPortInvalid, SocketInvalid
from .gateway import is_serial_port, is_socket_address

_LOGGER = logging.getLogger(__name__)


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
            if self._gateway_type == CONF_MQTT:
                user_input[CONF_DEVICE] = CONF_MQTT
            user_input[CONF_GATEWAY_TYPE] = user_input.get(
                CONF_GATEWAY_TYPE, self._gateway_type)
            try:
                user_input = GATEWAY_SCHEMA(user_input)
                if self._gateway_type == CONF_SERIAL:
                    user_input[CONF_DEVICE] = await self.hass.async_add_job(
                        is_serial_port, user_input[CONF_DEVICE])
                if self._gateway_type == CONF_TCP:
                    user_input[CONF_DEVICE] = await self.hass.async_add_job(
                        is_socket_address, user_input[CONF_DEVICE])
            except PersistenceFileInvalid as exc:
                _LOGGER.warning("Invalid persistence file specified: %s", exc)
                errors[CONF_PERSISTENCE_FILE] = 'invalid_persistence_file'
            except SerialPortInvalid as exc:
                _LOGGER.warning("Invalid serial port specified: %s", exc)
                errors[CONF_DEVICE] = 'invalid_serial_port'
            except SocketInvalid as exc:
                _LOGGER.warning("Invalid socket specified: %s", exc)
                errors[CONF_DEVICE] = 'invalid_socket'
            except vol.Invalid as exc:
                _LOGGER.warning("Invalid config specified: %s", exc)
                errors['base'] = 'invalid_config'
            if not errors:
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
