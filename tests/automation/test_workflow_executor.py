from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)

from app.automation.schemas.automation_result_schema import (
    AutomationResult,
)

from app.automation.workflows.workflow_executor import (
    WorkflowExecutor,
)


def test_executor():

    executor = WorkflowExecutor()

    result = AutomationResult(

        actions=[

            AutomationAction(

                action=ActionType.NOTIFY_SALES,

                description="Notify sales",

            ),

            AutomationAction(

                action=ActionType.GENERATE_REPLY,

                description="Generate reply",

            ),
        ]
    )

    executed = executor.execute(

        db=None,

        result=result,

    )

    assert len(executed) == 2

    assert executed[0] == "NOTIFY_SALES"

    assert executed[1] == "GENERATE_REPLY"