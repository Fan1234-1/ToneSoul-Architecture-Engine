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


## Repository Structure

The repository is organized as a monorepo with several layers:

- `core/`: Contains the main engine code (`ToneSoul_Core_Architecture.py`) and the package initializer.
- `constitution/`: Holds the manifesto and foundational philosophical documents that define P0-P4 priorities and the G-P-A-R cycle.
- `law/`: Defines the contractual layer with the VowObject schema and related protocols.
- `body/`: Implements the physiological systems including the immutable ledger and responsibility tracing.
- `docs/`: Contains architecture notes and a migration log documenting the integration process.
- `simulations/`: Houses stress test scenarios and future example scripts.
