from requests import Response
from amojowrapper.core.client import AbstractAmojoClient
from typing import Optional


class AmojoClient(AbstractAmojoClient):
    """
    This class is a wrapper around the AbstractAmojoClient for custom requests.

    It provides a method to perform HTTP requests to the AmoCRM API with the option
    to customize the request method, endpoint, and data. It inherits from AbstractAmojoClient
    and uses the internal `_request` method to send requests.
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
        Initializes the AmojoClient with the given credentials.

        Args:
            channel_secret (str): The secret key for the channel.
            channel_id (str): The ID of the channel.
            referer (str): The referer URL for the AmoCRM API.
            amojo_account_token (str): The token for the AmoCRM account.
            debug (bool, optional): Whether to enable debugging. Defaults to False.
        """
        super().__init__(
            channel_secret=channel_secret,
            channel_id=channel_id,
            referer=referer,
            amojo_account_token=amojo_account_token,
            debug=debug,
        )

    def custom_request(
        self,
        method: str = "GET",
        endpoint: Optional[str] = None,
        data: Optional[list] = None,
    ) -> Response:
        """
        Sends a custom HTTP request to the specified endpoint.

        Args:
            method (str): The HTTP method (GET, POST, etc.). Defaults to "GET".
            endpoint (Optional[str]): The API endpoint to request. Defaults to None.
            data (Optional[list]): The data to send with the request. Defaults to None.

        Returns:
            Response: The response object from the HTTP request.
        """
        if data is None:
            data = []

        return self._request(
            method=method, endpoint=endpoint, data=data, debug=self.debug
        )
