"""
Automation Handler Registry.

Maps automation action types to their handler implementations.
"""

from app.automation.enums.action_type import (
    ActionType,
)

from app.automation.handlers.base_handler import (
    BaseAutomationHandler,
)

from app.automation.handlers.create_meeting_handler import (
    CreateMeetingHandler,
)

from app.automation.handlers.generate_reply_handler import (
    GenerateReplyHandler,
)

from app.automation.handlers.notify_sales_handler import (
    NotifySalesHandler,
)

from app.automation.handlers.schedule_follow_up_handler import (
    ScheduleFollowUpHandler,
)

from app.automation.handlers.update_lead_handler import (
    UpdateLeadHandler,
)


HANDLER_REGISTRY: dict[
    ActionType,
    type[BaseAutomationHandler],
] = {

    #
    # Lead Management
    #

    ActionType.UPDATE_LEAD:
        UpdateLeadHandler,

    #
    # AI Reply Generation
    #

    ActionType.GENERATE_REPLY:
        GenerateReplyHandler,

    #
    # Notifications
    #

    ActionType.NOTIFY_SALES:
        NotifySalesHandler,

    #
    # Scheduling
    #

    ActionType.SCHEDULE_FOLLOW_UP:
        ScheduleFollowUpHandler,

    #
    # Meetings
    #

    ActionType.CREATE_MEETING:
        CreateMeetingHandler,

}