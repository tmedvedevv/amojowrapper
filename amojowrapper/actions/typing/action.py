import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from amojowrapper.actions.typing.schemes import TypingScheme, Sender


class TypingActionInterface(ABC):
    """
    Interface for typing actions that can be performed in the system.

    Methods:
        send: Sends a typing action request.
        _send: Internal method to send the request to the server.
    """

    @abstractmethod
    def send(self, **kwargs) -> str:
        """
        Sends a typing action request with the given parameters.
        """
        pass

    @abstractmethod
    def _send(self, body: Dict) -> int:
        """
        Sends the actual request to the server.
        """
        pass


class AbstractTypingAction(TypingActionInterface):
    """
    Abstract class for implementing typing actions, providing common utilities.

    Attributes:
        client: The client instance to send the request.
        scope_id: A unique identifier for the scope of the request.
        _required_fields: A set of required fields for the conversation parameters.
    """

    def __init__(self, client: Any):
        self.client = client
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"
        self._required_fields = {
            "id",
            "conversation_id",
            "ref_id",
            "conversation_ref_id",
        }

    def _filter_none(self, data: Dict) -> Dict:
        """
        Filters out any keys with None values from the provided dictionary.
        """
        return {k: v for k, v in data.items() if v is not None}

    def _validate_conversation_params(self, kwargs: Dict) -> None:
        """
        Validates that either conversation_id or conversation_ref_id is provided.
        """
        if not any(kwargs.get(field) for field in self._required_fields):
            raise ValueError(
                "Either conversation_id or conversation_ref_id must be provided"
            )

    def _create_sender(self, kwargs: Dict) -> Dict:
        """
        Creates a sender object with the given parameters.
        """
        sender_data = self._filter_none(
            {"id": kwargs.get("sender_id"), "ref_id": kwargs.get("sender_ref_id")}
        )
        return Sender(**sender_data).model_dump(exclude_none=True)

    def _build_payload(self, kwargs: Dict, **components) -> Dict:
        """
        Builds the payload for the typing action request.
        """
        self._validate_conversation_params(kwargs)

        payload_data = {
            "conversation_id": kwargs.get("conversation_id") or None,
            "conversation_ref_id": kwargs.get("conversation_ref_id") or None,
            "sender": components.get("sender") or None,
        }

        return TypingScheme(**self._filter_none(payload_data)).model_dump(
            exclude_none=True
        )


class TypingAction(AbstractTypingAction):
    """
    Concrete implementation of the TypingAction class, sends the typing action request.
    """

    def send(self, **kwargs) -> str:
        """
        Sends a typing action request.

        Args:
            kwargs: Parameters for the typing action, including sender, conversation ID, etc.
        """
        try:
            components = {
                "sender": self._create_sender(kwargs),
            }

            payload = self._build_payload(kwargs, **components)
        except ValueError as e:
            print(f"Validation error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

        return self._send(body=payload)

    def _send(self, body: Dict) -> int:
        """
        Sends the actual request to the server.

        Args:
            body: The payload to be sent to the server.

        Returns:
            int: The status code from the server response (204 if successful).
        """
        try:
            response = self.client.custom_request(
                method="POST",
                endpoint=f"/v2/origin/custom/{self.scope_id}/typing",
                data=body,
            )
            return response.status_code == 204

        except json.JSONDecodeError:
            raise
        except Exception as e:
            print(f"Error in sending request: {e}")
            raise
