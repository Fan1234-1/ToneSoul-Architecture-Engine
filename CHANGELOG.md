# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-23

### Added
- **Grand Unification**: Consolidated 12 fragmented repositories into a single Monorepo (`ToneSoul-Architecture-Engine`).
- **Guardian Protocol v1.0**: Implemented the core governance logic (`P0` Responsibility, `P1` Tension).
- **Rollback Mechanism (The Regret Reflex)**: Added ability to "undo" high-risk interactions by appending a `ROLLBACK` event to the ledger.
- **Rollback Limiter (Circuit Breaker)**: Added a safety mechanism to halt the system after 3 consecutive rollbacks.
- **NeuroModulator**: Implemented the "Subconscious" layer to modulate LLM parameters based on emotional state ($\Delta T, \Delta S, \Delta R$).
- **Canonical Protocol**: Defined JSON Schemas for `Triad`, `Vow`, and `StepRecord` in `modules/protocol/schemas/`.
- **Quickstart Guide**: Added `QUICKSTART.md` for rapid onboarding.

### Changed
- **Constitution**: Migrated to `law/constitution.json` as the single source of truth for ethics and risk keywords.
- **StepLedger**: Refactored to support `vow_id` linking and immutable hash chaining.
- **SpineEngine**: Updated to orchestrate the full Sense-Judge-Modulate-Record-Rollback loop.

### Fixed
- Fixed multiple syntax errors in `spine_system.py` related to docstring parsing.
- Fixed `AttributeError` in `StepLedger` methods.

## [0.9.0] - 2025-11-06
- Initial consolidation of `ai-soul-spine-system` and `tonesoul-codex`.
- Basic implementation of `ToneSoulTriad`.
