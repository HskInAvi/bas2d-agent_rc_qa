import os

from app.config.redis import RedisConfig


def test_should_return_redis_config_when_valid_input_given():
    # given
    os.environ["REDIS_IP"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["REDIS_DB"] = "0"
    os.environ["AGENT_NO"] = "60"

    # when
    config = RedisConfig.load()

    # then
    assert type(config) is dict, "config type should be dict"
    for key in ["host", "port", "database", "channel"]:
        assert key in config.keys(), "{key} should be in config"
