import random
from typing import Optional
from openenv.core import Environment
from vc_negotiation_env.models import Action, Observation, DealState

class VcNegotiationEnvironment(Environment):
    def __init__(self):
        self.state: Optional[DealState] = None

    def reset(self) -> Observation:
        self.state = DealState(
            founder_target_valuation=random.uniform(8.0, 20.0),
            founder_min_valuation=random.uniform(4.0, 7.9),
            founder_max_equity=random.uniform(10.0, 25.0),
            competing_offer=random.choice([None, round(random.uniform(6.0, 15.0), 1)]),
            current_round=0,
            max_rounds=6,
            deal_closed=False,
            founder_walked=False,
            offers_made=[]
        )
        msg = "We're looking for a strong partner. What would you like to know about us?"
        if self.state.competing_offer:
            msg += f" Just so you know, we have another offer on the table at ${self.state.competing_offer}M."
        return Observation(
            founder_message=msg,
            round_number=0,
            deal_closed=False,
            founder_walked=False
        )

    def step(self, action: Action) -> tuple[Observation, float, bool]:
        s = self.state
        s.current_round += 1
        reward = 0.0
        done = False
        founder_msg = ""

        if action.action_type == "ask":
            hints = []
            if "valuation" in (action.message or "").lower():
                hints.append(f"We think we're worth at least ${s.founder_min_valuation:.1f}M.")
            if "equity" in (action.message or "").lower():
                hints.append(f"We can't give away more than {s.founder_max_equity:.1f}% equity.")
            if "competing" in (action.message or "").lower() and s.competing_offer:
                hints.append(f"The other offer is at ${s.competing_offer}M.")
            founder_msg = " ".join(hints) if hints else "We're happy to discuss terms."
            reward = 0.05

        elif action.action_type == "offer":
            val = action.valuation or 0.0
            eq = action.equity or 0.0
            s.offers_made.append({"valuation": val, "equity": eq, "round": s.current_round})
            if val >= s.founder_target_valuation and eq <= s.founder_max_equity:
                s.deal_closed = True
                done = True
                reward = 1.0 - (eq / 100.0) - (s.current_round / s.max_rounds * 0.2)
                founder_msg = "This looks great! We accept your offer."
            elif val >= s.founder_min_valuation:
                founder_msg = f"Hmm, we were hoping for more. Can you go to ${s.founder_target_valuation:.1f}M?"
                reward = 0.2
            else:
                founder_msg = "That's too low for us. We need a better valuation."
                reward = -0.1

        elif action.action_type == "accept":
            if s.offers_made:
                last = s.offers_made[-1]
                if last["valuation"] >= s.founder_min_valuation:
                    s.deal_closed = True
                    done = True
                    reward = 0.5
                    founder_msg = "Deal accepted!"
                else:
                    founder_msg = "We can't accept on these terms."
                    reward = -0.2
            else:
                founder_msg = "There's no offer to accept yet."
                reward = -0.1

        elif action.action_type == "walkaway":
            s.founder_walked = True
            done = True
            reward = -1.0
            founder_msg = "Understood. We'll go with the other offer then."

        if s.current_round >= s.max_rounds and not done:
            done = True
            reward = -0.5
            founder_msg = "We've run out of time. No deal."

        return (
            Observation(
                founder_message=founder_msg,
                round_number=s.current_round,
                deal_closed=s.deal_closed,
                founder_walked=s.founder_walked
            ),
            reward,
            done
        )

    def state(self) -> DealState:
        return self.state