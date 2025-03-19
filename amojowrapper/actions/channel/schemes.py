from pydantic import BaseModel, Field


class ChannelResponseSchema(BaseModel):
    """
    Schema representing the response for a channel connection.

    This model is used to validate and structure the data returned
    by the API when interacting with a channel.
    """

    account_id: str = Field(..., description="The account ID in the chat API")

    hook_api_version: str = Field(
        ...,
        description="The version of the hook format that will be used by the integration when receiving outgoing messages. "
        "The hook URL should be configured in the chat channel settings for the specified version.",
    )

    title: str = Field(
        ..., description="The displayed name of the channel in the connected account"
    )

    scope_id: str = Field(
        ...,
        description="The identifier for the channel connection for a specific account",
    )

    is_time_window_disabled: bool = Field(
        default=False,
        description="Indicates whether the time window for messages is disabled",
    )
