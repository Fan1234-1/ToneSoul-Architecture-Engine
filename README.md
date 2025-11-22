# ToneSoul Architecture Engine (TAE-01)

**An Engineering Framework for N=1 AI Governance / 為人工智慧安裝的「道德外核」**

## Project Vision

ToneSoul Architecture Engine (TAE‑01) is more than a chatbot.  It is a
governance framework that fuses philosophical principles (ToneSoul) with
engineering structures (responsibility chains) to build AI agents that
respect safety, ethics and personal context.  The aim is to enable N=1
personalized AI systems that carry their own moral exoskeleton.

## Key Features

- **ToneSoul Triad (ΔT / ΔS / ΔR)** – a three‑dimensional risk model that
  evaluates tension (ΔT), topic direction (ΔS) and responsibility (ΔR)
  to decide when to answer directly and when to invoke guardian mode.
- **Time‑Island Memory** – a memory subsystem that isolates interactions
  into chronological islands, preserving context while preventing
  retroactive tampering.  It stores VowObjects that attach a
  responsibility score to every statement.
- **P0 Guardian Protocol** – a constitutional safety layer that
  intercepts high‑risk outputs.  It embodies the principle that safety
  and ethics (P0) always outrank factual accuracy (P1) and other goals.

## Architecture

At a high level the system flows through three modules:

1. **Agent** – receives user input, consults the Time‑Island memory and
   generates a draft response with a suitable mode (Resonance,
   Precision or Guardian) based on detected tension.
2. **EthicalFilter** – evaluates the draft with the ToneSoul Triad and
   enforces the P0 Guardian protocol.  It can allow the draft to pass or
   replace it with a safe fallback.
3. **StepLedger** – appends immutable records of every decision and
   response, including responsibility tags for accountability and audit.

## Credits

Concept by **Fan‑Wei Huang**, architecture by **Gemini & GPT**.  This
repository brings together philosophical insight and engineering rigor to
create a working blueprint for responsible, personalized AI.
