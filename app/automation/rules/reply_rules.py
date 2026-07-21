"""
Reply Rules

Maps AI reply analysis into executable automation workflows.
"""

from app.automation.enums.action_type import ActionType
from app.automation.enums.automation_priority import (
    AutomationPriority,
)

from app.automation.schemas.automation_action_schema import (
    AutomationAction,
)

from app.automation.schemas.automation_result_schema import (
    AutomationResult,
)

from app.leads.enums.lead_status import (
    LeadStatus,
)

from app.reply_intelligence.enums.reply_intent import (
    ReplyIntent,
)

from app.reply_intelligence.schemas.reply_analysis_schema import (
    ReplyAnalysis,
)


class ReplyRules:
    """
    Converts reply analysis into automation actions.
    """

    @staticmethod
    def determine_actions(
        analysis: ReplyAnalysis,
        lead_id: int,
        conversation_id: int,
    ) -> AutomationResult:

        actions: list[AutomationAction] = []

        match analysis.intent:

            # =====================================================
            # Interested
            # =====================================================

            case ReplyIntent.INTERESTED:

                actions.extend(

                    [

                        AutomationAction(

                            action=ActionType.UPDATE_LEAD,

                            priority=AutomationPriority.HIGH,

                            description="Mark lead as qualified.",

                            payload={

                                "lead_id": lead_id,

                                "status": LeadStatus.QUALIFIED,

                            },
                        ),

                        AutomationAction(

                            action=ActionType.NOTIFY_SALES,

                            priority=AutomationPriority.HIGH,

                            description="Notify sales representative.",

                            payload={

                                "lead_id": lead_id,

                                "message": analysis.reason,

                            },
                        ),

                        AutomationAction(

                            action=ActionType.GENERATE_REPLY,

                            priority=AutomationPriority.MEDIUM,

                            description="Generate meeting follow-up.",

                            payload={

                                "conversation_id": conversation_id,

                            },
                        ),

                    ]

                )

            # =====================================================
            # Meeting Requested
            # =====================================================

            case ReplyIntent.MEETING_REQUEST:

                actions.extend(

                    [

                        AutomationAction(

                            action=ActionType.CREATE_MEETING,

                            priority=AutomationPriority.CRITICAL,

                            description="Create meeting.",

                            payload={

                                "conversation_id": conversation_id,

                            },
                        ),

                        AutomationAction(

                            action=ActionType.NOTIFY_SALES,

                            priority=AutomationPriority.CRITICAL,

                            description="Notify sales immediately.",

                            payload={

                                "lead_id": lead_id,

                                "message": analysis.reason,

                            },
                        ),

                    ]

                )

            # =====================================================
            # Needs Information
            # =====================================================

            case ReplyIntent.NEEDS_INFORMATION:

                actions.append(

                    AutomationAction(

                        action=ActionType.GENERATE_REPLY,

                        priority=AutomationPriority.HIGH,

                        description="Generate information response.",

                        payload={

                            "conversation_id": conversation_id,

                        },
                    )

                )

            # =====================================================
            # Follow Up Later
            # =====================================================

            case ReplyIntent.FOLLOW_UP_LATER:

                actions.append(

                    AutomationAction(

                        action=ActionType.SCHEDULE_FOLLOW_UP,

                        priority=AutomationPriority.MEDIUM,

                        description="Schedule future follow-up.",

                        payload={

                            "lead_id": lead_id,

                        },
                    )

                )

            # =====================================================
            # Out Of Office
            # =====================================================

            case ReplyIntent.OUT_OF_OFFICE:

                actions.append(

                    AutomationAction(

                        action=ActionType.SCHEDULE_FOLLOW_UP,

                        priority=AutomationPriority.LOW,

                        description="Retry after out-of-office period.",

                        payload={

                            "lead_id": lead_id,

                        },
                    )

                )

            # =====================================================
            # Not Interested
            # =====================================================

            case ReplyIntent.NOT_INTERESTED:

                actions.extend(

                    [

                        AutomationAction(

                            action=ActionType.UPDATE_LEAD,

                            priority=AutomationPriority.HIGH,

                            description="Mark lead as lost.",

                            payload={

                                "lead_id": lead_id,

                                "status": LeadStatus.LOST,

                            },
                        ),

                    ]

                )

            # =====================================================
            # Already Customer
            # =====================================================

            case ReplyIntent.ALREADY_CUSTOMER:

                actions.append(

                    AutomationAction(

                        action=ActionType.UPDATE_LEAD,

                        priority=AutomationPriority.HIGH,

                        description="Mark as existing customer.",

                        payload={

                            "lead_id": lead_id,

                            "status": LeadStatus.WON,

                        },
                    )

                )

            # =====================================================
            # Already Using AI
            # =====================================================

            case ReplyIntent.ALREADY_USING_AI:

                actions.append(

                    AutomationAction(

                        action=ActionType.UPDATE_LEAD,

                        priority=AutomationPriority.MEDIUM,

                        description="Record existing AI adoption.",

                        payload={

                            "lead_id": lead_id,

                            "status": LeadStatus.CONTACTED,

                        },
                    )

                )

            # =====================================================
            # Default
            # =====================================================

            case _:

                actions.append(

                    AutomationAction(

                        action=ActionType.NO_ACTION,

                        priority=AutomationPriority.LOW,

                        description="No automation required.",

                    )

                )

        return AutomationResult(
            actions=actions,
        )