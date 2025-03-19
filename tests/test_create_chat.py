from amojowrapper.actions import ChatAction
from helpers import handle_response


def test_create_chat(amojo_client_fixture):
    chat = ChatAction(amojo_client_fixture)

    conversation_id = "identify-8e3e7640-49af-4448-a2c6-d5a421f7f217"
    source_external_id = "source_1"
    user_id = "identify-1241251234"
    user_avatar = "https://avatars.githubusercontent.com/u/47181197?v=4"
    user_name = "Some Name"
    user_profile_phone = "2412512352"
    user_profile_email = "example.client@example.com"

    chat_response = chat.create(
        conversation_id=conversation_id,
        source_external_id=source_external_id,
        user_id=user_id,
        user_avatar=user_avatar,
        user_name=user_name,
        user_profile_phone=user_profile_phone,
        user_profile_email=user_profile_email,
    )

    if amojo_client_fixture.debug:
        handle_response(chat_response)
