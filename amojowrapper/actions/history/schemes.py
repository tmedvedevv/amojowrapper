from pydantic import BaseModel, Field
from typing import Optional, List


class SenderReceiverBase(BaseModel):
    """
    Base class representing a sender or receiver in a messaging system.

    Attributes:
        id (Optional[str]): Unique identifier for the sender or receiver.
        name (Optional[str]): Name of the sender or receiver.
        client_id (Optional[str]): ID of the user on the integration side.
        avatar (Optional[str]): URL to the avatar image of the sender or receiver.
        phone (Optional[str]): Phone number of the sender or receiver.
        email (Optional[str]): Email address of the sender or receiver.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    client_id: Optional[str] = Field(
        None, description="ID пользователя на стороне интеграции"
    )
    avatar: Optional[str] = Field(None, description="Ссылка на аватар")
    phone: Optional[str] = Field(None, description="Телефон пользователя")
    email: Optional[str] = Field(None, description="Email пользователя")


class MessageModel(BaseModel):
    """
    Class representing a message in a chat system.

    Attributes:
        id (str): Unique identifier for the message in the chat system.
        client_id (Optional[str]): ID of the message on the integration side.
        type (str): Type of the message (e.g., text, image, etc.).
        text (str): Content of the message.
        media (str): URL to the media file associated with the message.
        thumbnail (str): URL to the thumbnail of the media file.
        file_name (str): Name of the file associated with the message.
        file_size (int): Size of the file in bytes.
        media_group_id (Optional[str]): ID of the media group for related files.
    """

    id: str = Field(..., description="ID сообщения в системе чатов")
    client_id: Optional[str] = Field(
        None, description="ID сообщения на стороне интеграции"
    )  # Изменено
    type: str = Field(..., description="Тип сообщения")
    text: str = Field(..., description="Текст сообщения")
    media: str = Field(default="", description="Ссылка на медиафайл")
    thumbnail: str = Field(default="", description="Ссылка на превью")
    file_name: str = Field(default="", description="Имя файла")
    file_size: int = Field(default=0, description="Размер файла в байтах")
    media_group_id: Optional[str] = Field(None, description="ID группы медиафайлов")


class MessageItem(BaseModel):
    """
    Class representing a message item, which includes message details and sender/receiver information.

    Attributes:
        timestamp (int): Timestamp of when the message was sent.
        sender (SenderReceiverBase): Sender information.
        receiver (Optional[SenderReceiverBase]): Receiver information (if applicable).
        message (MessageModel): The actual message data.
    """

    timestamp: int = Field(..., description="Временная метка сообщения")
    sender: SenderReceiverBase = Field(..., description="Отправитель сообщения")
    receiver: Optional[SenderReceiverBase] = Field(
        None, description="Получатель сообщения"
    )
    message: MessageModel = Field(..., description="Данные сообщения")


class HistoryResponse(BaseModel):
    """
    Class representing a chat response, which contains a list of message items.

    Attributes:
        messages (List[MessageItem]): A list of message items in the chat.
    """

    messages: List[MessageItem] = Field(..., description="Список сообщений")
