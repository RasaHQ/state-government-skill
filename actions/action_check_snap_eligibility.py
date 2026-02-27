"""Action to check SNAP eligibility via (mock) logic.

Uses approximate federal SNAP gross income limits for Georgia (FFY 2025).
These are illustrative — real eligibility depends on many additional factors.
"""

import asyncio
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Federal SNAP gross monthly income limits (130% of poverty level)
# Household size -> max gross monthly income
SNAP_INCOME_LIMITS = {
    1: 1580,
    2: 2137,
    3: 2694,
    4: 3250,
    5: 3807,
    6: 4364,
    7: 4921,
    8: 5478,
}


class ActionCheckSnapEligibility(Action):
    """Check SNAP eligibility based on household size and income."""

    def name(self) -> Text:
        return "action_check_snap_eligibility"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(1.0)

        household_size = tracker.get_slot("household_size")
        monthly_income = tracker.get_slot("monthly_income")

        if household_size is None or monthly_income is None:
            return [
                SlotSet("snap_eligible", None),
                SlotSet("api_error", True),
            ]

        household_size = int(household_size)
        monthly_income = float(monthly_income)

        # For households larger than 8, add $557 per additional member
        if household_size <= 8:
            income_limit = SNAP_INCOME_LIMITS.get(household_size)
        else:
            income_limit = SNAP_INCOME_LIMITS[8] + (household_size - 8) * 557

        if income_limit is None:
            return [
                SlotSet("snap_eligible", None),
                SlotSet("api_error", True),
            ]

        eligible = monthly_income <= income_limit

        return [
            SlotSet("snap_eligible", eligible),
            SlotSet("api_error", False),
        ]
