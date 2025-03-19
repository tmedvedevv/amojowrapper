import json

from amojowrapper.actions.chat.schemes import Source, User, Profile
from amojowrapper.actions.chat.schemes import ChatRequest, ChatResponse


class ChatAction:
    """
    A class to handle chat-related actions such as creating a new chat conversation.

    This class provides methods to interact with the Amojo API for chat operations.
    It initializes with a client and scope_id, and offers a method to create a chat.

    Attributes:
        client (AmojoClient): The Amojo client instance for interacting with the API.
        scope_id (str): A combination of channel ID and account token.
    """

    def __init__(self, client: "AmojoClient"):
        """
        Initializes the ChatAction instance with a client and scope_id.

        :param client: The Amojo client instance for interacting with the API.
        """
        self.client = client  # amojo_client
        # Scope ID is a combination of channel ID and account token
        self.scope_id = f"{self.client.channel_id}_{self.client.amojo_account_token}"

    def create(self, **kwargs) -> ChatResponse:
        """
        Creates a new chat conversation with the provided details.

        This method takes various optional parameters to create a chat conversation.
        It handles the creation of a `Source` and `Profile` object if certain
        parameters are provided, and then sends a request to create the chat.

        :param kwargs: Contains optional parameters for creating a chat.
            Possible parameters include:
            - conversation_id (str): The ID of the conversation.
            - source_external_id (str): The external ID for the source of the chat.
            - user_id (str): The ID of the user participating in the chat.
            - user_name (str): The name of the user.
            - user_avatar (str): The URL of the user's avatar.
            - user_profile_link (str): The link to the user's profile.
            - user_profile_phone (str): The phone number of the user.
            - user_profile_email (str): The email of the user.

        :return: A `ChatResponse` object containing the server's response data,
            including information about the chat and user.
        """
        # Handling the source (if external_id is provided, create a Source object)
        external_id = kwargs.get("source_external_id")
        source = Source(external_id=external_id) if external_id is not None else None

        # Handling the profile (if phone or email is provided, create a Profile object)
        phone = kwargs.get("user_profile_phone")
        email = kwargs.get("user_profile_email")
        profile = (
            Profile(phone=phone, email=email)
            if (phone is not None or email is not None)
            else None
        )

        # Creating the payload for the chat request
        payload = ChatRequest(
            conversation_id=kwargs.get("conversation_id"),
            source=source,
            user=User(
                id=kwargs.get("user_id"),
                name=kwargs.get("user_name"),
                avatar=kwargs.get("user_avatar"),
                profile=profile,
                profile_link=kwargs.get("user_profile_link"),
            ),
        )

        # Serialize the payload while excluding None values
        json_payload = json.loads(payload.model_dump_json(exclude_none=True))

        # Making the POST request to create the chat
        response: dict = self.client.custom_request(
            method="POST",
            endpoint=f"/v2/origin/custom/{self.scope_id}/chats",
            data=json_payload,
        ).json()

        # Returning the response as a ChatResponse object
        return ChatResponse(**response)
