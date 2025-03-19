import hashlib
import hmac
import datetime


class AmojoHeaderBuilder:
    """
    Class for step-by-step building of HTTP request headers.
    """

    def __init__(self):
        self.headers: dict[str, str] = {}

    def add_date(self) -> "AmojoHeaderBuilder":
        """
        Adds the Date header.
        """
        # Используем timezone-aware объект для представления времени в UTC
        date = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        self.headers["Date"] = date
        return self

    def add_content_type(
        self, content_type: str = "application/json"
    ) -> "AmojoHeaderBuilder":
        """
        Adds the Content-Type header.
        """
        self.headers["Content-Type"] = content_type
        return self

    def add_content_md5(self, payload: str) -> "AmojoHeaderBuilder":
        """
        Adds the Content-MD5 header.
        """
        self.headers["Content-MD5"] = hashlib.md5(payload.encode()).hexdigest()
        return self

    def add_signature(
        self, channel_secret: str, method: str, endpoint: str, payload: str
    ) -> "AmojoHeaderBuilder":
        """
        Adds the X-Signature header.
        """
        sign = "\n".join(
            [
                method,
                self.headers["Content-MD5"],
                self.headers["Content-Type"],
                self.headers["Date"],
                endpoint,
            ]
        )
        signature = hmac.new(
            channel_secret.encode(), sign.encode(), hashlib.sha1
        ).hexdigest()
        self.headers["X-Signature"] = signature
        return self

    def build(self) -> dict[str, str]:
        """
        Returns the final dictionary of headers.
        """
        return self.headers
