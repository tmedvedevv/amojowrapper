from amojowrapper.actions import ReactAction


def test_set_react(amojo_client_fixture):
    conversation_ref_id = "b6893a27-test-4d49-8710-ba777ce96001"
    user_ref_id = "a984adf2-a7a2-4044-a045-88bcd53c7f3c"
    id = "ccc0ccdd-ef14-4d87-9281-5f5656685d3d"
    type = "react"
    emoji = "👍"

    react = ReactAction(amojo_client_fixture)
    react.set(
        conversation_ref_id=conversation_ref_id,
        user_ref_id=user_ref_id,
        id=id,
        type=type,
        emoji=emoji,
    )
