"""Unit system helper class and methods."""

import logging
from numbers import Number

from typing import Optional, Dict

from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, LENGTH_CENTIMETERS, LENGTH_METERS,
    LENGTH_KILOMETERS, LENGTH_INCHES, LENGTH_FEET, LENGTH_YARD, LENGTH_MILES,
    VOLUME_LITERS, VOLUME_MILLILITERS, VOLUME_GALLONS, VOLUME_FLUID_OUNCE,
    MASS_GRAMS, MASS_KILOGRAMS, MASS_OUNCES, MASS_POUNDS,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL, LENGTH, MASS, VOLUME, TEMPERATURE,
    UNIT_NOT_RECOGNIZED_TEMPLATE)
from homeassistant.util import temperature as temperature_util
from homeassistant.util import distance as distance_util

_LOGGER = logging.getLogger(__name__)

TIME = 'time'
ELECTRIC_CURRENT = 'electric_current'
THERMODYNAMIC_TEMPERATURE = 'thermodynamic_temperature'
AMOUNT_OF_SUBSTANCE = 'amount_of_substance'
LUMINOUS_INTENSITY = 'luminous_intensity'
ANGLE = 'angle'
SOLID_ANGLE = 'solid_angle'
FREQUENCY = 'frequency'
FORCE = 'force'
PRESSURE = 'pressure'
ENERGY = 'energy'
POWER = 'power'
ELECTRIC_CHARGE = 'electric_charge'
VOLTAGE = 'voltage'
ELECTRIC_CAPACITANCE = 'electric_capacitance'
ELECTRIC_RESISTANCE = 'electric_resistance'
ELECTRICAL_CONDUCTANCE = 'electrical_conductance'
MAGNETIC_FLUX = 'magnetic_flux'
MAGNETIC_FLUX_DENSITY = 'magnetic_flux_density'
INDUCTANCE = 'inductance'
LUMINOUS_FLUX = 'luminous_flux'
ILLUMINANCE = 'illuminance'
RADIOACTIVITY = 'radioactivity'
ABSORBED_DOSE_RADIATION = 'absorbed_dose_radiation'
EQUIVALENT_DOSE_RADIATION = 'equivalent_dose_radiation'
CATALYTIC_ACTIVITY = 'catalytic_activity'
HUMIDITY = 'humidity'
BATTERY_LEVEL = 'battery_level'
STORAGE_USED = 'storage_used'
COUNT = 'count'
BANDWIDTH = 'bandwidth'
US_DOLLAR = 'us_dollar'
BITCOIN = 'bitcoin'
WIND_SPEED = 'wind_speed'
RAIN = 'rain'
VISIBILITY = 'visibility'

LENGTH_UNITS = [
    LENGTH_MILES,
    LENGTH_YARD,
    LENGTH_FEET,
    LENGTH_INCHES,
    LENGTH_KILOMETERS,
    LENGTH_METERS,
    LENGTH_CENTIMETERS,
]

MASS_UNITS = [
    MASS_POUNDS,
    MASS_OUNCES,
    MASS_KILOGRAMS,
    MASS_GRAMS,
]

VOLUME_UNITS = [
    VOLUME_GALLONS,
    VOLUME_FLUID_OUNCE,
    VOLUME_LITERS,
    VOLUME_MILLILITERS,
]

TEMPERATURE_UNITS = [
    TEMP_FAHRENHEIT,
    TEMP_CELSIUS,
]

METRIC_IMPERIAL_UNITS = {
    LENGTH: LENGTH_UNITS,
    TEMPERATURE: TEMPERATURE_UNITS,
    MASS: MASS_UNITS,
    VOLUME: VOLUME_UNITS,
}

SI_UNITS = {
    TIME: 's',
    ELECTRIC_CURRENT: 'A',
    THERMODYNAMIC_TEMPERATURE: 'K',
    AMOUNT_OF_SUBSTANCE: 'mol',
    LUMINOUS_INTENSITY: 'cd',
    ANGLE: 'rad',
    SOLID_ANGLE: 'sr',
    FREQUENCY: 'Hz',
    FORCE: 'N',
    PRESSURE: 'Pa',
    ENERGY: 'J',
    POWER: 'W',
    ELECTRIC_CHARGE: 'C',
    VOLTAGE: 'V',
    ELECTRIC_CAPACITANCE: 'F',
    ELECTRIC_RESISTANCE: 'Ω',
    ELECTRICAL_CONDUCTANCE: 'S',
    MAGNETIC_FLUX: 'Wb',
    MAGNETIC_FLUX_DENSITY: 'T',
    INDUCTANCE: 'H',
    LUMINOUS_FLUX: 'lm',
    ILLUMINANCE: 'lx',
    RADIOACTIVITY: 'Bq',
    ABSORBED_DOSE_RADIATION: 'Gy',
    EQUIVALENT_DOSE_RADIATION: 'Sv',
    CATALYTIC_ACTIVITY: 'kat',
}

COMPUTER_UNITS = {
    BATTERY_LEVEL: '%',
    STORAGE_USED: '%',
    COUNT: 'count',
    BANDWIDTH: 'Mb/s'  # type: str
}

WEATHER_UNITS = {
    HUMIDITY: '%',
    WIND_SPEED: 'm/s',
    RAIN: 'mm',
    VISIBILITY: 'km',
}

CURRENCY = {
    US_DOLLAR: 'USD',
    BITCOIN: 'BTC',
}


def is_valid_unit(
        unit: str, unit_type: str, unit_system: Optional[Dict]=None) -> bool:
    """Check if the unit is valid for it's type."""
    if unit_system is None:
        unit_system = METRIC_IMPERIAL_UNITS
    units = unit_system.get(unit_type)
    if units is None:
        return False
    if not isinstance(units, list):
        units = [units]
    return unit in units


class UnitSystem(object):
    """A container for units of measure."""

    def __init__(self: object, name: str, temperature: str, length: str,
                 volume: str, mass: str) -> None:
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, unit_type)
                      for unit, unit_type in [
                          (temperature, TEMPERATURE),
                          (length, LENGTH),
                          (volume, VOLUME),
                          (mass, MASS), ]
                      if not is_valid_unit(unit, unit_type))  # type: str

        if errors:
            raise ValueError(errors)

        self.name = name
        self.temperature_unit = temperature
        self.length_unit = length
        self.mass_unit = mass
        self.volume_unit = volume

    @property
    def is_metric(self: object) -> bool:
        """Determine if this is the metric unit system."""
        return self.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(self: object, temperature: float, from_unit: str) -> float:
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        from_unit, self.temperature_unit)

    def length(self: object, length: float, from_unit: str) -> float:
        """Convert the given length to this unit system."""
        if not isinstance(length, Number):
            raise TypeError('{} is not a numeric value.'.format(str(length)))

        return distance_util.convert(length, from_unit,
                                     self.length_unit)  # type: float

    def as_dict(self) -> dict:
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: self.length_unit,
            MASS: self.mass_unit,
            TEMPERATURE: self.temperature_unit,
            VOLUME: self.volume_unit
        }


METRIC_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
