"""MySensors constants."""
import voluptuous as vol

from homeassistant.components.mqtt import (
    valid_publish_topic, valid_subscribe_topic)
from homeassistant.const import CONF_OPTIMISTIC
import homeassistant.helpers.config_validation as cv

from .errors import PersistenceFileInvalid

ATTR_DEVICES = 'devices'

CONF_BAUD_RATE = 'baud_rate'
CONF_DEVICE = 'device'
CONF_GATEWAYS = 'gateways'
CONF_GATEWAY_TYPE = 'gateway_type'
CONF_MQTT = 'mqtt'
CONF_SERIAL = 'serial'
CONF_TCP = 'tcp'
CONF_NODE_NAME = 'name'
CONF_NODES = 'nodes'
CONF_PERSISTENCE_FILE = 'persistence_file'
CONF_RETAIN = 'retain'
CONF_TCP_PORT = 'tcp_port'
CONF_TOPIC_IN_PREFIX = 'topic_in_prefix'
CONF_TOPIC_OUT_PREFIX = 'topic_out_prefix'
CONF_VERSION = 'version'

DEFAULT_BAUD_RATE = 115200
DEFAULT_TCP_PORT = 5003
DEFAULT_VERSION = '1.4'
DOMAIN = 'mysensors'
ENTRY_GATEWAY = 'gateway'
MQTT_COMPONENT = 'mqtt'
MYSENSORS_GATEWAYS = 'mysensors_gateways'
PLATFORM = 'platform'
SCHEMA = 'schema'
SIGNAL_CALLBACK = 'mysensors_callback_{}_{}_{}_{}'
TYPE = 'type'


def is_persistence_file(value):
    """Validate that persistence file path ends in either .pickle or .json."""
    if value.endswith(('.json', '.pickle')):
        return value
    else:
        raise PersistenceFileInvalid(
            '{} does not end in either `.json` or `.pickle`'.format(value))


NODE_SCHEMA = vol.Schema({
    cv.positive_int: {
        vol.Required(CONF_NODE_NAME): cv.string
    }
})

COMMON_GATEWAY_SCHEMA = vol.Schema({
    vol.Optional(CONF_OPTIMISTIC, default=False): vol.Coerce(bool),
    vol.Optional(CONF_PERSISTENCE_FILE): str,
    vol.Optional(CONF_VERSION, default=DEFAULT_VERSION): vol.Coerce(str),
})

SELECT_GATEWAY_SCHEMA = vol.Schema({
    vol.Required(CONF_GATEWAY_TYPE):
        vol.In([CONF_MQTT, CONF_SERIAL, CONF_TCP]),
})

GATEWAY_SCHEMA = SELECT_GATEWAY_SCHEMA.extend({
    vol.Optional(CONF_BAUD_RATE, default=DEFAULT_BAUD_RATE):
        cv.positive_int,
    vol.Required(CONF_DEVICE): cv.string,
    vol.Optional(CONF_NODES, default={}): NODE_SCHEMA,
    vol.Optional(CONF_OPTIMISTIC, default=False): cv.boolean,
    vol.Optional(CONF_PERSISTENCE_FILE):
        vol.All(cv.string, is_persistence_file),
    vol.Optional(CONF_RETAIN, default=True): cv.boolean,
    vol.Optional(CONF_TCP_PORT, default=DEFAULT_TCP_PORT): cv.port,
    vol.Optional(CONF_TOPIC_IN_PREFIX): valid_subscribe_topic,
    vol.Optional(CONF_TOPIC_OUT_PREFIX): valid_publish_topic,
    vol.Optional(CONF_VERSION, default=DEFAULT_VERSION): cv.string,
})

MQTT_GATEWAY_SCHEMA = COMMON_GATEWAY_SCHEMA.extend({
    vol.Optional(CONF_RETAIN, default=True): vol.Coerce(bool),
    vol.Optional(CONF_TOPIC_IN_PREFIX): str,
    vol.Optional(CONF_TOPIC_OUT_PREFIX): str,
})

SERIAL_GATEWAY_SCHEMA = COMMON_GATEWAY_SCHEMA.extend({
    vol.Required(CONF_DEVICE): str,
    vol.Optional(CONF_BAUD_RATE, default=DEFAULT_BAUD_RATE): cv.positive_int,
})

TCP_GATEWAY_SCHEMA = COMMON_GATEWAY_SCHEMA.extend({
    vol.Required(CONF_DEVICE): str,
    vol.Optional(CONF_TCP_PORT, default=DEFAULT_TCP_PORT): vol.Coerce(int),
})

GATEWAY_SCHEMAS = {
    CONF_MQTT: MQTT_GATEWAY_SCHEMA,
    CONF_SERIAL: SERIAL_GATEWAY_SCHEMA,
    CONF_TCP: TCP_GATEWAY_SCHEMA,
}

# MySensors const schemas
BINARY_SENSOR_SCHEMA = {PLATFORM: 'binary_sensor', TYPE: 'V_TRIPPED'}
CLIMATE_SCHEMA = {PLATFORM: 'climate', TYPE: 'V_HVAC_FLOW_STATE'}
LIGHT_DIMMER_SCHEMA = {
    PLATFORM: 'light', TYPE: 'V_DIMMER',
    SCHEMA: {'V_DIMMER': cv.string, 'V_LIGHT': cv.string}}
LIGHT_PERCENTAGE_SCHEMA = {
    PLATFORM: 'light', TYPE: 'V_PERCENTAGE',
    SCHEMA: {'V_PERCENTAGE': cv.string, 'V_STATUS': cv.string}}
LIGHT_RGB_SCHEMA = {
    PLATFORM: 'light', TYPE: 'V_RGB', SCHEMA: {
        'V_RGB': cv.string, 'V_STATUS': cv.string}}
LIGHT_RGBW_SCHEMA = {
    PLATFORM: 'light', TYPE: 'V_RGBW', SCHEMA: {
        'V_RGBW': cv.string, 'V_STATUS': cv.string}}
NOTIFY_SCHEMA = {PLATFORM: 'notify', TYPE: 'V_TEXT'}
DEVICE_TRACKER_SCHEMA = {PLATFORM: 'device_tracker', TYPE: 'V_POSITION'}
DUST_SCHEMA = [
    {PLATFORM: 'sensor', TYPE: 'V_DUST_LEVEL'},
    {PLATFORM: 'sensor', TYPE: 'V_LEVEL'}]
SWITCH_LIGHT_SCHEMA = {PLATFORM: 'switch', TYPE: 'V_LIGHT'}
SWITCH_STATUS_SCHEMA = {PLATFORM: 'switch', TYPE: 'V_STATUS'}
MYSENSORS_CONST_SCHEMA = {
    'S_DOOR': [BINARY_SENSOR_SCHEMA, {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_MOTION': [BINARY_SENSOR_SCHEMA, {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_SMOKE': [BINARY_SENSOR_SCHEMA, {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_SPRINKLER': [
        BINARY_SENSOR_SCHEMA, {PLATFORM: 'switch', TYPE: 'V_STATUS'}],
    'S_WATER_LEAK': [
        BINARY_SENSOR_SCHEMA, {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_SOUND': [
        BINARY_SENSOR_SCHEMA, {PLATFORM: 'sensor', TYPE: 'V_LEVEL'},
        {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_VIBRATION': [
        BINARY_SENSOR_SCHEMA, {PLATFORM: 'sensor', TYPE: 'V_LEVEL'},
        {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_MOISTURE': [
        BINARY_SENSOR_SCHEMA, {PLATFORM: 'sensor', TYPE: 'V_LEVEL'},
        {PLATFORM: 'switch', TYPE: 'V_ARMED'}],
    'S_HVAC': [CLIMATE_SCHEMA],
    'S_COVER': [
        {PLATFORM: 'cover', TYPE: 'V_DIMMER'},
        {PLATFORM: 'cover', TYPE: 'V_PERCENTAGE'},
        {PLATFORM: 'cover', TYPE: 'V_LIGHT'},
        {PLATFORM: 'cover', TYPE: 'V_STATUS'}],
    'S_DIMMER': [LIGHT_DIMMER_SCHEMA, LIGHT_PERCENTAGE_SCHEMA],
    'S_RGB_LIGHT': [LIGHT_RGB_SCHEMA],
    'S_RGBW_LIGHT': [LIGHT_RGBW_SCHEMA],
    'S_INFO': [NOTIFY_SCHEMA, {PLATFORM: 'sensor', TYPE: 'V_TEXT'}],
    'S_GPS': [
        DEVICE_TRACKER_SCHEMA, {PLATFORM: 'sensor', TYPE: 'V_POSITION'}],
    'S_TEMP': [{PLATFORM: 'sensor', TYPE: 'V_TEMP'}],
    'S_HUM': [{PLATFORM: 'sensor', TYPE: 'V_HUM'}],
    'S_BARO': [
        {PLATFORM: 'sensor', TYPE: 'V_PRESSURE'},
        {PLATFORM: 'sensor', TYPE: 'V_FORECAST'}],
    'S_WIND': [
        {PLATFORM: 'sensor', TYPE: 'V_WIND'},
        {PLATFORM: 'sensor', TYPE: 'V_GUST'},
        {PLATFORM: 'sensor', TYPE: 'V_DIRECTION'}],
    'S_RAIN': [
        {PLATFORM: 'sensor', TYPE: 'V_RAIN'},
        {PLATFORM: 'sensor', TYPE: 'V_RAINRATE'}],
    'S_UV': [{PLATFORM: 'sensor', TYPE: 'V_UV'}],
    'S_WEIGHT': [
        {PLATFORM: 'sensor', TYPE: 'V_WEIGHT'},
        {PLATFORM: 'sensor', TYPE: 'V_IMPEDANCE'}],
    'S_POWER': [
        {PLATFORM: 'sensor', TYPE: 'V_WATT'},
        {PLATFORM: 'sensor', TYPE: 'V_KWH'},
        {PLATFORM: 'sensor', TYPE: 'V_VAR'},
        {PLATFORM: 'sensor', TYPE: 'V_VA'},
        {PLATFORM: 'sensor', TYPE: 'V_POWER_FACTOR'}],
    'S_DISTANCE': [{PLATFORM: 'sensor', TYPE: 'V_DISTANCE'}],
    'S_LIGHT_LEVEL': [
        {PLATFORM: 'sensor', TYPE: 'V_LIGHT_LEVEL'},
        {PLATFORM: 'sensor', TYPE: 'V_LEVEL'}],
    'S_IR': [
        {PLATFORM: 'sensor', TYPE: 'V_IR_RECEIVE'},
        {PLATFORM: 'switch', TYPE: 'V_IR_SEND',
         SCHEMA: {'V_IR_SEND': cv.string, 'V_LIGHT': cv.string}}],
    'S_WATER': [
        {PLATFORM: 'sensor', TYPE: 'V_FLOW'},
        {PLATFORM: 'sensor', TYPE: 'V_VOLUME'}],
    'S_CUSTOM': [
        {PLATFORM: 'sensor', TYPE: 'V_VAR1'},
        {PLATFORM: 'sensor', TYPE: 'V_VAR2'},
        {PLATFORM: 'sensor', TYPE: 'V_VAR3'},
        {PLATFORM: 'sensor', TYPE: 'V_VAR4'},
        {PLATFORM: 'sensor', TYPE: 'V_VAR5'},
        {PLATFORM: 'sensor', TYPE: 'V_CUSTOM'}],
    'S_SCENE_CONTROLLER': [
        {PLATFORM: 'sensor', TYPE: 'V_SCENE_ON'},
        {PLATFORM: 'sensor', TYPE: 'V_SCENE_OFF'}],
    'S_COLOR_SENSOR': [{PLATFORM: 'sensor', TYPE: 'V_RGB'}],
    'S_MULTIMETER': [
        {PLATFORM: 'sensor', TYPE: 'V_VOLTAGE'},
        {PLATFORM: 'sensor', TYPE: 'V_CURRENT'},
        {PLATFORM: 'sensor', TYPE: 'V_IMPEDANCE'}],
    'S_GAS': [
        {PLATFORM: 'sensor', TYPE: 'V_FLOW'},
        {PLATFORM: 'sensor', TYPE: 'V_VOLUME'}],
    'S_WATER_QUALITY': [
        {PLATFORM: 'sensor', TYPE: 'V_TEMP'},
        {PLATFORM: 'sensor', TYPE: 'V_PH'},
        {PLATFORM: 'sensor', TYPE: 'V_ORP'},
        {PLATFORM: 'sensor', TYPE: 'V_EC'},
        {PLATFORM: 'switch', TYPE: 'V_STATUS'}],
    'S_AIR_QUALITY': DUST_SCHEMA,
    'S_DUST': DUST_SCHEMA,
    'S_LIGHT': [SWITCH_LIGHT_SCHEMA],
    'S_BINARY': [SWITCH_STATUS_SCHEMA],
    'S_LOCK': [{PLATFORM: 'switch', TYPE: 'V_LOCK_STATUS'}],
}
