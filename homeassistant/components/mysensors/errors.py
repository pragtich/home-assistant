"""Errors for the MySensors component."""
from homeassistant.exceptions import HomeAssistantError


class ValidationError(HomeAssistantError):
    """Voluptuous error for invalid persistence file."""


class PersistenceFileInvalid(ValidationError):
    """Voluptuous error for invalid persistence file."""


class SerialPortInvalid(ValidationError):
    """Voluptuous error for invalid serial port."""


class SocketInvalid(ValidationError):
    """Voluptuous error for invalid socket address."""
