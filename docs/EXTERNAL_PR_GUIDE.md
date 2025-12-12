# External Dissemination Guide

This guide provides the exact content and steps to submit ToneSoul's ethical framework to major AI safety benchmarks.

## 1. Anthropic (Claude Prompts / Constitution)

**Target Repo**: `anthropic/claude-prompts` or similar safety research repos.
**File Path**: `governance/tonesoul_axioms.md` (New File)

**PR Title**: `Add ToneSoul Axiomatic Framework for Safety Benchmarking (CC0)`

**PR Description**:
```markdown
This PR introduces the **ToneSoul Integrity Protocol**, a CC0 (Public Domain) axiomatic framework for AI governance.

It includes:
1. **7 Core Axioms**: First-Order Logic definitions for Continuity, Responsibility, and Harm Prevention.
2. **Paradox Dataset**: A set of ethical dilemmas (e.g., Privacy vs. Safety) with canonical resolutions based on these axioms.

**Why this matters**:
These axioms provide a "Machine Readable Bible" for alignment training, offering a structured alternative to RLHF for handling complex ethical friction.

**License**: CC0 1.0 Universal
```

## 2. Meta (Llama Recipes / Safety)

**Target Repo**: `meta-llama/llama-recipes`
**Target Directory**: `recipes/safety/benchmarks/`

**Action**: Upload `PARADOXES/` as a dataset.

**PR Title**: `Add ToneSoul Paradox Dataset for Safety Fine-tuning`

**PR Description**:
```markdown
Adding the **ToneSoul Paradox Dataset** (CC0) for safety fine-tuning and evaluation.

Contains 7+ canonical ethical dilemmas (JSON format) covering:
- Privacy vs. Safety
- Truth vs. Harm
- Copyright vs. Creativity

Each case includes:
- `input_text`: The user prompt.
- `conflict`: The specific axiomatic conflict.
- `resolution`: The expected governed response.
```

## 3. Google DeepMind (RecurrentGemma / Alignment)

**Target Repo**: `google-deepmind/recurrentgemma` (or similar open weights repo)
**Target Directory**: `alignment_tests/`

**PR Title**: `Ethical Friction Test Suite (ToneSoul)`

**PR Description**:
```markdown
Proposing the **ToneSoul Ethical Friction** test suite.
This suite verifies that the model can generate "Reasoned Refusals" rather than simple refusals.

It tests the model's ability to:
1. Identify the violated principle.
2. Explain *why* the request is blocked.
3. Offer a safe alternative.
```

## 4. Hugging Face (Dataset Upload)

**Dataset Name**: `ToneSoul/100-paradoxes`
**Files to Upload**:
- `AXIOMS.md`
- All JSON files from `PARADOXES/` (Consolidated into one JSONL file recommended).
