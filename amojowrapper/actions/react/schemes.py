from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a user in the react action.

    Attributes:
        id (Optional[str]): The unique identifier for the user.
        ref_id (Optional[str]): A reference identifier for the user.
    """

    id: Optional[str] = None
    ref_id: Optional[str] = None


class ReactScheme(BaseModel):
    """
    Represents the schema for a React action.

    Attributes:
        conversation_id (Optional[str]): The unique identifier for the conversation.
        conversation_ref_id (Optional[str]): A reference identifier for the conversation.
        id (Optional[str]): The unique identifier for the react action.
        user (Optional[User]): The user associated with the react action.
        type (Optional[str]): The type of the react action (e.g., 'like', 'love').
        emoji (Optional[str]): The emoji used for the react action.
    """

    conversation_id: Optional[str] = None
    conversation_ref_id: Optional[str] = None
    id: Optional[str] = None
    user: Optional[User] = None
    type: Optional[str] = None
    emoji: Optional[str] = None
