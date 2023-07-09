from quest import Quest, Reward_type
import json

class QuestManager:

    def __init__(self, communnity_id: str):
        with open("data.json", "r") as file:
            existing_data = json.load(file)
        self.quests = existing_data

    def add_quest(
        self,
        title: str,
        creator: str,
        latitude: int,
        longitude: int,
        quest_thread_id: str,  # ID of the quest chain event
        description: str | None,
        reward_type: Reward_type,
        rewards: int | str | None,  # int = xp, str = addr, None = nothing
        end_timestamp: float | None,  # int | float = timestamp, None = endless quest
        start_timestamp: float | None,  # int | float = timestamp, None = instant quest
    ):
        self.quests[self.__get_quest_id(title)] = (
            Quest(
                title=title,
                creator=creator,
                latitude=latitude,
                longitude=longitude,
                description=description,
                reward_type=reward_type,
                rewards=rewards,
                end_timestamp=end_timestamp,
                start_timestamp=start_timestamp,
            )
        )
        with open("data.json", "w") as file:
            # Write the updated data to the file
            json.dump(self.quests, file)

    def __get_quest_id(self, thread_id: str) -> str:
        quest_count = len(self.quests[thread_id]) + 1
        return f"{thread_id}_{quest_count}"

    def verify_user(self, user_wallet: str, latitude: int, longitude: int, quest_thread_id: str) -> bool:
        quest = self.quests[quest_thread_id]
        if quest.verify(latitude, longitude):
            self.__get_user(user_wallet).reward(quest.rewards, quest.reward_type)
            return True
        return False

    def __get_user(self, user_wallet: str):
        pass

    def __get_quest(self, quest_id: str) -> Quest:
        pass
