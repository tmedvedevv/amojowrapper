from typing import Optional
from pydantic import BaseModel


class Sender(BaseModel):
    """
    Represents a sender in the typing action request.

    Attributes:
        id: The unique identifier for the sender.
        ref_id: The reference identifier for the sender.
    """

    id: Optional[str] = None
    ref_id: Optional[str] = None


class TypingScheme(BaseModel):
    """
    Represents the payload schema for a typing action request.

    Attributes:
        conversation_id: The unique identifier for the conversation.
        conversation_ref_id: The reference identifier for the conversation.
        sender: The sender of the typing action.
    """

    conversation_id: Optional[str] = None
    conversation_ref_id: Optional[str] = None
    sender: Optional[Sender] = None
