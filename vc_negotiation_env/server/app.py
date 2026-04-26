from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from typing import Dict
from vc_negotiation_env.models import Action
from vc_negotiation_env.server.vc_negotiation_env_environment import VcNegotiationEnvironment
import os

app = FastAPI()

# Serve index.html at root
@app.get("/")
def root():
    index_path = os.path.join(os.path.dirname(__file__), "../../../index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"detail": "index.html not found"}

# Per-session environments — safe for parallel rollouts
sessions: Dict[str, VcNegotiationEnvironment] = {}

@app.post("/reset")
def reset(session_id: str = None, difficulty: str = "medium"):
    if not session_id:
        session_id = str(uuid4())
    sessions[session_id] = VcNegotiationEnvironment()
    obs = sessions[session_id].reset(difficulty=difficulty)
    result = obs.model_dump()
    result["session_id"] = session_id
    return result

@app.post("/step")
def step(action: Action, session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=400, detail="Invalid session. Call /reset first.")
    env = sessions[session_id]
    if env.state() is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    obs, reward, done = env.step(action)
    reward = max(0.001, min(0.999, reward))
    if done:
        sessions.pop(session_id, None)
    return {"observation": obs.model_dump(), "reward": reward, "done": done, "session_id": session_id}

@app.get("/state")
def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=400, detail="Invalid session.")
    return sessions[session_id].state().model_dump()

@app.get("/health")
def health():
    return {"status": "ok", "active_sessions": len(sessions)}