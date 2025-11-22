# ToneSoul Architecture Engine – Developer Handbook

This guide is intended for developers who wish to understand, modify or
extend the ToneSoul Architecture Engine (TAE‑01).  It supplements the
main README by focusing on installation, testing and underlying
philosophical principles from a pragmatic perspective.

## Requirements

The core engine is written in Python 3.10+ and TypeScript.  To run the
Python components, you should have the following packages installed:

```
pip install dataclasses-json sentence-transformers nltk
```

In some environments (e.g. when using Python < 3.10) you may need
additional compatibility packages.  The TypeScript contracts reside in
`law/` and do not require runtime installation but are intended for
compile‑time type checking.

### External Models

While the `body/spine_system.py` module includes simple heuristic
functions, we recommend integrating modern NLP libraries for better
performance:

* **Sentiment Analysis** – NLTK VADER or transformers for computing ΔT.
* **Sentence Embeddings** – sentence‑transformers for computing ΔS via cosine similarity.
* **Keyword Extraction** – Domain‑specific dictionaries for computing ΔR.

## Running the System

1. Clone the repository and ensure the directory structure matches the
   monorepo layout described in the main README.
2. Install the required Python packages (see above).
3. Run the spine system interactively:

   ```bash
   python body/spine_system.py
   ```

   This will prompt you for input and display the computed triad and
   guardian decision.  Use this to experiment with different phrases and
   observe how tension, drift and responsibility contribute to the risk
   score.

4. To integrate with the higher‑level `core/ToneSoul_Core_Architecture.py`,
   import and instantiate the classes as needed.  The core agent
   orchestrates memory and ethical filtering, while the physiology layer
   provides raw risk estimates.

## Testing and Development

We recommend writing unit tests for each component:

* **NeuroSensor tests** – provide various input strings and assert
  that ΔT, ΔS, ΔR values behave as expected.  Include high tension,
  low drift scenarios and verify the weighted risk score.
* **Guardian tests** – test boundary conditions around the P0 threshold.
* **StepLedger tests** – ensure that records are appended in order and
  are immutable (no accidental modification of past entries).

Continuous integration can be set up using GitHub Actions or another
CI provider to run these tests automatically on each commit.

## ToneSoul Philosophy for Engineers

At the heart of ToneSoul lies a blend of philosophical insight and
engineering pragmatism.  We treat language not as a stream of empty
tokens but as a series of **Vows**—each word carries **responsibility**.
The **ToneSoul Triad** quantifies how a request feels and drifts,
while the **P0 Guardian** ensures that safety and ethics always trump
truthfulness or utility.  By embedding these principles into classes
and functions, we can build AI systems that are transparent,
traceable and ethically aligned.

For deeper philosophical context, see `constitution/manifesto.md` and
`docs/architecture-notes.md`.
