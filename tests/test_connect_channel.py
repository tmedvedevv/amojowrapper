from amojowrapper.actions import ChannelAction
from helpers import handle_response


def test_actions_channel_connect(amojo_client_fixture):
    channel = ChannelAction(amojo_client_fixture)
    result = channel.connect()
    if amojo_client_fixture.debug:
        handle_response(result)
