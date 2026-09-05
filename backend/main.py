from fastapi import FastAPI

app = FastAPI()

data = {
    "scenes": 24,
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

    return data