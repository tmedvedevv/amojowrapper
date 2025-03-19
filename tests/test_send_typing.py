from amojowrapper.actions import TypingAction


def test_set_react(amojo_client_fixture):
    conversation_ref_id = "helloworld_test"
    sender_id = "new_user-mazharreal"

    typing = TypingAction(amojo_client_fixture)
    typing.send(conversation_id=conversation_ref_id, sender_id=sender_id)
