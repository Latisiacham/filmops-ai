from backend.adk_ai import get_adk_recommendation


async def make_decision(equipment_result, schedule_result):
    incident = ""

    if equipment_result["offline"]:
        incident = (
            "Offline equipment: "
            + ", ".join(equipment_result["offline"])
            + ". Available equipment: "
            + ", ".join(equipment_result["available"])
        )

    if schedule_result["affected_scene"]:
        incident += (
            ". Affected scene: "
            + schedule_result["affected_scene"]
        )

    try:
        return await get_adk_recommendation(
            incident,
            schedule_result["delay"]
        )

    except Exception:
        return (
            "AI recommendation is temporarily unavailable. "
            "Continue the production recovery plan while the AI service reconnects."
        )