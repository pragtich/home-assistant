"""
Component to interface with u2f-client in the frontend.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/u2f/
"""
import logging

from aiohttp import web

from homeassistant.components.http import HomeAssistantView

REQUIREMENTS = ['python-u2flib-server']

_LOGGER = logging.getLogger(__name__)
REGISTERED_DEVICES = 'registered_devices'
REGISTRATION_INFO = 'registration_info'
CHALLENGE = 'challenge'


async def async_setup(hass, config):
    """Set up the u2f component."""
    hass.http.register_view(U2FEnroll())

    return True


class U2FView(HomeAssistantView):
    """Base U2FView."""

    def __init__(self):
        """Initialize U2F view."""
        self.facet = ''  # FIX THIS!!!
        self.app_id = self.facet
        self.users = {}

    async def get(self, request):
        """Start a get request."""
        response = await self.handle(request)
        return response

    async def handle(self, request):
        """Handle the u2f request."""
        raise NotImplementedError()

    async def start_registration(self, username):
        """Start registration of a u2f key."""
        from u2flib_server.u2f import begin_registration
        if username not in self.users:
            self.users[username] = {}

        user = self.users[username]
        reg = begin_registration(self.app_id, user.get(REGISTERED_DEVICES, []))
        user[REGISTRATION_INFO] = reg.json
        return self.json(reg.data_for_client)

    async def finish_registration(self, username, data):
        """Finish registration of a u2f key."""
        from u2flib_server.u2f import complete_registration
        from cryptography import x509
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.serialization import Encoding
        user = self.users[username]
        device, cert = complete_registration(
            user.pop(REGISTRATION_INFO), data, [self.facet])
        user.setdefault(REGISTERED_DEVICES, []).append(device.json)

        _LOGGER.info('U2F device registered, username: %s', username)
        cert = x509.load_der_x509_certificate(cert, default_backend())
        _LOGGER.debug(
            'Attestation certificate:\n%s', cert.public_bytes(Encoding.PEM))

        return self.json(True)

    async def start_authentication(self, username):
        """Start authentication of a u2f key."""
        from u2flib_server.u2f import begin_authentication
        user = self.users.get(username)
        if not user:
            return web.Response(status=401)
        challenge = begin_authentication(
            self.app_id, user.get(REGISTERED_DEVICES, []))
        user[CHALLENGE] = challenge.json
        return self.json(challenge.data_for_client)

    async def finish_authentication(self, username, data):
        """Finish authentication of a u2f key."""
        from u2flib_server.u2f import complete_authentication
        user = self.users[username]
        challenge = user.pop(CHALLENGE)
        device, count, touch = complete_authentication(
            challenge, data, [self.facet])
        return self.json({
            'keyHandle': device['keyHandle'], 'touch': touch,
            'counter': count})


class U2FEnroll(U2FView):
    """U2FView to enroll a u2f key."""

    url = '/api/u2f/enroll'
    name = 'api:u2f:enroll'

    async def handle(self, request):
        """Start enrolling a u2f key."""
        username = request.params.get('username')
        # data = request.params.get('data', None)
        if not username:
            return web.Response(status=401)
