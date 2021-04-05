def test_error_status(error_msg):
    assert 'error' in error_msg.get('status', '')


def test_value_error(no_params_msg):
    assert 'Expecting value' in no_params_msg
