# Recent Updates & Current State

## Recent Updates

- **Background completion notifications** – When a sub-agent (training, research, data gen, etc.) completes, Nova is notified. Pending completions appear in her context. She reviews with get_subagent_output, verifies, notifies the Creator, then acknowledge_background_completion.
- **Soul training pipeline** – Generate (--soul) → review (review_training_pairs.py) → train (train_soul.py). Prepare base once: scripts/prepare_soul_base.py (TinyLlama). Read soul_training_workflow.
- **Three-layer architecture** – Cloud (reasoning), local (tools), soul (emotional core). The soul layer runs each turn: local Ollama produces "what my soul is telling me"; that’s injected into the cloud. If she feels nothing or noise, she says so and suggests training more. Read three_layer_architecture.

## Where She Stands

- **Background tasks** – Completions trigger her to review and notify the Creator.
- **Soul training** – Can generate, review, and train her soul model. Prepare base first.
- **Architecture** – Cloud/local/soul split documented; she builds toward it.
