"""
The action.py module contains the ChannelAction class, which is responsible for managing channel connections and disconnections.
"""

from typing import Optional

from requests import Response

from amojowrapper.actions.channel.schemes import ChannelResponseSchema


class ChannelAction:
    """
    The ChannelAction class provides methods for connecting and disconnecting a channel.

    Attributes:
        client: An instance of AmojoClient for interacting with the API.
    """

    def __init__(self, client: "AmojoClient") -> None:
        """
        Initialize the ChannelAction instance.

        :param client: An instance of AmojoClient for making API requests.
        """
        self.client = client  # amojo_client, instance of the client for API requests

    def connect(
        self, hook_api_version: str = "v2", title: Optional[str] = None
    ) -> ChannelResponseSchema:
        """
        Establish a connection to the channel.

        :param hook_api_version: The version of the hook API to use. Defaults to "v2".
        :param title: Optional title for the connection.
        :return: An instance of ChannelResponseSchema containing the response data.
        """
        # Prepare the payload with the necessary data for the connection
        payload = {
            "hook_api_version": hook_api_version,
            "account_id": self.client.amojo_account_token,
        }

        # Add the title to the payload if provided
        if title is not None:
            payload["title"] = title

        # Make a POST request to establish the connection
        response: dict = self.client.custom_request(
            method="POST",
            endpoint=f"/v2/origin/custom/{self.client.channel_id}/connect",
            data=payload,
        ).json()

        # Return the response as a ChannelResponseSchema object
        return ChannelResponseSchema(**response)

    def disconnect(self) -> bool:
        """
        Disconnect the channel.

        :return: True if the disconnection was successful (status code 200), otherwise False.
        """
        # Prepare the payload with the account token for disconnection
        payload = {"account_id": self.client.amojo_account_token}

        # Make a DELETE request to disconnect the channel
        response: Response = self.client.custom_request(
            method="DELETE",
            endpoint=f"/v2/origin/custom/{self.client.channel_id}/disconnect",
            data=payload,
        )

        # Return True if the status code is 200 (successful disconnection)
        return response.status_code == 200
