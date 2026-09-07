def check_schedule(scenes, incident, delay):
    affected_scene = None

    for scene in scenes:
        if "Scene " + str(scene["number"]) in incident:
            affected_scene = scene["name"]

    return {
        "affected_scene": affected_scene,
        "delay": delay
    }