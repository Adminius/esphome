from typing import Any

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.const import CONF_ID, PLATFORM_ESP32, PLATFORM_ESP8266
from . import generate

CODEOWNERS = ["@olegtarasov"]
MULTI_CONF = True

CONF_IN_PIN = "in_pin"
CONF_OUT_PIN = "out_pin"
CONF_CH_ENABLE = "ch_enable"
CONF_DHW_ENABLE = "dhw_enable"
CONF_COOLING_ENABLE = "cooling_enable"
CONF_OTC_ACTIVE = "otc_active"
CONF_CH2_ACTIVE = "ch2_active"
CONF_SUMMER_MODE_ACTIVE = "summer_mode_active"
CONF_DHW_BLOCK = "dhw_block"
CONF_SYNC_MODE = "sync_mode"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(generate.OpenthermHub),
            cv.Required(CONF_IN_PIN): pins.internal_gpio_input_pin_schema,
            cv.Required(CONF_OUT_PIN): pins.internal_gpio_output_pin_schema,
            cv.Optional(CONF_CH_ENABLE, True): cv.boolean,
            cv.Optional(CONF_DHW_ENABLE, True): cv.boolean,
            cv.Optional(CONF_COOLING_ENABLE, False): cv.boolean,
            cv.Optional(CONF_OTC_ACTIVE, False): cv.boolean,
            cv.Optional(CONF_CH2_ACTIVE, False): cv.boolean,
            cv.Optional(CONF_SUMMER_MODE_ACTIVE, False): cv.boolean,
            cv.Optional(CONF_DHW_BLOCK, False): cv.boolean,
            cv.Optional(CONF_SYNC_MODE, False): cv.boolean,
        }
    ).extend(cv.COMPONENT_SCHEMA),
    cv.only_on([PLATFORM_ESP32, PLATFORM_ESP8266]),
)


async def to_code(config: dict[str, Any]) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # Set pins
    in_pin = await cg.gpio_pin_expression(config[CONF_IN_PIN])
    cg.add(var.set_in_pin(in_pin))

    out_pin = await cg.gpio_pin_expression(config[CONF_OUT_PIN])
    cg.add(var.set_out_pin(out_pin))

    non_sensors = {CONF_ID, CONF_IN_PIN, CONF_OUT_PIN}
    for key, value in config.items():
        if key in non_sensors:
            continue

        cg.add(getattr(var, f"set_{key}")(value))