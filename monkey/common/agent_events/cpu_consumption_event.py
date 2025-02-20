from pydantic import conint

from common.types import Percent

from . import AbstractAgentEvent


class CPUConsumptionEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent consumes significant CPU resources for its own purposes.

    Attributes:
        :param utilization: The percentage of the CPU that is utilized
        :param cpu_number: The number of the CPU core that is utilized
    """

    utilization: Percent
    cpu_number: conint(ge=0, strict=True)  # type: ignore [valid-type]
