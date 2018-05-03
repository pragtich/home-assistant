"""Tests for MySensors config flow."""
from unittest.mock import patch

from homeassistant.components.mysensors import config_flow, const


async def test_user_serial_flow(hass):
    """Test config flow for serial gateway started by user."""
    flow = config_flow.MySensorsFlowHandler()
    flow.hass = hass
    result = await flow.async_step_init()

    assert result['type'] == 'form'
    assert result['step_id'] == 'init'
    assert result['data_schema'] == const.SELECT_GATEWAY_SCHEMA
    assert result['errors'] == {}

    user_input = {'gateway_type': 'serial'}
    result = await flow.async_step_init(user_input)

    assert result['type'] == 'form'
    assert result['step_id'] == 'configure_gateway'
    assert result['data_schema'] == const.SERIAL_GATEWAY_SCHEMA
    assert result['errors'] == {}

    user_input = {'device': 'test/port'}
    with patch('homeassistant.components.mysensors.'
               'config_flow.is_serial_port') as mock_is_serial:
        mock_is_serial.return_value = 'test/port'
        result = await flow.async_step_configure_gateway(user_input)

    assert result['type'] == 'create_entry'
    assert result['title'] == "MySensors gateway: test/port"
    assert result['data'] == {
        'gateway': {
            'gateway_type': 'serial',
            'device': 'test/port',
            'baud_rate': 115200,
            'nodes': {},
            'optimistic': False,
            'retain': True,
            'tcp_port': 5003,
            'version': '1.4',
        }
    }
