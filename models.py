from pydantic import BaseModel
from openenv.core.env_server import Action, Observation, State

class MyAssistantBotAction(Action):
    message: str   # The AI's answer to the coding challenge

class MyAssistantBotObservation(Observation):
    echoed_message: str  # The challenge text or feedback

class MyAssistantBotState(State):
    current_challenge_index: int = 0
    total_score: float = 0.0
    easy_score: float = 0.0
    medium_score: float = 0.0
    hard_score: float = 0.0
    correct_count: int = 0
    wrong_count: int = 0