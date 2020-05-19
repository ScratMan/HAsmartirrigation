"""Config flow for Smart Irrigation integration."""
import logging
import requests
import json
import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

from .OWMClient import OWMClient

from .const import (
    CONF_API_KEY,
    CONF_REFERENCE_ET,
    CONF_REFERENCE_ET_1,
    CONF_REFERENCE_ET_2,
    CONF_REFERENCE_ET_3,
    CONF_REFERENCE_ET_4,
    CONF_REFERENCE_ET_5,
    CONF_REFERENCE_ET_6,
    CONF_REFERENCE_ET_7,
    CONF_REFERENCE_ET_8,
    CONF_REFERENCE_ET_9,
    CONF_REFERENCE_ET_10,
    CONF_REFERENCE_ET_11,
    CONF_REFERENCE_ET_12,
    CONF_NUMBER_OF_SPRINKLERS,
    CONF_FLOW,
    CONF_AREA,
    DOMAIN,
    PLATFORMS,
    NAME,
)


class SmartIrrigationConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Irrigation."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._api_key = None
        self._reference_et = {}
        self._errors = {}

    async def async_step_step3(self, user_input=None):
        """Handle a flow step3."""
        self._errors = {}

        # only a single instance is allowed
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            user_input[CONF_API_KEY] = self._api_key
            user_input[CONF_REFERENCE_ET] = self._reference_et
            return self.async_create_entry(title=NAME, data=user_input)
        return await self._show_config_form(user_input)

    async def async_step_step2(self, user_input=None):
        """Handle a flow step2."""
        self._errors = {}

        # only a single instance is allowed
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            reference_et = [
                user_input[CONF_REFERENCE_ET_1],
                user_input[CONF_REFERENCE_ET_2],
                user_input[CONF_REFERENCE_ET_3],
                user_input[CONF_REFERENCE_ET_4],
                user_input[CONF_REFERENCE_ET_5],
                user_input[CONF_REFERENCE_ET_6],
                user_input[CONF_REFERENCE_ET_7],
                user_input[CONF_REFERENCE_ET_8],
                user_input[CONF_REFERENCE_ET_9],
                user_input[CONF_REFERENCE_ET_10],
                user_input[CONF_REFERENCE_ET_11],
                user_input[CONF_REFERENCE_ET_12],
            ]
            valid_et = self._check_reference_et(reference_et)
            if valid_et:
                # store entered values
                self._reference_et = reference_et
                # show next step
                return await self._show_step3(user_input)
            else:
                self._errors["base"] = "reference_evapotranspiration_problem"
                return await self._show_config_form(user_input)
            # valid_et = self._check_reference_et(reference_et)

            # if valid_api and valid_et:
            #    return self.async_create_entry(title=NAME, data=user_input)
            # if not valid_api:
            #    self._errors["base"] = "auth"
            # elif not valid_et:
            #    self._errors["base"] = "reference_evapotranspiration_problem"
            # return await self._show_config_form(user_input)
        return await self._show_config_form(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # only a single instance is allowed
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid_api = await self._test_api_key(user_input[CONF_API_KEY])
            if valid_api:
                # store values entered
                self._api_key = user_input[CONF_API_KEY].strip()
                # show next step
                return await self._show_step2(user_input)
            else:
                self._errors["base"] = "auth"
                return await self._show_config_form(user_input)
            # valid_et = self._check_reference_et(reference_et)

            # if valid_api and valid_et:
            #    return self.async_create_entry(title=NAME, data=user_input)
            # if not valid_api:
            #    self._errors["base"] = "auth"
            # elif not valid_et:
            #    self._errors["base"] = "reference_evapotranspiration_problem"
            # return await self._show_config_form(user_input)
        return await self._show_config_form(user_input)

    async def _show_step2(self, user_input):
        """Show the configuration form step 2: reference ET values."""
        return self.async_show_form(
            step_id="step2",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_REFERENCE_ET_1): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_2): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_3): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_4): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_5): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_6): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_7): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_8): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_9): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_10): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_11): vol.Coerce(float),
                    vol.Required(CONF_REFERENCE_ET_12): vol.Coerce(float),
                    # vol.Required(CONF_NUMBER_OF_SPRINKLERS): vol.Coerce(float),
                    # vol.Required(CONF_FLOW): vol.Coerce(float),
                    # vol.Required(CONF_AREA): vol.Coerce(float),
                }
            ),
            errors=self._errors,
        )

    async def _show_step3(self, user_input):
        """Show the configuration form step 2: reference ET values."""
        return self.async_show_form(
            step_id="step3",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NUMBER_OF_SPRINKLERS): vol.Coerce(float),
                    vol.Required(CONF_FLOW): vol.Coerce(float),
                    vol.Required(CONF_AREA): vol.Coerce(float),
                }
            ),
            errors=self._errors,
        )

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit info."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    # vol.Required(CONF_REFERENCE_ET_1): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_2): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_3): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_4): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_5): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_6): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_7): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_8): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_9): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_10): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_11): vol.Coerce(float),
                    # vol.Required(CONF_REFERENCE_ET_12): vol.Coerce(float),
                    # vol.Required(CONF_NUMBER_OF_SPRINKLERS): vol.Coerce(float),
                    # vol.Required(CONF_FLOW): vol.Coerce(float),
                    # vol.Required(CONF_AREA): vol.Coerce(float),
                }
            ),
            errors=self._errors,
        )

    async def _test_api_key(self, api_key):
        """Test access to Open Weather Map API here."""
        client = OWMClient(
            api_key=api_key.strip(), latitude=52.353218, longitude=5.0027695
        )

        try:
            client.get_data()
            return True
        except Exception as Ex:
            _LOGGER.error(Ex.strerror)
            return False

    def _check_reference_et(self, reference_et):
        """Check reference et values here."""
        try:
            if len(reference_et) != 12:
                return False
            else:
                all_floats = True
                for r in reference_et:
                    if not isinstance(r, float):
                        all_floats = False
                        break
                return all_floats
        except Exception as e:
            _LOGGER.error("Supplied reference Evapotranspiration was not valid.")
            return False

    def _check_irrigation_time(self, itime):
        """Check irrigation time."""
        timesplit = itime.split(":")
        if len(timesplit) != 2:
            return False
        else:
            try:
                hours = val(timesplit[0])
                minutes = val(timesplit[1])
                if hours >= 0 and hours <= 23 and minutes >= 0 and minutes <= 59:
                    return True
                else:
                    return False
            except ValueError as e:
                _LOGGER.error("No valid irrigation time specified.")
                return False
