from agents.production import make_decision

equipment_result = {
    "offline": ["Camera 03"],
    "available": ["Camera 01", "Camera 02"]
}

schedule_result = {
    "affected_scene": "Night Chase",
    "delay": 45
}

result = make_decision(
    equipment_result,
    schedule_result
)

print(result)