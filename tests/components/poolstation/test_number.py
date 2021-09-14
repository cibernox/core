"""Tests for the Poolstation sensor platform."""
from homeassistant.components.number.const import ATTR_VALUE, DOMAIN, SERVICE_SET_VALUE
from homeassistant.components.poolstation.number import (
    TARGET_ELECTROLYSIS_SUFFIX,
    TARGET_PH_SUFFIX,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_ICON,
    ATTR_UNIT_OF_MEASUREMENT,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry

from .common import init_integration, mock_config_entry, mock_pool

ENTITY_TARGET_PH = "number.home_target_ph"
ENTITY_TARGET_ELECTROLYSIS = "number.home_target_production"


async def test_read_pool_numbers(hass: HomeAssistant) -> None:
    """Test creating and reading Poolstation numbers."""
    config_entry = mock_config_entry(uniqe_id="id_123_sensor_test_pool")
    pool = mock_pool(id=123)
    await init_integration(hass, config_entry, [pool])
    registry = entity_registry.async_get(hass)

    # PH
    state = hass.states.get(ENTITY_TARGET_PH)
    assert state
    assert state.state == str(pool.target_ph)
    assert state.attributes.get(ATTR_ICON) == "mdi:gauge"
    entry = registry.async_get(ENTITY_TARGET_PH)
    assert entry
    assert entry.unique_id == f"{pool.alias}{TARGET_PH_SUFFIX}"

    # Electrolysis
    state = hass.states.get(ENTITY_TARGET_ELECTROLYSIS)
    assert state
    assert state.state == str(pool.target_percentage_electrolysis)
    assert state.attributes.get(ATTR_ICON) == "mdi:gauge"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == PERCENTAGE
    entry = registry.async_get(ENTITY_TARGET_ELECTROLYSIS)
    assert entry
    assert entry.unique_id == f"{pool.alias}{TARGET_ELECTROLYSIS_SUFFIX}"


async def test_write_pool_numbers(hass: HomeAssistant) -> None:
    """Test updating Poolstation numbers."""
    config_entry = mock_config_entry(uniqe_id="id_123_number_test_pool")
    pool = mock_pool(id=123)
    await init_integration(hass, config_entry, [pool])

    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: ENTITY_TARGET_PH, ATTR_VALUE: 7.41},
        blocking=True,
    )
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_TARGET_PH)
    assert state
    assert state.state == "7.41"

    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: ENTITY_TARGET_ELECTROLYSIS, ATTR_VALUE: 65},
        blocking=True,
    )
    await hass.async_block_till_done()
    state = hass.states.get(ENTITY_TARGET_ELECTROLYSIS)
    assert state
    assert state.state == "65"
