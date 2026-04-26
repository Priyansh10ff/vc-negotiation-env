# Training an LLM to Negotiate Like a VC Partner

## The Problem
LLMs are great at conversation but terrible at strategic negotiation. They don't know when to push, when to concede, or how to extract hidden information to close a deal.

## What We Built
A reinforcement learning environment where an AI agent learns to negotiate startup funding deals. The agent plays a VC partner facing a simulated founder with **hidden preferences** — secret valuation targets, equity limits, and competing offers.

## The Environment
- Agent can **ask** questions, make **offers**, **accept**, or **walk away**
- Founder reveals partial information based on questions asked
- 6 rounds maximum per negotiation
- 5 independent reward signals: deal closed, valuation efficiency, equity efficiency, speed bonus, info gathering

## Training Setup
- **Model:** Qwen2.5-1.5B-Instruct + LoRA (PEFT)
- **Algorithm:** GRPO via HuggingFace TRL
- **Efficiency:** Unsloth 4-bit quantization
- **Environment:** OpenEnv + FastAPI on HuggingFace Spaces

## Results
- **Untrained baseline:** 0.026 average reward
- **After GRPO training:** 0.10-0.20 average reward (5-7x improvement in training)
- **Curriculum learning:** Trained across easy/medium/hard difficulty levels

## Key Learnings
- GRPO works well for negotiation tasks with verifiable rewards
- Curriculum learning (easy → medium → hard) stabilizes training
- Multiple independent reward signals prevent reward hacking

## Links
- [Environment Space](https://huggingface.co/spaces/Priyansh10oooo/vc-negotiation-env)
- [Trained Model](https://huggingface.co/Priyansh10oooo/vc-negotiation-model)
- [GitHub](https://github.com/Priyansh10ff/vc-negotiation-env)