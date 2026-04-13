from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify
from database import init_db, save_session, get_all_sessions
from keywords import SYMPTOM_MAP, SYMPTOM_DESCRIPTIONS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SACA - Smart Adaptive Clinical Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class SymptomInput(BaseModel):
    symptom_text: str

@app.post("/classify")
def classify_symptoms(data: SymptomInput):
    result = classify(data.symptom_text)
    save_session(
    symptom_text=data.symptom_text,
    symptoms=result["symptoms"],
    severity=result["severity"],
    severity_sw=result["severity_sw"],
    reason=result["reason"]
)
    return result

@app.get("/sessions")
def get_sessions():
    rows = get_all_sessions()
    return [
    {
        "id": row[0],
        "symptom_text": row[1],
        "symptoms_detected": row[2],
        "severity": row[3],
        "severity_sw": row[4],
        "reason": row[5],
        "timestamp": row[6]
    }
    for row in rows
]

@app.get("/keywords")
def get_keywords():
    seen = set()
    result = []
    for sw, code in SYMPTOM_MAP.items():
        if sw not in seen:
            seen.add(sw)
            result.append({
                "sw": sw,
                "en": SYMPTOM_DESCRIPTIONS.get(code, code.replace("_", " "))
            })
    return sorted(result, key=lambda x: x["sw"])

@app.get("/")
def root():
    return {"message": "SACA API is running"}