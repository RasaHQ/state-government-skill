"""Action to check driver's license status via (mock) API."""

import asyncio
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Mock license data - simulating what we'd get from a real Georgia DDS API
MOCK_LICENSE_DATA = {
    "class_c": "Active — expires 03/2028",
    "class_cp": "Expired — expired 11/2025",
    "class_d": "Suspended — contact DDS for details",
}


class ActionCheckLicenseStatus(Action):
    """Check driver's license status via (mock) API."""

    def name(self) -> Text:
        return "action_check_license_status"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Simulate API latency
        await asyncio.sleep(1.0)

        license_type = tracker.get_slot("license_type")

        if not license_type or license_type not in MOCK_LICENSE_DATA:
            return [
                SlotSet("license_status", None),
                SlotSet("api_error", True),
            ]

        status = MOCK_LICENSE_DATA[license_type]

        return [
            SlotSet("license_status", status),
            SlotSet("api_error", False),
        ]
