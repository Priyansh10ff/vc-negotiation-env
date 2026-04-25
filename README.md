---
title: VC Negotiation Env
emoji: 💼
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# 💼 VC Negotiation Environment

An RL training environment where an AI agent learns to negotiate startup funding deals like a seasoned VC partner.

## 🎯 Problem

LLMs are great at conversation but terrible at strategic negotiation — they don't know when to push, when to concede, or how to extract hidden information to close a deal. This environment trains agents to do exactly that.

## 🌍 Environment

The agent plays a VC partner negotiating with a simulated startup founder who has **hidden preferences**:
- Secret target valuation
- Minimum acceptable valuation  
- Maximum equity they'll give away
- Possible competing offers

The agent must **investigate**, **strategize**, and **close** — all within 6 rounds.

### Actions
| Action | Description |
|--------|-------------|
| `ask` | Ask founder questions to reveal hidden info |
| `offer` | Make a term sheet offer (valuation + equity) |
| `accept` | Accept the current terms |
| `walkaway` | Walk away from the deal |

### Reward Signals (5 Independent)
| Signal | Weight | Description |
|--------|--------|-------------|
| `deal_closed` | 40% | Did the agent close the deal? |
| `valuation_efficiency` | 20% | How close to founder's minimum? |
| `equity_efficiency` | 20% | How little equity did agent give away? |
| `speed_bonus` | 10% | Faster close = higher reward |
| `info_gathering` | 10% | Did agent ask smart questions? |

## 🚀 API

```bash
# Start a new negotiation
POST /reset

# Take an action
POST /step?session_id=<id>
{"action_type": "ask", "message": "what is your valuation expectation?"}

# Check hidden state
GET /state?session_id=<id>
```

## 📈 Training Results

- **Baseline reward:** 0.026
- **After GRPO training:** 0.13+ (5x improvement)
- **Model:** Qwen2.5-1.5B-Instruct + LoRA
- **Framework:** TRL GRPO + Unsloth

## 🛠️ Stack
- OpenEnv (environment framework)
- FastAPI (server)
- TRL GRPO (training)
- Unsloth (efficiency)
- HuggingFace Spaces (deployment)

## 📚 Resources
- [Training Notebook](#) ← add Kaggle link after training
- [Mini Blog](#) ← add HF blog link