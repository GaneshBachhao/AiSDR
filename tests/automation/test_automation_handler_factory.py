from pytest import raises

from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.handlers.automation_handler_factory import (
    AutomationHandlerFactory,
)

from app.automation.handlers.update_lead_handler import (
    UpdateLeadHandler,
)


def test_factory_returns_handler():

    handler = AutomationHandlerFactory.get_handler(
        ActionType.UPDATE_LEAD,
    )

    assert isinstance(
        handler,
        UpdateLeadHandler,
    )


def test_unknown_handler():

    class FakeAction:
        pass

    with raises(ValueError):

        AutomationHandlerFactory.get_handler(
            FakeAction(),
        )