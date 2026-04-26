from config import settings


def test_env_bool_uses_default_when_variable_is_missing(monkeypatch):
    monkeypatch.delenv("BILLETTERIE_TEST_BOOL", raising=False)

    assert settings.env_bool("BILLETTERIE_TEST_BOOL", default=True) is True


def test_env_bool_parses_enabled_values(monkeypatch):
    monkeypatch.setenv("BILLETTERIE_TEST_BOOL", "yes")

    assert settings.env_bool("BILLETTERIE_TEST_BOOL") is True


def test_env_bool_rejects_unknown_values(monkeypatch):
    monkeypatch.setenv("BILLETTERIE_TEST_BOOL", "no")

    assert settings.env_bool("BILLETTERIE_TEST_BOOL", default=True) is False


def test_env_list_uses_default_when_variable_is_missing(monkeypatch):
    default_hosts = ["localhost", "testserver"]
    monkeypatch.delenv("BILLETTERIE_TEST_HOSTS", raising=False)

    assert settings.env_list("BILLETTERIE_TEST_HOSTS", default_hosts) == default_hosts


def test_env_list_ignores_blank_items(monkeypatch):
    monkeypatch.setenv("BILLETTERIE_TEST_HOSTS", "localhost, ,testserver")

    assert settings.env_list("BILLETTERIE_TEST_HOSTS", []) == [
        "localhost",
        "testserver",
    ]
