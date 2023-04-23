import os

from app.config.netgear import NetgearConfig


def test_should_return_netgear_config_when_valid_input_given():
    # given
    os.environ["SERVER_IP"] = "192.168.1.240"
    os.environ["SERVER_PORT"] = "11118"
    os.environ["TIMEOUT"] = "10"
    os.environ["MAX_RETRIES"] = "20"
    os.environ["IS_COPY"] = "True"
    os.environ["IS_COMPRESSION"] = "False"

    # when
    config = NetgearConfig.load()

    # then
    assert config.ip_addr == "192.168.1.240", "ip addr error"
    assert type(config.port) is int and config.port == 11118, "port error"
    assert type(config.timeout) is int and config.timeout == 10, "timeout error"
    assert type(config.max_retries) is int  and config.max_retries == 20, "max_retries error"
    assert type(config.is_copy) is bool and config.is_copy == True, "is_copy error"
    assert type(config.is_compression) is bool and config.is_compression == False, "is_compression error"



def test_should_return_netgear_option_when_valid_input_given():
    # given
    os.environ["SERVER_IP"] = "192.168.1.240"
    os.environ["SERVER_PORT"] = "11118"
    os.environ["TIMEOUT"] = "10"
    os.environ["MAX_RETRIES"] = "20"
    os.environ["IS_COPY"] = "True"
    os.environ["IS_COMPRESSION"] = "False"

    # when
    option = NetgearConfig.load().option

    # then
    assert type(option) is dict, "option is not dict type"
    for key in ["max_retries", "request_timeout", "copy", "jpeg_compression"]:
        assert key  in option.keys(), f"{key} is not option properties"
