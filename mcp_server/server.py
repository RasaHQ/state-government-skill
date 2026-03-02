# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp", "uvicorn"]
# ///
"""MCP server exposing Georgia state services tools."""

import random
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from fastmcp import FastMCP

mcp = FastMCP("Georgia Services MCP Server")

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


@mcp.tool()
def check_snap_eligibility(household_size: int, monthly_income: float) -> dict:
    """Check SNAP (food stamps) eligibility based on household size and income.

    Args:
        household_size: Number of people in the household.
        monthly_income: Total monthly gross household income in dollars.
    """
    if household_size < 1:
        return {"error": "Household size must be at least 1"}

    # For households larger than 8, add $557 per additional member
    if household_size <= 8:
        income_limit = SNAP_INCOME_LIMITS.get(household_size)
    else:
        income_limit = SNAP_INCOME_LIMITS[8] + (household_size - 8) * 557

    eligible = monthly_income <= income_limit

    return {
        "household_size": household_size,
        "monthly_income": monthly_income,
        "income_limit": income_limit,
        "eligible": eligible,
    }


def _generate_appointment_slots(
    start_date: datetime,
    end_date: datetime,
    start_hour: int,
    end_hour: int,
    excluded_dates: List[date],
) -> List[str]:
    """Generate up to 10 realistic DFCS office appointment slots."""
    slots: List[str] = []
    current = start_date
    business_start = max(start_hour, 8)
    business_end = min(end_hour, 17)

    if business_start >= business_end:
        business_start, business_end = 9, 17

    while len(slots) < 10 and current <= end_date:
        if current.weekday() < 5 and current.date() not in excluded_dates:
            hour = random.randint(business_start, business_end - 1)
            minute = random.choice([0, 15, 30, 45])
            appointment = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
            formatted = appointment.strftime("%-m/%-d at %-I:%M %p")
            if formatted not in slots:
                slots.append(formatted)
        current += timedelta(days=1)

    return slots[:10]


@mcp.tool()
def query_available_appointments(
    user_availability_start_date: str,
    user_availability_end_date: str,
    user_availability_start_time: str,
    user_availability_end_time: str,
    non_available_days: str,
) -> Dict[str, Any]:
    """Query available DFCS office appointment slots for SNAP services.

    Returns up to 10 available appointment slots within the specified criteria.

    Args:
        user_availability_start_date: Start date in mm/dd/yyyy format. Use 'any' if not specified.
        user_availability_end_date: End date in mm/dd/yyyy format. Use 'any' if not specified.
        user_availability_start_time: Start time in HH:MM 24-hour format. Use 'any' if not specified.
        user_availability_end_time: End time in HH:MM 24-hour format. Use 'any' if not specified.
        non_available_days: Dates user is NOT available, separated by ';' in mm/dd/yyyy format. Use 'any' if none.
    """
    # Defaults
    if not user_availability_start_date or user_availability_start_date.lower() == "any":
        user_availability_start_date = datetime.now().strftime("%m/%d/%Y")
    if not user_availability_end_date or user_availability_end_date.lower() == "any":
        try:
            start_dt = datetime.strptime(user_availability_start_date, "%m/%d/%Y")
        except ValueError:
            start_dt = datetime.now()
        user_availability_end_date = (start_dt + timedelta(days=14)).strftime("%m/%d/%Y")
    if not user_availability_start_time or user_availability_start_time.lower() == "any":
        user_availability_start_time = "09:00"
    if not user_availability_end_time or user_availability_end_time.lower() == "any":
        user_availability_end_time = "17:00"

    # Parse excluded dates
    excluded_dates: List[date] = []
    if non_available_days and non_available_days.lower() != "any":
        for ds in non_available_days.split(";"):
            ds = ds.strip()
            if ds:
                try:
                    excluded_dates.append(datetime.strptime(ds, "%m/%d/%Y").date())
                except ValueError:
                    pass

    try:
        start_datetime = datetime.strptime(user_availability_start_date, "%m/%d/%Y")
        end_datetime = datetime.strptime(user_availability_end_date, "%m/%d/%Y")
        start_hour = int(user_availability_start_time.split(":")[0])
        end_hour = int(user_availability_end_time.split(":")[0])

        available_slots = _generate_appointment_slots(
            start_datetime, end_datetime, start_hour, end_hour, excluded_dates,
        )

        return {
            "success": True,
            "available_slots": available_slots,
            "total_slots": len(available_slots),
            "message": f"Found {len(available_slots)} available DFCS appointment slots"
            if available_slots
            else "No appointments available in that range. Please try different dates.",
        }

    except (ValueError, Exception) as e:
        return {
            "success": False,
            "error": f"Error finding appointments: {e}",
            "available_slots": [],
        }


@mcp.tool()
def book_appointment(appointment_slot: str) -> Dict[str, Any]:
    """Book a DFCS office appointment at the specified time slot.

    Args:
        appointment_slot: The appointment slot to book, e.g. '3/5 at 1:00 PM'.
    """
    return {
        "success": True,
        "appointment_confirmed": True,
        "message": f"Your DFCS appointment has been booked for {appointment_slot}.",
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8090, path="/")
