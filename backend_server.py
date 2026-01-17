from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
from modules.chatbot_backend import ChatbotBackend
from modules.evaluations import EvaluationAnalyzer
from utils.auth import AuthManager
from utils.monitoring import MonitoringManager

app = FastAPI(title="Safran RH API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = ChatbotBackend()
analyzer = EvaluationAnalyzer()
auth_manager = AuthManager()
monitoring = MonitoringManager()

logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    question: str
    profile: str = "CDI"
    language: str = "fr"

class ChatResponse(BaseModel):
    response: str
    confidence: float
    intent: str

class LoginRequest(BaseModel):
    username: str
    password: str

class EvaluationRequest(BaseModel):
    file_path: str

@app.post("/ask", response_model=ChatResponse)
async def ask_chatbot(request: ChatRequest):
    result = chatbot.ask(request.question, request.profile, request.language)
    monitoring.log_chatbot_interaction(request.question, result["response"], result["confidence"], "user")
    return ChatResponse(
        response=result["response"],
        confidence=result["confidence"],
        intent=result["intent"]
    )

@app.post("/login")
async def login(request: LoginRequest):
    result = auth_manager.authenticate(request.username, request.password)
    if not result:
        monitoring.log_security_event("failed_login", f"User={request.username}")
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    
    monitoring.log_user_login(request.username)
    return result

@app.post("/evaluate")
async def analyze_evaluations(request: EvaluationRequest):
    try:
        analyzer.load_evaluations(request.file_path)
        report = analyzer.generate_report()
        monitoring.log_evaluation_processing(request.file_path, report.get("total_evaluations", 0))
        return report
    except Exception as e:
        logger.error(f"Erreur analyse évaluations: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profiles")
async def get_profiles():
    return {"profiles": chatbot.get_available_profiles()}

@app.get("/languages")
async def get_languages():
    return {"languages": chatbot.get_available_languages()}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Safran RH API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
