from amojowrapper.actions import MessageAction
from tests.helpers import handle_response


def test_reply_client_msgid(amojo_client_fixture):

    message_type = "text"
    message_text = "test_reply"
    conversation_id = "sfafsaf-47a0-9a7b-9a4820228bd0"
    sender_id = "safa-6c48-4bd2-a975-fd7b75956b85"
    reply_to_msgid = "client_hello24"
    silent = False

    message = MessageAction(amojo_client_fixture)
    result = message.send(
        message_type=message_type,
        message_text=message_text,
        conversation_id=conversation_id,
        sender_id=sender_id,
        reply_to_msgid=reply_to_msgid,
        silent=silent,
    )

    if amojo_client_fixture.debug:
        handle_response(result)
