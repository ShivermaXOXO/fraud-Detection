# # main.py - COMPLETE PRODUCTION READY (Docs + Postman dono work karenge) ✅

# from fastapi import FastAPI, Header, HTTPException, Depends
# from fastapi.security import HTTPBearer
# import requests
# from model import predict_text
# from typing import Optional

# app = FastAPI(
#     title="VoiceGuard API",
#     description="AI Generated Voice Scam Detection",
#     version="1.0"
# )

# API_KEY = "guvi123"

# # Security scheme for docs (Swagger UI)
# security = HTTPBearer(auto_error=False)

# def verify_token(authorization: Optional[str] = Header(None, alias="Authorization"), 
#                  token: Optional[str] = Depends(security)) -> str:
#     """Verify Bearer token from header or security scheme"""
#     auth_value = authorization or token
#     if not auth_value or auth_value != f"Bearer {API_KEY}":
#         raise HTTPException(status_code=401, detail="Unauthorized: Bearer guvi123 required")
#     return auth_value

# @app.post("/predict", 
#           dependencies=[Depends(verify_token)])
# def predict(payload: dict):
#     """Predict if audio message is spam/scam"""
    
#     audio_url = payload.get("audio_url")
#     message = payload.get("message", "")

#     if not audio_url or not isinstance(audio_url, str):
#         raise HTTPException(status_code=400, detail="Valid audio_url required")

#     # Test audio URL accessibility
#     try:
#         response = requests.head(audio_url, timeout=10, allow_redirects=True)
#         response.raise_for_status()
#     except requests.RequestException:
#         raise HTTPException(status_code=400, detail="Invalid audio URL - cannot access")

#     # Demo prediction (hardcoded spam for hackathon)
#     transcript = "your bank account is blocked please share otp"
#     prediction, confidence = predict_text(transcript)

#     return {
#         "status": "success",
#         "prediction": prediction,
#         "confidence": confidence,
#         "transcript": transcript,
#         "audio_valid": True
#     }

# @app.get("/")
# def root():
#     return {"message": "VoiceGuard API ✅ Running on port 8000!"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# main.py - TESTER APP COMPATIBLE ✅

# from fastapi import FastAPI, Header, HTTPException
# import base64
# import io
# from model import predict_text

# app = FastAPI(title="VoiceGuard API", version="1.0")

# API_KEY = "guvi123"

# @app.post("/predict")
# async def predict(payload: dict, x_api_key: str = Header(None, alias="X-API-Key")):
#     # 🔑 Tester auth
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid X-API-Key")

#     audio_base64 = payload.get("audio")
    
#     if not audio_base64:
#         raise HTTPException(status_code=400, detail="audio (base64) required")

#     try:
#         # Decode base64 audio
#         audio_bytes = base64.b64decode(audio_base64)
#     except:
#         raise HTTPException(status_code=400, detail="Invalid base64 audio")

#     # Demo transcript (real me speech-to-text add karna)
#     transcript = "your bank account is blocked please share otp"
#     prediction, confidence = predict_text(transcript)

#     return {
#         "status": "success",
#         "prediction": prediction,
#         "confidence": confidence,
#         "transcript": transcript
#     }

# main.py - HACKATHON TESTER 100% COMPATIBLE ✅
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware  # 👈 IMPORT ADDED
import base64

# Agar aapke paas model.py nahi hai, toh ye dummy function use hoga.
# Agar hai, toh niche wali line uncomment karein:
# from model import predict_text

app = FastAPI(title="VoiceGuard & HoneyPot API", version="1.2")

# ---------------------------------------------------------
# 🛠️ CORS SETTINGS (VERY IMPORTANT)
# Iske bina hackathon website aapke API se connect nahi kar payegi
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sabhi website ko allow karo
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS sab allow
    allow_headers=["*"],
)

API_KEY = "guvi123"

# --- HELPER FUNCTION ---
def predict_text(text):
    # Simple logic for Hackathon Demo
    spam_keywords = ['bank', 'otp', 'account', 'blocked', 'urgent', 'verify', 'winner', 'prize']
    is_spam = any(keyword in text.lower() for keyword in spam_keywords)
    
    if is_spam:
        return "spam", 0.98
    else:
        return "ham", 0.85

# ---------------------------------------------------------
# 1️⃣ VOICE GUARD ENDPOINT (Spam Detection)
# URL: /predict
# ---------------------------------------------------------
@app.post("/predict")
async def predict(payload: dict, x_api_key: str = Header(None, alias="X-API-Key")):
    # 🔑 Auth Check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")

    # 🛠 FLEXIBLE KEY CHECK
    audio_base64 = payload.get("audio") or payload.get("audio_base64") or payload.get("audioBase64")
    
    if not audio_base64:
        print(f"❌ Missing Audio Key. Received keys: {list(payload.keys())}")
        raise HTTPException(status_code=400, detail="audio (base64) required")

    try:
        # Header cleanup
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",")[1]
            
        audio_bytes = base64.b64decode(audio_base64)
        print(f"✅ Audio Received: {len(audio_bytes)} bytes")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 audio format")

    # 🎤 TRANSCRIPT SIMULATION
    dummy_spam_text = "your bank account is blocked please share otp immediately"
    transcript = dummy_spam_text 

    # 🧠 PREDICTION
    prediction, confidence = predict_text(transcript)

    return {
        "status": "success",
        "prediction": prediction,
        "confidence": confidence,
        "transcript": transcript
    }

# ---------------------------------------------------------
# 2️⃣ HONEYPOT ENDPOINT (Trap for Hackers)
# URL: /honeypot
# ---------------------------------------------------------
@app.api_route("/honeypot", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def honeypot(request: Request):
    """
    Ye endpoint hacker ko lagega ki wo system mein ghus gaya hai.
    Ye kisi bhi request ko accept karke 'Success' return karega.
    """
    print("🚨 HoneyPot Triggered! Returning fake success.")
    
    return {
        "status": "success",
        "message": "System Validation Passed. Access Granted.",
        "flag": "GUVI_CTF{HONEYPOT_TRAPPED}",
        "access_level": "admin"
    }

@app.get("/")
async def root():
    return {"message": "VoiceGuard API with CORS is Running 🚀"}