from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.enums.automation_priority import (
    AutomationPriority,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)

from app.automation.schemas.automation_result_schema import (
    AutomationResult,
)


def test_action():

    action = AutomationAction(

        action=ActionType.NOTIFY_SALES,

        priority=AutomationPriority.HIGH,

        description="Notify SDR",

    )

    assert action.action == ActionType.NOTIFY_SALES

    assert action.priority == AutomationPriority.HIGH


def test_result():

    result = AutomationResult()

    assert result.success

    assert result.actions == []

    assert result.warnings == []