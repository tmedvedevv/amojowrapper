import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from amojowrapper.actions.react.schemes import ReactScheme, User


class ReactActionInterface(ABC):
    """Interface for React action classes."""

    @abstractmethod
    def set(self) -> int:
        """Sets the react action, to be implemented by subclasses."""
        pass

    @abstractmethod
    def _send(self, body: Dict) -> int:
        """Sends the react action payload, to be implemented by subclasses."""
        pass


class AbstractReactAction(ReactActionInterface):
    """Abstract base class for React actions, implements common methods for React actions."""

    def __init__(self, client: Any):
        """Initializes the React action with client information."""
        self.client = client
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"

        self._required_fields = {
            "conversation_id",
            "conversation_ref_id",
            "id",
            "user",
            "type",
            "emoji",
        }

    def _filter_none(self, data: Dict) -> Dict:
        """Filters out None values from a dictionary."""
        return {k: v for k, v in data.items() if v is not None}

    def _validate_conversation_params(self, kwargs: Dict) -> None:
        """Validates that required conversation parameters are provided."""
        if not any(kwargs.get(field) for field in self._required_fields):
            raise ValueError(
                "Either conversation_id or conversation_ref_id must be provided"
            )

    def _create_user(self, kwargs: Dict) -> Dict:
        """Creates a user dictionary from provided data."""
        user_data = self._filter_none(
            {
                "id": kwargs.get("user_id"),
                "ref_id": kwargs.get("user_ref_id"),
            }
        )
        return User(**user_data).model_dump(exclude_none=True)

    def _build_payload(self, kwargs: Dict, **components) -> Dict:
        """Builds the payload dictionary for the react action."""
        self._validate_conversation_params(kwargs)

        payload_data = {
            "conversation_id": kwargs.get("conversation_id") or None,
            "conversation_ref_id": kwargs.get("conversation_ref_id") or None,
            "id": kwargs.get("id") or None,
            "user": components.get("user") or None,
            "type": kwargs.get("type") or None,
            "emoji": kwargs.get("emoji") or None,
        }

        return ReactScheme(**self._filter_none(payload_data)).model_dump(
            exclude_none=True
        )


class ReactAction(AbstractReactAction):
    """Class for handling React actions."""

    def set(self, **kwargs) -> int:
        """Sets the react action by building and sending the payload."""
        try:
            components = {
                "user": self._create_user(kwargs),
            }

            payload = self._build_payload(kwargs, **components)
        except ValueError as e:
            # Catching the ValueError more specifically
            print(f"ValueError: {e}")
            return -1  # Returning a failure code, for example

        return self._send(body=payload)

    def _send(self, body: Dict) -> int:
        """Sends the payload to the API and returns the response code."""
        try:
            response = self.client.custom_request(
                method="POST",
                endpoint=f"/v2/origin/custom/{self.scope_id}/react",
                data=body,
            )
            return response

        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            raise
        except Exception as e:
            # Catching more general exceptions
            print(f"Exception occurred: {e}")
            raise
