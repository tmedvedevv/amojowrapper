from typing import Literal, Optional, List
from pydantic import BaseModel, model_validator


class Profile(BaseModel):
    """Represents a user's profile with optional contact details."""

    phone: Optional[str] = None
    email: Optional[str] = None


class EmbeddedUser(BaseModel):
    """Represents an embedded user with id, ref_id, and name."""

    id: Optional[str] = None
    ref_id: Optional[str] = None
    name: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_embedded_user(cls, values):
        """Ensure that at least one of id, ref_id, or name is provided."""
        if not values.get("id") and not values.get("ref_id") and not values.get("name"):
            raise ValueError("At least one of id, ref_id, or name must be provided")
        return values


class Location(BaseModel):
    """Represents a geographical location with longitude and latitude."""

    lon: float
    lat: float


class Contact(BaseModel):
    """Represents a contact with a name and phone number."""

    name: str
    phone: str


class EmbeddedMessage(BaseModel):
    """Represents an embedded message, which could be text, contact, file, etc."""

    id: Optional[str] = None
    msgid: Optional[str] = None
    type: Optional[
        Literal[
            "text",
            "contact",
            "file",
            "video",
            "picture",
            "voice",
            "audio",
            "sticker",
            "location",
        ]
    ] = None
    text: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    media_duration: Optional[int] = None
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    timestamp: Optional[int] = None
    msec_timestamp: Optional[int] = None
    sender: Optional[EmbeddedUser] = None

    @model_validator(mode="before")
    @classmethod
    def check_embedded_message(cls, values):
        """Validate that required fields are provided based on message type."""
        if not values.get("id") and not values.get("msgid"):
            required_fields = ["type", "timestamp", "msec_timestamp", "sender"]
            for field in required_fields:
                if not values.get(field):
                    raise ValueError(
                        f"{field} is required when id and msgid are not present"
                    )
            msg_type = values.get("type")
            if msg_type == "text" and not values.get("text"):
                raise ValueError("text is required for embedded message of type 'text'")
            if msg_type == "contact" and not values.get("contact"):
                raise ValueError(
                    "contact is required for embedded message of type 'contact'"
                )
            if msg_type == "location" and not values.get("location"):
                raise ValueError(
                    "location is required for embedded message of type 'location'"
                )
        return values


class ReplyTo(BaseModel):
    """Represents a reply to a message."""

    message: EmbeddedMessage


class Forwards(BaseModel):
    """Represents forwarded messages."""

    messages: List[EmbeddedMessage]
    conversation_ref_id: Optional[str] = None
    conversation_id: Optional[str] = None


class Message(BaseModel):
    """Represents a message, which could be of various types such as text, file, location, etc."""

    type: Literal[
        "text",
        "contact",
        "file",
        "video",
        "picture",
        "voice",
        "audio",
        "sticker",
        "location",
    ]
    text: Optional[str] = None
    media: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    sticker_id: Optional[str] = None
    location: Optional[Location] = None
    contact: Optional[Contact] = None
    callback_data: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values):
        """Ensure that the required fields are present based on message type."""
        msg_type = values.get("type")
        errors = []
        if msg_type == "text" and not values.get("text"):
            errors.append("text is required for type 'text'")
        elif msg_type == "contact" and not values.get("contact"):
            errors.append("contact is required for type 'contact'")
        elif msg_type == "location" and not values.get("location"):
            errors.append("location is required for type 'location'")
        elif msg_type in ["file", "video", "picture"]:
            if not values.get("media"):
                errors.append(f"media is required for type '{msg_type}'")
            if not values.get("file_name"):
                errors.append(f"file_name is required for type '{msg_type}'")
        if errors:
            raise ValueError("; ".join(errors))
        return values


class SenderReceiver(BaseModel):
    """Represents a sender or receiver with optional profile information."""

    id: Optional[str] = None
    ref_id: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    profile: Optional[Profile] = None
    profile_link: Optional[str] = None


class Source(BaseModel):
    """Represents the source of the message, identified by external_id."""

    external_id: Optional[str] = None


class DeliveryStatus(BaseModel):
    """Represents the delivery status of a message."""

    status_code: int
    error_code: Optional[int] = None
    error: Optional[str] = None


class Payload(BaseModel):
    """Represents the payload of a message, including the sender, receiver, and message details."""

    timestamp: Optional[int] = None
    msec_timestamp: Optional[int] = None
    msgid: Optional[str] = None
    conversation_id: Optional[str] = None
    conversation_ref_id: Optional[str] = None
    silent: Optional[bool] = True
    source: Optional[Source] = None
    sender: SenderReceiver = None
    receiver: Optional[SenderReceiver] = None
    id: Optional[str] = None
    message: Optional[Message] = None
    reply_to: Optional[ReplyTo] = None
    forwards: Optional[Forwards] = None
    delivery_status: Optional[DeliveryStatus] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values):
        """Ensure that essential fields such as conversation_id and timestamp are present."""
        if not values.get("conversation_id") and not values.get("conversation_ref_id"):
            raise ValueError("need conversation_id or conversation_ref_id")
        if not values.get("timestamp") and not values.get("msec_timestamp"):
            raise ValueError("need timestamp or msec_timestamp")
        return values


class RequestModel(BaseModel):
    """Represents a request model for new or edited messages."""

    event_type: Literal["new_message", "edit_message"]
    payload: Payload


class NewMessageResponse(BaseModel):
    """Represents the response for a new message."""

    conversation_id: Optional[str] = None
    ref_id: Optional[str] = None
    msgid: Optional[str] = None
    sender_id: Optional[str] = None


class MessageResponse(BaseModel):
    """Represents a message response containing new message details."""

    new_message: NewMessageResponse
