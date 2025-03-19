import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from amojowrapper.actions.delivery.schemes import DeliveryStatusRequest


class DeliveryStatusActionInterface(ABC):
    """
    Abstract base class that defines the interface for delivery status actions.

    Subclasses must implement `set()` and `_send()` methods.
    """

    @abstractmethod
    def set(self) -> None:
        """Sets the delivery status, to be implemented in subclass."""

    @abstractmethod
    def _send(self, body: Dict) -> int:
        """Sends the request, to be implemented in subclass."""


class AbstractDeliveryStatusAction(DeliveryStatusActionInterface):
    """
    Abstract class that provides common functionality for managing
    delivery status actions.
    """

    def __init__(self, client: Any) -> None:
        """
        Initializes the instance with client and scope_id.

        :param client: The client used to interact with the API.
        """
        self.client = client
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"
        self.msgid = None  # Message ID will be set later
        self._required_fields = {"msgid", "delivery_status", "error_code", "error"}

    def _filter_none(self, data: Dict) -> Dict:
        """
        Filters out keys in the provided dictionary where the values are None.

        :param data: A dictionary of data to filter.
        :return: A dictionary with keys that have non-None values.
        """
        return {k: v for k, v in data.items() if v is not None}

    def _validate_conversation_params(self, kwargs: Dict) -> None:
        """
        Validates that at least one required conversation parameter is provided.

        :param kwargs: A dictionary containing parameters for the conversation.
        :raises ValueError: If none of the required fields are provided.
        """
        if not any(kwargs.get(field) for field in self._required_fields):
            raise ValueError("Either msgid or delivery_status must be provided")

    def _build_payload(self, kwargs: Dict) -> Dict:
        """
        Builds the payload for the delivery status request.

        :param kwargs: A dictionary containing the delivery status parameters.
        :return: A dictionary containing the formatted request payload.
        """
        self._validate_conversation_params(kwargs)

        # Build payload dictionary using provided parameters
        payload_data = {
            "msgid": kwargs.get("msgid"),
            "delivery_status": kwargs.get("delivery_status"),
            "error_code": kwargs.get("error_code"),
            "error": kwargs.get("error"),
        }

        # Return the formatted payload excluding None values
        return DeliveryStatusRequest(**self._filter_none(payload_data)).model_dump(
            exclude_none=True
        )


class DeliveryStatusAction(AbstractDeliveryStatusAction):
    """
    Concrete implementation of the delivery status action, sends delivery status requests.
    """

    def set(self, **kwargs) -> str:
        """
        Sets the delivery status for a message, and sends the request to the server.

        :param kwargs: Parameters required to set the delivery status (e.g., msgid, delivery_status).
        :return: The response status or error message.
        :raises ValueError: If the 'msgid' is not provided.
        """
        # Build the payload using the provided arguments
        payload: dict = self._build_payload(kwargs)

        # Check if msgid is provided, and set it before sending
        if kwargs.get("msgid"):
            self.msgid = kwargs.get("msgid")
            return self._send(body=payload)
        raise ValueError("msgid not found")

    def _send(self, body: Dict) -> int:
        """
        Sends the delivery status request to the server.

        :param body: The payload to send in the request.
        :return: The HTTP status code from the response (200 if successful).
        :raises Exception: If the request fails or response is invalid.
        """
        try:
            # Perform the API request to update delivery status
            response = self.client.custom_request(
                method="POST",
                endpoint=f"/v2/origin/custom/{self.scope_id}/{self.msgid}/delivery_status",
                data=body,
            )
            # Return True if the status code is 200, indicating success
            return response.status_code

        except json.JSONDecodeError:
            # Handle potential JSON decoding errors
            raise

        except Exception:
            # Catch and re-raise any other exceptions
            raise
