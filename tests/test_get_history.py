from amojowrapper.actions import HistoryAction
from tests.helpers import handle_response


def test_set_delivery(amojo_client_fixture):
    conversation_ref_id = "b6893a27-a78c-4d49-8710-ba777ce96001"
    history = HistoryAction(amojo_client_fixture)
    result = history.get(conversation_ref_id=conversation_ref_id)
    if amojo_client_fixture.debug:
        handle_response(result)
