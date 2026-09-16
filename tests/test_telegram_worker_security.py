import pytest

import telegram_bot_worker


def test_telegram_worker_refuses_to_start_when_delivery_is_disabled(monkeypatch):
    monkeypatch.setitem(
        telegram_bot_worker.app.config,
        "NOTIFICATION_DELIVERY_ENABLED",
        False,
    )

    with pytest.raises(RuntimeError, match="disabled by application configuration"):
        telegram_bot_worker.run_worker()
