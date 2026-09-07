from agents.equipment import check_equipment

equipment = [
    {"name": "Camera 01", "status": "online"},
    {"name": "Camera 02", "status": "online"},
    {"name": "Camera 03", "status": "offline"}
]

result = check_equipment(equipment)

print(result)