"""
Support for MySensors locks.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/lock.mysensors/
"""
import logging

from homeassistant.components import mysensors
from homeassistant.components.lock import LockDevice
from homeassistant.const import STATE_OFF, STATE_ON

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the mysensors platform for locks."""
    # Only act if loaded via mysensors by discovery event.
    # Otherwise gateway is not setup.
    if discovery_info is None:
        return

    for gateway in mysensors.GATEWAYS.values():
        # Define the S_TYPES and V_TYPES that the platform should handle as
        # states. Map them in a dict of lists.
        pres = gateway.const.Presentation
        set_req = gateway.const.SetReq
        map_sv_types = {
            pres.S_LOCK: [set_req.V_LOCK_STATUS],
        }

        devices = {}
        gateway.platform_callbacks.append(mysensors.pf_callback_factory(
            map_sv_types, devices, add_devices, MySensorsLock))


class MySensorsLock(mysensors.MySensorsDeviceEntity, LockDevice):
    """Representation of the value of a MySensors Lock child node."""

    @property
    def assumed_state(self):
        """Return True if unable to access real state of entity."""
        return self.gateway.optimistic

    @property
    def is_locked(self):
        """Return true if the lock is locked."""
        if self.value_type in self._values:
            return self._values[self.value_type] == STATE_ON
        return False

    def lock(self, **kwargs):
        """Lock the lock."""
        self.gateway.set_child_value(
            self.node_id, self.child_id, self.value_type, 1)
        if self.gateway.optimistic:
            # optimistically assume that lock has changed state
            self._values[self.value_type] = STATE_ON
            self.update_ha_state()

    def unlock(self, **kwargs):
        """Unlock the lock."""
        self.gateway.set_child_value(
            self.node_id, self.child_id, self.value_type, 0)
        if self.gateway.optimistic:
            # optimistically assume that lock has changed state
            self._values[self.value_type] = STATE_OFF
            self.update_ha_state()
