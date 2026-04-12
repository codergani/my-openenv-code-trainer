from pydantic import BaseModel, Field
from openenv.core.env_server import Action, Observation, State

class MyAssistantBotAction(Action):
    message: str   # The AI's answer to the coding challenge

class MyAssistantBotObservation(Observation):
    echoed_message: str  # The challenge text or feedback

class MyAssistantBotState(State):
    current_challenge_index: int = Field(default=0, ge=0)
    total_score: int = Field(default=0, ge=0)
    easy_score: int = Field(default=0, ge=0)
    medium_score: int = Field(default=0, ge=0)
    hard_score: int = Field(default=0, ge=0)
    correct_count: int = Field(default=0, ge=0)
    wrong_count: int = Field(default=0, ge=0)