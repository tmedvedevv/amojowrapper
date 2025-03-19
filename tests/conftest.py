import pytest
from amojowrapper.client import AmojoClient
from helpers import get_env
from collections import deque
from pprint import pprint


def pytest_addoption(parser):
    """
    Add a command-line option --amojo-debug to enable debug mode for AmojoClient.
    """
    parser.addoption(
        "--amojo-debug", action="store_true", help="Enable debug mode for AmojoClient"
    )


def pytest_collection_modifyitems(config, items):
    """
    Hook to modify the order of test execution using a queue.
    Prioritizes specific tests to run first or last.
    """
    # Create a queue to manage the order of tests
    test_queue = deque()

    # Define priority tests and their desired positions
    priority_tests = {
        "test_actions_channel_connect": 0,  # Should run first
        "test_actions_channel_disconnect": -1,  # Should run last
    }

    # Iterate through all tests and add them to the queue
    for item in items:
        if item.name in priority_tests:
            # If the test is prioritized, add it to the queue at the specified position
            position = priority_tests[item.name]
            if position == 0:
                test_queue.appendleft(item)  # Add to the beginning
            elif position == -1:
                test_queue.append(item)  # Add to the end
            print(f" - {item.name} added to the queue at position {position}.")
        else:
            # Add other tests to the queue in their original order
            test_queue.insert(1, item)

    # Convert the queue back to a list
    items[:] = list(test_queue)

    # Print the final order of tests
    print("Final test order:")
    pprint(items)


@pytest.fixture(scope="session")
def amojo_client_fixture(request):
    """
    Fixture to create an AmojoClient instance with data from .pytest.env.
    Supports debug mode via the --amojo-debug command-line option.
    """
    debug_mode = request.config.getoption(
        "--amojo-debug"
    )  # Get the value of --amojo-debug

    return AmojoClient(
        referer=get_env("referer"),
        amojo_account_token=get_env("amojo_account_token"),
        channel_secret=get_env("channel_secret"),
        channel_id=get_env("channel_id"),
        debug=debug_mode,  # Pass the debug mode value
    )
