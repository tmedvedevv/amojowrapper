import json
import uuid
import datetime
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from amojowrapper.actions.message.schemes import (
    Payload,
    Message,
    Source,
    SenderReceiver,
    MessageResponse,
    RequestModel,
    ReplyTo,
)


class MessageActionInterface(ABC):
    """
    Interface for actions related to sending and editing messages.
    """

    @abstractmethod
    def send(self, **kwargs) -> MessageResponse:
        """
        Sends a message.

        :param kwargs: Parameters for sending the message.
        :return: Response from the server.
        """
        pass


class AbstractMessageAction(MessageActionInterface):
    """
    Abstract class providing common functionality for message actions.
    """

    def __init__(self, client: Any):
        """
        Initializes the instance with a client and scope_id.

        :param client: The client used to interact with the API.
        """
        self.client = client
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"
        self._required_fields = {"conversation_id", "conversation_ref_id"}

    def _filter_none(self, data: Dict) -> Dict:
        """
        Filters out keys with None values from the dictionary.

        :param data: Dictionary to filter.
        :return: Filtered dictionary.
        """
        return {k: v for k, v in data.items() if v is not None}

    def _generate_uid(self, prefix: str = "") -> str:
        """
        Generates a unique identifier with an optional prefix.

        :param prefix: Prefix for the unique identifier.
        :return: Generated unique identifier.
        """
        return prefix + str(uuid.uuid4())

    def _get_timestamp(self) -> int:
        """
        Returns the current UTC timestamp in seconds.

        :return: Current UTC timestamp.
        """
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    def _get_msec_timestamp(self) -> int:
        """
        Returns the current UTC timestamp in milliseconds.

        :return: Current UTC timestamp in milliseconds.
        """
        return self._get_timestamp() * 1000

    def _create_message(self, kwargs: Dict) -> Dict:
        """
        Creates a message dictionary from the provided arguments.

        :param kwargs: Arguments for creating the message.
        :return: Dictionary representing the message.
        """

        payload = {
            "type": kwargs.get("message_type"),
            "text": kwargs.get("message_text"),
            "media": kwargs.get("message_media"),
            "file_name": kwargs.get("message_file_name"),
            "file_size": kwargs.get("message_file_size"),
            "sticker_id": kwargs.get("message_sticker_id"),
            "location": {
                "lon": kwargs.get("message_location_lon"),
                "lat": kwargs.get("message_location_lat"),
            },
            "contact": {
                "name": kwargs.get("message_contact_name"),
                "phone": kwargs.get("message_contact_phone"),
            },
            "callback_data": kwargs.get("message_callback_data"),
        }

        if payload["contact"]["name"] is None and payload["contact"]["phone"] is None:
            payload.pop("contact")

        if payload["location"]["lon"] is None and payload["location"]["lat"] is None:
            payload.pop("location")

        message_data = self._filter_none(payload)

        return Message(**message_data).model_dump(exclude_none=True)

    def _create_source(self, kwargs: Dict) -> Optional[Dict]:
        """
        Creates a source dictionary if an external_id is provided.

        :param kwargs: Arguments for creating the source.
        :return: Dictionary representing the source, or None if no external_id is provided.
        """
        if external_id := kwargs.get("source_external_id"):
            return Source(external_id=external_id).model_dump(exclude_none=True)
        return None

    def _create_sender(self, kwargs: Dict) -> Dict:
        """
        Creates a sender dictionary from the provided arguments.

        :param kwargs: Arguments for creating the sender.
        :return: Dictionary representing the sender.
        """

        profile = {}

        if kwargs.get("sender_profile_phone"):
            profile["phone"] = kwargs.get("sender_profile_phone")

        if kwargs.get("sender_profile_email"):
            profile["email"] = kwargs.get("sender_profile_email")

        if bool(profile) is False:
            profile = None

        sender_data = self._filter_none(
            {
                "id": kwargs.get("sender_id"),
                "ref_id": kwargs.get("sender_ref_id"),
                "name": kwargs.get("sender_name") or "amojowrapper",
                "profile": profile,
                "avatar": kwargs.get("sender_avatar"),
                "profile_link": kwargs.get("sender_profile_link"),
            }
        )
        return SenderReceiver(**sender_data).model_dump(exclude_none=True)

    def _create_receiver(self, kwargs: Dict) -> Optional[Dict]:
        """
        Creates a receiver dictionary if either receiver_id or receiver_ref_id is provided.

        :param kwargs: Arguments for creating the receiver.
        :return: Dictionary representing the receiver, or None if no valid data is provided.
        """
        receiver_data = self._filter_none(
            {
                "id": kwargs.get("receiver_id"),
                "ref_id": kwargs.get("receiver_ref_id"),
            }
        )

        if not receiver_data.get("ref_id") and not receiver_data.get("id"):
            return None

        return SenderReceiver(**receiver_data).model_dump(exclude_none=True)

    def _create_reply_to(self, kwargs: Dict) -> Optional[Dict]:
        """
        Creates a reply_to dictionary if a reply_to_msgid is provided.

        :param kwargs: Arguments for creating the reply_to.
        :return: Dictionary representing the reply_to, or None if no reply_to_msgid is provided.
        """
        if msg_id := kwargs.get("reply_to_msgid"):
            return ReplyTo(message={"id": msg_id}).model_dump(exclude_none=True)
        return None

    def _validate_conversation_params(self, kwargs: Dict) -> None:
        """
        Validates that at least one of the required conversation parameters is provided.

        :param kwargs: Arguments to validate.
        :raises ValueError: If neither conversation_id nor conversation_ref_id is provided.
        """
        if not any(kwargs.get(field) for field in self._required_fields):
            raise ValueError(
                "Either conversation_id or conversation_ref_id must be provided"
            )

    def _build_payload(self, kwargs: Dict, **components) -> Dict:
        """
        Builds the payload dictionary for the request.

        :param kwargs: Arguments for building the payload.
        :param components: Pre-built components (message, source, sender, receiver, reply_to).
        :return: Dictionary representing the payload.
        """
        self._validate_conversation_params(kwargs)

        payload_data = {
            "timestamp": kwargs.get("timestamp") or self._get_timestamp(),
            "msec_timestamp": kwargs.get("msec_timestamp")
            or self._get_msec_timestamp(),
            "msgid": kwargs.get("msgid") or self._generate_uid("amojowrapper_msgid_"),
            "conversation_id": kwargs.get("conversation_id"),
            "conversation_ref_id": kwargs.get("conversation_ref_id"),
            "silent": kwargs.get("silent", False),
            "message": components.get("message"),
            "sender": components.get("sender"),
            "source": components.get("source"),
            "receiver": components.get("receiver"),
            "reply_to": components.get("reply_to"),
        }

        return Payload(**self._filter_none(payload_data)).model_dump(exclude_none=True)

    @abstractmethod
    def _send(self, body: Dict) -> MessageResponse:
        """
        Sends the request to the server.

        :param body: The payload to send.
        :return: Response from the server.
        """
        pass


class MessageAction(AbstractMessageAction):
    """
    Concrete implementation of message actions.
    """

    def send(self, **kwargs) -> MessageResponse:
        """
        Sends a message using the provided arguments.

        Possible parameters include:
            sender_id
            sender_ref_id
            sender_name
            sender_profile_phone
            sender_profile_email
            sender_profile_link
            reply_to_msgid
            source_external_id
            conversation_id
            conversation_ref_id
            receiver_id
            receiver_ref_id
            silent

        :param kwargs: Arguments for sending the message.
        :return: Response from the server.
        """
        try:
            components = {
                "message": self._create_message(kwargs),
                "source": self._create_source(kwargs),
                "sender": self._create_sender(kwargs),
                "receiver": self._create_receiver(kwargs),
                "reply_to": self._create_reply_to(kwargs),
            }

            payload = self._build_payload(kwargs, **components)
            request_body = RequestModel(
                event_type="new_message", payload=Payload(**payload)
            ).model_dump(exclude_none=True)

            return self._send(request_body)

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to decode JSON response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to send message: {e}")

    def edit(self, **kwargs) -> MessageResponse:
        """
        Edits a message using the provided arguments.

        :param kwargs: Arguments for editing the message.
        :return: Response from the server.
        """
        try:
            components = {"message": self._create_message(kwargs)}

            payload = self._build_payload(kwargs, **components)

            request_body = RequestModel(
                event_type="edit_message", payload=Payload(**payload)
            ).model_dump(exclude_none=True)

            return self._send(request_body)

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to decode JSON response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to edit message: {e}")

    def _send(self, body: Dict) -> MessageResponse:
        """
        Sends the request to the server.

        :param body: The payload to send.
        :return: Response from the server.
        """
        try:
            response = self.client.custom_request(
                method="POST", endpoint=f"/v2/origin/custom/{self.scope_id}", data=body
            )
            return MessageResponse(**response.json())

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to decode JSON response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to send request: {e}")
