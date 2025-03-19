import hashlib
import hmac


class WebhookValidator:
    """
    This class is responsible for validating the webhook signature using HMAC SHA-1 hashing.

    It compares the signature sent with the webhook request (x_signature) against a generated
    hash from the payload and a secret key, ensuring the authenticity of the webhook request.
    """

    def __init__(self, client):
        """
        Initializes the WebhookValidator with the client.

        Args:
            client (object): The client object that holds the channel secret.
        """
        self.client: object = client

    def validate(self, payload: str, x_signature: str) -> bool:
        """
        Validates the webhook by comparing the calculated HMAC signature to the provided one.

        Args:
            payload (str): The raw webhook payload.
            x_signature (str): The signature sent with the webhook request.

        Returns:
            bool: True if the signatures match, indicating a valid webhook; False otherwise.
        """
        payload: str = payload.strip("\r\n")
        hash_result: str = hmac.new(
            self.client.channel_secret.encode(), payload.encode(), hashlib.sha1
        ).hexdigest()
        return hash_result == x_signature
