from amojowrapper.actions import ChannelAction


def test_actions_channel_disconnect(amojo_client_fixture):
    channel = ChannelAction(amojo_client_fixture)
    channel.disconnect()
