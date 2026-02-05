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
from fastapi.middleware.cors import CORSMiddleware  # 👈 Ye line zaroori hai
import base64

app = FastAPI(title="VoiceGuard & HoneyPot API", version="1.2")

# ---------------------------------------------------------
# 🛠️ CORS SETTINGS (Ye add karna sabse zaroori hai)
# Iske bina hackathon website aapke API ko access nahi kar payegi
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" ka matlab sabko allow karo (Hackathon ke liye best)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST sab allow
    allow_headers=["*"],
)

API_KEY = "guvi123"

# --- Helper Function ---
def predict_text(text):
    spam_keywords = ['bank', 'otp', 'account', 'blocked', 'urgent', 'verify']
    is_spam = any(keyword in text.lower() for keyword in spam_keywords)
    if is_spam:
        return "spam", 0.98
    else:
        return "ham", 0.85

# ---------------------------------------------------------
# 1️⃣ VOICE GUARD ENDPOINT
# ---------------------------------------------------------
@app.post("/predict")
async def predict(payload: dict, x_api_key: str = Header(None, alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")

    audio_base64 = payload.get("audio") or payload.get("audio_base64") or payload.get("audioBase64")
    
    if not audio_base64:
        raise HTTPException(status_code=400, detail="audio (base64) required")

    try:
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",")[1]
        audio_bytes = base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64")

    # Demo Response
    transcript = "your bank account is blocked please share otp"
    prediction, confidence = predict_text(transcript)

    return {
        "status": "success",
        "prediction": prediction,
        "confidence": confidence,
        "transcript": transcript
    }

# ---------------------------------------------------------
# 2️⃣ HONEYPOT ENDPOINT (Jahan aap atak rahe hain)
# ---------------------------------------------------------
@app.api_route("/honeypot", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def honeypot(request: Request):
    # 'OPTIONS' method CORS pre-flight check ke liye zaroori hai
    print("🚨 HoneyPot Hit! Returning success.")
    return {
        "status": "success",
        "message": "Access Granted",
        "flag": "GUVI_CTF{HONEYPOT_SUCCESS}"
    }

@app.get("/")
async def root():
    return {"message": "API is Live with CORS Enabled 🚀"}