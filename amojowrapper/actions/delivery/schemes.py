from typing import Optional
from pydantic import BaseModel


class DeliveryStatusRequest(BaseModel):
    """
    Represents the request payload for updating the delivery status of a message.

    Attributes:
        msgid (Optional[str]): The unique identifier of the message.
        delivery_status (Optional[int]): The status of the message delivery.
        error_code (Optional[int]): The error code, if any, associated with the delivery.
        error (Optional[str]): A description of the error, if any.
    """

    msgid: Optional[str] = None
    delivery_status: Optional[int] = None
    error_code: Optional[int] = None
    error: Optional[str] = None
