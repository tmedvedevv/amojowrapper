from requests import Response, exceptions
from typing import Dict, Optional
from amojowrapper.request._request import AbstractBaseRequest
from amojowrapper.request.exceptions import RequestError


class CustomRequest(AbstractBaseRequest):
    """
    A custom HTTP request handler that performs requests, handles errors, and logs the responses.

    Inherits from AbstractBaseRequest and provides a method to send HTTP requests.
    It also includes error handling with logging support when debugging is enabled.
    """

    @classmethod
    def request(
        cls,
        url: str,
        method: str,
        headers: Dict[str, str],
        data: Optional[Dict] = None,
        debug: bool = False,
    ) -> Response:
        """
        Send an HTTP request and handle errors with optional logging for debugging.

        Args:
            url (str): The URL to which the request will be sent.
            method (str): The HTTP method (GET, POST, etc.).
            headers (dict): The headers to include in the request.
            data (dict, optional): The body of the request (default is None).
            debug (bool, optional): If True, enables logging for debugging (default is False).

        Returns:
            Response: The response object from the HTTP request.

        Raises:
            OAuthRequestError: If an HTTP error or request error occurs.
        """

        try:
            if debug:
                from loguru import logger  # Import inside the function for debug

            if debug:
                logger.info(f"Trying to request: {method} {url} {data}")

            # Send the actual request
            response = cls._send_request(
                method=method, url=url, headers=headers, data=data
            )

            # Raise an error for unsuccessful responses
            response.raise_for_status()

            if debug:
                logger.success(f"Response: {response.status_code}: {response.reason}")

            return response

        except exceptions.HTTPError as e:
            # Handle HTTP errors (e.g., 4xx, 5xx responses)
            __error_msg = f"HTTP error occurred: {e.response.reason} {e.response.status_code}: {method} {url}\n"
            __error_msg += f"Payload: {data}\nResponse: {e.response.content}\n {str(e)}"

            if debug:
                logger.critical(__error_msg)

            raise RequestError(__error_msg) from e

        except exceptions.RequestException as e:
            # Handle any request-related errors (e.g., network issues)
            __error_msg = f"Error during request: {method} {url}\nPayload: {data}\nError: {str(e)}"

            if debug:
                logger.critical(__error_msg)

            raise RequestError(__error_msg) from e
