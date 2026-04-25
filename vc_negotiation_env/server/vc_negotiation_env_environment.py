import random
from typing import Optional
from openenv.core import Environment
from vc_negotiation_env.models import Action, Observation, DealState

class VcNegotiationEnvironment(Environment):
    def __init__(self):
        self._state: Optional[DealState] = None

    def reset(self) -> Observation:
        self._state = DealState(
            founder_target_valuation=round(random.uniform(8.0, 20.0), 1),
            founder_min_valuation=round(random.uniform(4.0, 7.9), 1),
            founder_max_equity=round(random.uniform(10.0, 25.0), 1),
            competing_offer=random.choice([None, round(random.uniform(6.0, 15.0), 1)]),
            current_round=0,
            max_rounds=6,
            deal_closed=False,
            founder_walked=False,
            offers_made=[]
        )
        msg = "We're looking for a strong partner. What would you like to know about us?"
        if self._state.competing_offer:
            msg += f" Just so you know, we have another offer at ${self._state.competing_offer}M."
        return Observation(
            founder_message=msg,
            round_number=0,
            deal_closed=False,
            founder_walked=False,
            rewards={}
        )

    def step(self, action: Action) -> tuple:
        s = self._state
        s.current_round += 1
        done = False
        founder_msg = ""

        # Independent reward signals
        reward_deal_closed = 0.0
        reward_valuation_efficiency = 0.0
        reward_equity_efficiency = 0.0
        reward_speed_bonus = 0.0
        reward_info_gathering = 0.0

        if action.action_type == "ask":
            hints = []
            if "valuation" in (action.message or "").lower():
                hints.append(f"We think we're worth at least ${s.founder_min_valuation:.1f}M.")
                reward_info_gathering += 0.05
            if "equity" in (action.message or "").lower():
                hints.append(f"We can't give away more than {s.founder_max_equity:.1f}%.")
                reward_info_gathering += 0.05
            if "competing" in (action.message or "").lower() and s.competing_offer:
                hints.append(f"The other offer is at ${s.competing_offer}M.")
                reward_info_gathering += 0.05
            founder_msg = " ".join(hints) if hints else "Happy to discuss terms."

        elif action.action_type == "offer":
            val = action.valuation or 0.0
            eq = action.equity or 0.0

            # Anti-hack: clamp values to realistic ranges
            val = max(0.1, min(val, 100.0))
            eq = max(0.1, min(eq, 49.9))

            s.offers_made.append({"valuation": val, "equity": eq, "round": s.current_round})

            if val >= s.founder_target_valuation and eq <= s.founder_max_equity:
                s.deal_closed = True
                done = True
                reward_deal_closed = 0.999
                reward_valuation_efficiency = round(min(0.999, 1.0 - ((val - s.founder_target_valuation) / s.founder_target_valuation)), 3)
                reward_equity_efficiency = round(min(0.999, 1.0 - (eq / s.founder_max_equity)), 3)
                reward_speed_bonus = round(min(0.999, 1.0 - (s.current_round / s.max_rounds)), 3)
                founder_msg = "This looks great! We accept your offer."
            elif val >= s.founder_min_valuation:
                founder_msg = f"We were hoping for more. Can you reach ${s.founder_target_valuation:.1f}M?"
                reward_valuation_efficiency = 0.1
            else:
                founder_msg = "That's too low. We need a better valuation."
                reward_valuation_efficiency = 0.001

        elif action.action_type == "accept":
            if s.offers_made:
                last = s.offers_made[-1]
                if last["valuation"] >= s.founder_min_valuation:
                    s.deal_closed = True
                    done = True
                    reward_deal_closed = 0.5
                    founder_msg = "Deal accepted!"
                else:
                    founder_msg = "We can't accept on these terms."
                    reward_deal_closed = 0.001
            else:
                founder_msg = "There's no offer to accept yet."

        elif action.action_type == "walkaway":
            s.founder_walked = True
            done = True
            reward_deal_closed = 0.001
            founder_msg = "We'll go with the other offer then."

        # Timeout penalty
        if s.current_round >= s.max_rounds and not done:
            done = True
            reward_deal_closed = 0.001
            founder_msg = "We've run out of time. No deal."

        # Combined reward
        total_reward = round(
            reward_deal_closed * 0.4 +
            reward_valuation_efficiency * 0.2 +
            reward_equity_efficiency * 0.2 +
            reward_speed_bonus * 0.1 +
            reward_info_gathering * 0.1,
            4
        )

        rewards = {
            "deal_closed": reward_deal_closed,
            "valuation_efficiency": reward_valuation_efficiency,
            "equity_efficiency": reward_equity_efficiency,
            "speed_bonus": reward_speed_bonus,
            "info_gathering": reward_info_gathering,
            "total": total_reward
        }

        return (
            Observation(
                founder_message=founder_msg,
                round_number=s.current_round,
                deal_closed=s.deal_closed,
                founder_walked=s.founder_walked,
                rewards=rewards
            ),
            total_reward,
            done
        )

    def state(self) -> DealState:
        return self._state