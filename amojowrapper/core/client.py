import json
from typing import Dict
from requests import Response
from amojowrapper.request import CustomRequest

from amojowrapper.helpers.endpoint import AmojoEndpoint
from amojowrapper.helpers.headers import AmojoHeaderBuilder


class AbstractAmojoClient:
    """
    Represents a client to interact with the amoCRM API.

    This class provides methods to make HTTP requests to the AmoCRM API using the
    specified channel credentials and configuration.

    Attributes:
        channel_secret: The secret key for the channel.
        channel_id: The unique identifier for the channel.
        amojo_base_url: The base URL for AmoCRM API.
        amojo_account_token: The account token for the AmoCRM API.
        debug: A flag to enable or disable debugging output.
    """

    def __init__(
        self,
        channel_secret: str,
        channel_id: str,
        referer: str,
        amojo_account_token: str,
        debug: bool = False,
    ):
        """
        Initializes the AbstractAmojoClient with the necessary credentials and configurations.

        Args:
            channel_secret (str): The secret key for the channel.
            channel_id (str): The unique identifier for the channel.
            referer (str): The referer to get the base URL.
            amojo_account_token (str): The account token for the AmoCRM API.
            debug (bool): A flag to enable or disable debugging output. Default is False.
        """
        self.channel_secret = channel_secret
        self.channel_id = channel_id
        self.amojo_base_url = AmojoEndpoint(referer=referer).get_base_url()
        self.amojo_account_token = amojo_account_token
        self.debug = debug

    def _request(
        self, method: str, endpoint: str, data: Dict = None, debug: bool = False
    ) -> Response:
        """
        Executes an HTTP request to the AmoCRM API.

        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The endpoint of the AmoCRM API.
            data (Dict, optional): The payload data for the request. Defaults to None.
            debug (bool, optional): Whether to enable debug output. Defaults to False.

        Returns:
            Response: The response object from the HTTP request.
        """
        payload_str = json.dumps(data)

        headers = (
            AmojoHeaderBuilder()
            .add_date()
            .add_content_type()
            .add_content_md5(payload_str)
            .add_signature(self.channel_secret, method, endpoint, payload_str)
            .build()
        )

        url = f"{self.amojo_base_url}{endpoint}"

        return CustomRequest.request(
            method=method, url=url, headers=headers, data=data, debug=debug
        )
