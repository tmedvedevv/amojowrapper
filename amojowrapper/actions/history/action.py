import json
from abc import ABC, abstractmethod
from typing import Any

from amojowrapper.actions.history.schemes import HistoryResponse


class HistoryActionInterface(ABC):
    """
    Abstract base class that defines the interface for history actions.

    Subclasses must implement `get()` and `_send()` methods.
    """

    @abstractmethod
    def get(self, **kwargs) -> str:
        """
        Retrieves the chat history for a given conversation.

        :param kwargs: Additional parameters for the request.
        :return: The response from the server.
        """

    @abstractmethod
    def _send(self, conversation_ref_id: str) -> HistoryResponse:
        """
        Sends the request to retrieve chat history.

        :param conversation_ref_id: The unique identifier of the conversation.
        :return: The response from the server.
        """


class AbstractHistoryAction(HistoryActionInterface):
    """
    Abstract class that provides common functionality for managing
    history actions.
    """

    def __init__(self, client: Any):
        """
        Initializes the instance with client and scope_id.

        :param client: The client used to interact with the API.
        """
        self.client = client
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"


class HistoryAction(AbstractHistoryAction):
    """
    Concrete implementation of the history action, retrieves chat history.
    """

    def get(self, **kwargs) -> HistoryResponse:
        """
        Retrieves the chat history for a given conversation.

        :param kwargs: Additional parameters for the request.
        :return: The response from the server.
        """
        conversation_ref_id: str = kwargs.get("conversation_ref_id")
        return self._send(conversation_ref_id=conversation_ref_id)

    def _send(self, conversation_ref_id: str) -> HistoryResponse:
        """
        Sends the request to retrieve chat history.

        :param conversation_ref_id: The unique identifier of the conversation.
        :return: The response from the server.
        :raises RuntimeError: If the request fails or response is invalid.
        """
        try:
            response = self.client.custom_request(
                method="GET",
                endpoint=f"/v2/origin/custom/{self.scope_id}/chats/{conversation_ref_id}/history",
            )
            return HistoryResponse(**response.json())

        except (json.JSONDecodeError, Exception) as e:
            raise RuntimeError(f"Failed to retrieve chat history: {e}") from e
