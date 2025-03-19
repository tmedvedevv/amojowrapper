from amojowrapper.actions import MessageAction
from tests.helpers import handle_response


def test_edit_message_text(amojo_client_fixture):
    conversation_ref_id = "b6893a27-test-4d49-8710-ba777ce96001"
    sender_ref_id = "cb6cf2cb-test-46db-bd00-5083a5b98a51"
    msgid = "amojowrapper_msgid_1ecac67d-test-414b-afea-4e274fec4d7e"
    message_type = "text"
    message_text = "1"

    message = MessageAction(amojo_client_fixture)
    result = message.edit(
        msgid=msgid,
        message_type=message_type,
        message_text=message_text,
        conversation_ref_id=conversation_ref_id,
        sender_ref_id=sender_ref_id,
    )

    if amojo_client_fixture.debug:
        handle_response(result)
