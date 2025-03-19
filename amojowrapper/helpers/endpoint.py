import re


class AmojoEndpoint:
    """
    A class to handle the base URL construction for the AmoCRM API.

    This class takes the referer URL, processes it to extract the domain segment,
    and constructs the corresponding base URL for AmoCRM.

    Attributes:
        referer (str): The referer URL (e.g., example.amocrm.ru).
    """

    def __init__(self, referer: str):
        """
        Initializes the AmojoEndpoint with the given referer URL.

        Args:
            referer (str): The referer URL to be processed (e.g., example.amocrm.ru).
        """
        self.referer: str = referer

    def get_base_url(self) -> str:
        """
        Constructs the base URL for the AmoCRM API based on the referer URL.

        The referer URL is processed to extract the domain part, and then the
        corresponding AmoCRM base URL is returned.

        Returns:
            str: The base URL for the amoCRM API (e.g., https://amojo.amocrm.ru).
        """
        segment = re.sub(r"^.*?\.", "", self.referer)
        return f"https://amojo.{segment}"
