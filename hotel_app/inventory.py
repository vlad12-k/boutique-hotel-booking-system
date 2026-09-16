from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Mapping

from hotel_app.domain import Money


@dataclass(frozen=True, slots=True)
class RoomTypeContract:
    code: str
    label_config_key: str
    default_label: str
    bathroom_type: str
    has_balcony_or_terrace: bool
    rate_config_key: str


@dataclass(frozen=True, slots=True)
class RoomContract:
    number: str
    room_type_code: str


HAIFA_ROOM_TYPES = (
    RoomTypeContract(
        code="private-bathroom",
        label_config_key="HAIFA_PRIVATE_ROOM_LABEL",
        default_label="Private bathroom room",
        bathroom_type="private",
        has_balcony_or_terrace=False,
        rate_config_key="HAIFA_PRIVATE_ROOM_RATE",
    ),
    RoomTypeContract(
        code="private-bathroom-terrace",
        label_config_key="HAIFA_TERRACE_ROOM_LABEL",
        default_label="Private bathroom room with terrace",
        bathroom_type="private",
        has_balcony_or_terrace=True,
        rate_config_key="HAIFA_TERRACE_ROOM_RATE",
    ),
    RoomTypeContract(
        code="shared-bathroom-economy",
        label_config_key="HAIFA_ECONOMY_ROOM_LABEL",
        default_label="Shared bathroom economy room",
        bathroom_type="shared",
        has_balcony_or_terrace=False,
        rate_config_key="HAIFA_ECONOMY_ROOM_RATE",
    ),
)

HAIFA_ROOMS = (
    RoomContract("1", "private-bathroom"),
    RoomContract("2", "private-bathroom"),
    RoomContract("3", "private-bathroom-terrace"),
    RoomContract("4", "shared-bathroom-economy"),
    RoomContract("5", "shared-bathroom-economy"),
    RoomContract("6", "private-bathroom"),
    RoomContract("7", "private-bathroom"),
)


def configured_room_type_values(
    config: Mapping[str, object], contract: RoomTypeContract
) -> tuple[str, Money]:
    """Resolve configurable labels and rates without inventing production prices."""
    label = str(config.get(contract.label_config_key) or contract.default_label).strip()
    rate_value = config.get(contract.rate_config_key)
    currency = str(config.get("PROPERTY_CURRENCY") or "ILS").upper()

    if not label:
        raise ValueError(f"{contract.label_config_key} cannot be empty.")
    if rate_value in (None, ""):
        raise ValueError(f"{contract.rate_config_key} must be configured.")

    try:
        rate = Decimal(str(rate_value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(
            f"{contract.rate_config_key} must be a valid monetary amount."
        ) from error

    money = Money(rate, currency)
    return label, money
