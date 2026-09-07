from backend.ai import get_recommendation


def make_decision(equipment_result, schedule_result):
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

    return get_recommendation(
        incident,
        schedule_result["delay"]
    )