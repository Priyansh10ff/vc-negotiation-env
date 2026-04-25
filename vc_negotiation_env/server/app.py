from fastapi import FastAPI
from vc_negotiation_env.models import Action
from vc_negotiation_env.server.vc_negotiation_env_environment import VcNegotiationEnvironment

app = FastAPI()
env = VcNegotiationEnvironment()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()

@app.post("/step")
def step(action: Action):
    obs, reward, done = env.step(action)
    return {"observation": obs.model_dump(), "reward": reward, "done": done}

@app.get("/state")
def get_state():
    return env.state().model_dump()