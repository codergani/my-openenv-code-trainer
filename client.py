# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""My Assistant Bot Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from .models import MyAssistantBotAction, MyAssistantBotObservation


class MyAssistantBotEnv(
    EnvClient[MyAssistantBotAction, MyAssistantBotObservation, State]
):
    """
    Client for the My Assistant Bot Environment.

    This client maintains a persistent WebSocket connection to the environment server,
    enabling efficient multi-step interactions with lower latency.
    Each client instance has its own dedicated environment session on the server.

    Example:
        >>> # Connect to a running server
        >>> with MyAssistantBotEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.echoed_message)
        ...
        ...     result = client.step(MyAssistantBotAction(message="Hello!"))
        ...     print(result.observation.echoed_message)

    Example with Docker:
        >>> # Automatically start container and connect
        >>> client = MyAssistantBotEnv.from_docker_image("my_assistant_bot-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(MyAssistantBotAction(message="Test"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: MyAssistantBotAction) -> Dict:
        """
        Convert MyAssistantBotAction to JSON payload for step message.

        Args:
            action: MyAssistantBotAction instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return {
            "message": action.message,
        }

    def _parse_result(self, payload: Dict) -> StepResult[MyAssistantBotObservation]:
        """
        Parse server response into StepResult[MyAssistantBotObservation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with MyAssistantBotObservation
        """
        obs_data = payload.get("observation", {})
        observation = MyAssistantBotObservation(
            echoed_message=obs_data.get("echoed_message", ""),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    from .models import MyAssistantBotAction, MyAssistantBotObservation, MyAssistantBotState

    def _parse_state(self, payload: Dict) -> MyAssistantBotState:
        """
        Parse server response into MyAssistantBotState object.

        Args:
            payload: JSON response from state request

        Returns:
            MyAssistantBotState object
        """
        return MyAssistantBotState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            current_challenge_index=payload.get("current_challenge_index", 0),
            total_score=payload.get("total_score", 0.0),
            correct_count=payload.get("correct_count", 0),
            wrong_count=payload.get("wrong_count", 0),
            easy_score=payload.get("easy_score", 0.0),
            medium_score=payload.get("medium_score", 0.0),
            hard_score=payload.get("hard_score", 0.0),
        )
