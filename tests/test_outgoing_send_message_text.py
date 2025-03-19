from amojowrapper.actions import MessageAction
from tests.helpers import handle_response


def test_outgoing_send_message_text(amojo_client_fixture):
    conversation_ref_id = "b6893a27-test-4d49-8710-ba777ce96001"
    receiver_ref_id = "cb6cf2cb-71e8-test-bd00-5083a5b98a51"
    sender_ref_id = "a984adf2-a7a2-test-a045-88bcd53c7f3c"
    message_type = "text"
    message_text = "outgoing chat message"

    message = MessageAction(amojo_client_fixture)
    result = message.send(
        message_type=message_type,
        message_text=message_text,
        conversation_ref_id=conversation_ref_id,
        sender_ref_id=sender_ref_id,
        receiver_ref_id=receiver_ref_id,
        silent=True,
    )

    if amojo_client_fixture.debug:
        handle_response(result)
