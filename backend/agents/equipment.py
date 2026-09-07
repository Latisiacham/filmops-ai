def check_equipment(equipment):
    offline = []
    available = []

    for item in equipment:
        if item["status"] == "offline":
            offline.append(item["name"])

        if item["status"] == "online":
            available.append(item["name"])

    return {
        "offline": offline,
        "available": available
    }