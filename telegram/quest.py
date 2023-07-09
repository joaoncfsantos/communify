import math
import time
import enum as Enum


class Reward_type(Enum):
    XP = 1
    NFT = 2
    TOKEN = 3
    NO_REWARD = 0


class Quest:

    DISTANCE = 5

    def __init__(
        self,
        title: str,
        creator: str,
        latitude: int,
        longitude: int,
        description: str | None,
        reward_type: Reward_type,
        rewards: int | str | None,  # int = xp, str = addr, None = nothing
        end_timestamp: float | None,  # int | float = timestamp, None = endless quest
        start_timestamp: float | None,  # int | float = timestamp, None = instant quest
    ):
        self.title = title
        self.rewards = rewards
        self.description = description
        self.end_timestamp = end_timestamp
        self.start_timestamp = (
            time.time() if start_timestamp is None else start_timestamp
        )

    def verify(self, latitude: int, longitude: int) -> bool:
        return (
            self.get_distance(latitude, longitude) <= self.DISTANCE & self.is_active()
        )

    def __get_distance(self, latitude: int, longitude: int) -> float:
        lat_dif = abs(self.latitude - latitude)
        lon_dif = abs(self.longitude - longitude)
        return math.sqrt(pow(lat_dif, 2) + pow(lon_dif, 2))

    def is_active(self) -> bool:
        return time.time <= self.end_timestamp
