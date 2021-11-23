import json
import logging

import requests

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT
from infection_monkey.config import GUID, WormConfiguration
from infection_monkey.control import ControlClient
from monkey.infection_monkey.i_control_channel import IControlChannel

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class ControlChannel(IControlChannel):
    control_channel_server = WormConfiguration.current_server

    def should_agent_stop(self) -> bool:
        if not self.control_channel_server:
            return

        try:
            response = requests.get(  # noqa: DUO123
                f"{self.control_channel_server}/api/monkey_control/{GUID}",
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            response = json.loads(response.content.decode())
            return response["stop_agent"]
        except Exception as e:
            logger.error(f"An error occurred while trying to connect to server. {e}")

    def get_config(self) -> dict:
        ControlClient.load_control_config()
        return WormConfiguration.as_dict()

    def get_credentials_for_propagation(self) -> dict:
        if not self.control_channel_server:
            return

        try:
            response = requests.get(  # noqa: DUO123
                f"{self.control_channel_server}/api/propagationCredentials",
                verify=False,
                timeout=SHORT_REQUEST_TIMEOUT,
            )

            response = json.loads(response.content.decode())["propagation_credentials"]
            return response
        except Exception as e:
            logger.error(f"An error occurred while trying to connect to server. {e}")
