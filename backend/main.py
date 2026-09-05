from fastapi import FastAPI

app = FastAPI()

data = {
    "scenes": 24,
    "crew_present": 38,
    "crew_total": 40,
    "equipment_working": 12,
    "equipment_total": 13,
    "delay": 45,
    "incident": "Camera 03 Failure"
}


@app.get("/")
def home():
    return {"message": "FilmOps AI is running"}


@app.get("/production")
def production():
    return data