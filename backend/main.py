from fastapi import FastAPI
from backend.ai import get_recommendation


app = FastAPI()

data = {
    "scenes": [
        {
            "number": 17,
            "name": "Opening Scene",
            "equipment": ["Camera 01"],
            "status": "complete"
        },
        {
            "number": 18,
            "name": "Night Chase",
            "equipment": ["Camera 03"],
            "status": "delayed"
        },
        {
            "number": 19,
            "name": "Final Shot",
            "equipment": ["Camera 02"],
            "status": "waiting"
        }
    ],

    "crew_present": 38,
    "crew_total": 40,
    "equipment": [
        {"name": "Camera 01", "status": "online"},
        {"name": "Camera 02", "status": "online"},
        {"name": "Camera 03", "status": "offline"}
    ],
    "delay": 45
}

def check_incident():
    for item in data["equipment"]:
        if item["status"] == "offline":
            for scene in data["scenes"]:
                if item["name"] in scene["equipment"]:
                    return item["name"] + " Failure - Scene " + str(scene["number"])

            return item["name"] + " Failure"

    return "No active incidents"


@app.get("/")
def home():
    return {"message": "FilmOps AI is running"}


@app.get("/production")
def production():
    working = 0

    for item in data["equipment"]:
        if item["status"] == "online":
            working += 1

    data["equipment_working"] = working
    data["equipment_total"] = len(data["equipment"])
    data["incident"] = check_incident()

    data["recommendation"] = get_recommendation(
    data["incident"],
    data["delay"]
)

    return data