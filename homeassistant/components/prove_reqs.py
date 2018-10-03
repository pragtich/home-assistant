"""Prove that requirements are not available at the module level."""
from homeassistant.helpers.discovery import load_platform

REQUIREMENTS = ['pandas']
DOMAIN = 'prove_reqs'


def setup(hass, config):
    """Your controller/hub specific code."""
    load_platform(hass, 'sensor', DOMAIN)

    return True
