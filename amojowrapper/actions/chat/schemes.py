from typing import Optional
from pydantic import BaseModel, Field, constr


class Profile(BaseModel):
    """
    Represents additional information about a user, such as their phone and email.

    Fields:
        phone (Optional[str]): The user's phone number, optional.
        email (Optional[str]): The user's email address, optional.
    """

    phone: Optional[str] = Field(
        None, description="User's phone number. Optional field."
    )
    email: Optional[str] = Field(
        None, description="User's email address. Optional field."
    )


class User(BaseModel):
    """
    Represents a chat participant with necessary details such as name, avatar, and profile.

    Fields:
        id (str): The identifier of the chat participant on the integration side (required).
        ref_id (Optional[str]): The participant's identifier on amoCRM side. Used for existing users.
        client_id (Optional[str]): The client ID of the participant. Absent for amoCRM users.
        name (str): The participant's name (required).
        avatar (Optional[str]): The URL of the participant's avatar, should be accessible for download.
        profile (Optional[Profile]): Additional information about the user (optional).
        profile_link (Optional[str]): The user's profile link in an external chat system (optional).
    """

    id: str = Field(
        ...,
        description="The participant's identifier on the integration side (required).",
    )
    ref_id: Optional[str] = Field(
        None,
        description="The participant's identifier on amoCRM side. Used for existing users.",
    )
    client_id: Optional[str] = Field(
        None,
        description="The participant's identifier on the integration side. Absent for amoCRM users.",
    )
    name: str = Field(..., description="The participant's name (required).")
    avatar: Optional[str] = Field(
        None,
        description="URL of the participant's avatar. Should be downloadable.",
    )
    profile: Optional[Profile] = Field(
        None, description="Additional information about the user (optional)."
    )
    profile_link: Optional[str] = Field(
        None,
        description="Link to the user's profile in an external chat system (optional).",
    )


class Source(BaseModel):
    """
    Represents the source of the chat, containing an external ID.

    Fields:
        external_id (Optional[constr(max_length=40)]): The external identifier of the chat source.
    """

    external_id: Optional[constr(max_length=40)] = Field(
        None,
        description="The external identifier of the chat source (up to 40 characters, printable ASCII).",
    )


class ChatRequest(BaseModel):
    """
    Represents the request body for creating or interacting with a chat.

    Fields:
        conversation_id (str): The identifier of the chat on the integration side (required).
        source (Optional[Source]): Information about the chat source (optional).
        user (User): Information about the chat participant (required).
    """

    conversation_id: str = Field(
        ...,
        description="The identifier of the chat on the integration side (required).",
    )
    source: Optional[Source] = Field(
        None, description="Information about the chat source (optional)."
    )
    user: User = Field(
        ..., description="Information about the chat participant (required)."
    )


class ChatResponse(BaseModel):
    """
    Represents the response structure for chat interactions.

    Fields:
        id (str): The identifier of the chat on the integration side (required).
        source (Optional[Source]): Information about the chat source (optional).
        user (User): Information about the chat participant (required).
    """

    id: str = Field(
        ...,
        description="The identifier of the chat on the integration side (required).",
    )
    source: Optional[Source] = Field(
        None, description="Information about the chat source (optional)."
    )
    user: User = Field(
        ..., description="Information about the chat participant (required)."
    )
