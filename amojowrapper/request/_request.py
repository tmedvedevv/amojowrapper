from abc import ABC, abstractmethod
from typing import Optional, Dict
import requests
import sys
from amojowrapper import __version__


class AbstractBaseRequest(ABC):
    """
    Abstract class for performing HTTP requests with logging.
    """

    @classmethod
    @abstractmethod
    def request(
        cls, url: str, method: str, headers: Dict[str, str], data: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Performs an HTTP request.

        :param url: The URL to send the request to.
        :param method: The HTTP method (GET, POST, PATCH, PUT, DELETE).
        :param headers: The headers to include in the request.
        :param data: The data to send in the request body (optional).
        :return: The response as a dictionary, or None if an error occurs.
        """
        pass

    @classmethod
    def _send_request(
        cls,
        method: str,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, str]],
    ) -> requests.Response:
        """
        Sends an HTTP request.

        :param method: The HTTP method (GET, POST, PATCH, PUT, DELETE).
        :param url: The URL to send the request to.
        :param headers: The headers to include in the request.
        :param data: The data to send in the request body (optional).
        :return: The response from the server.
        :raises ValueError: If the HTTP method is unsupported.
        """
        method_map = {
            "GET": requests.get,
            "POST": requests.post,
            "PATCH": requests.patch,
            "PUT": requests.put,
            "DELETE": requests.delete,
        }

        if method not in method_map:
            raise ValueError(f"Unsupported HTTP method: {method}")

        identifier = f"amojowrapper/{__version__}"  # Переименовано в snake_case
        headers.update({"User-Agent": identifier})

        try:
            return method_map[method](url, headers=headers, json=data)
        except KeyboardInterrupt:
            print("User interrupt. Exiting.")
            sys.exit()  # Использование sys.exit вместо exit
