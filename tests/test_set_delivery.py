from amojowrapper.actions import DeliveryStatusAction


def test_set_delivery(amojo_client_fixture):
    delivery = DeliveryStatusAction(amojo_client_fixture)
    delivery.set(
        msgid="ccc0ccdd-ef14-4d87-9281-5f5656685d3d",
        delivery_status=-1,
        error_code=905,
        error="test222",
    )
