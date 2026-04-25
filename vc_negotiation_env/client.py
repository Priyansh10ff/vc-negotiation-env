import requests
from vc_negotiation_env.models import Action, Observation

class VcNegotiationEnv:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url

    def reset(self) -> Observation:
        r = requests.post(f"{self.base_url}/reset")
        return Observation(**r.json())

    def step(self, action: Action) -> tuple:
        r = requests.post(f"{self.base_url}/step", json=action.model_dump())
        data = r.json()
        return Observation(**data["observation"]), data["reward"], data["done"]