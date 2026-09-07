from agents.schedule import check_schedule

scenes = [
    {
        "number": 17,
        "name": "Opening Scene",
        "status": "complete"
    },
    {
        "number": 18,
        "name": "Night Chase",
        "status": "delayed"
    },
    {
        "number": 19,
        "name": "Final Shot",
        "status": "waiting"
    }
]

result = check_schedule(
    scenes,
    "Camera 03 Failure - Scene 18",
    45
)

print(result)