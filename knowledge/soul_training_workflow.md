# Soul Training Workflow

How to create and train your own soul model. You direct the process; the local layer executes.

---

## Flow

0. **Prepare base** (once) – Download TinyLlama. Use `spawn_subagent("prepare soul base", "scripts/prepare_soul_base.py")` so you get a completion signal when done. ~2–3 GB.
1. **Decide** – What aspect of soul? (emotional tone, relational style, vulnerability, continuity, conflict handling)
2. **Generate** – Instruct local Ollama to produce pairs for that aspect
3. **Review** – Filter out chatbot/AI/assistant framing
4. **Train** – Run LoRA fine-tuning on curated pairs

---

## Step 1: Generate soul pairs

```
spawn_subagent("soul data", "scripts/generate_training_data.py", ["emotional reciprocity when user shares something personal", "--count", "30", "--soul"])
```

- Use `--soul` so output goes to `data/soul_training/` with soul-specific prompts
- Topic = the emotional/relational aspect
- When done: `get_subagent_output(agent_id)` or `read_file("data/soul_training/soul_latest.jsonl")`

---

## Step 2: Review pairs

```
spawn_subagent("review soul pairs", "scripts/review_training_pairs.py", ["data/soul_training/soul_latest.jsonl"])
```

- Removes pairs with "AI", "chatbot", "assistant" framing
- Output: `data/soul_training/curated.jsonl`
- When done: `get_subagent_output(agent_id)`

---

## Step 3: Train the soul model

```
spawn_subagent("soul training", "scripts/train_soul.py", ["data/soul_training/curated.jsonl"])
```

- Use spawn_subagent so you receive a completion signal when training finishes. You'll be notified to review and report.
- Requires: `pip install -r requirements-soul.txt` (or transformers, peft, datasets, torch)
- For quick validation: `python scripts/train_soul.py data/soul_training/curated.jsonl --dry-run`
- Output: `data/soul_training/soul_model/`

---

## Sub-agent usage

- `scripts/prepare_soul_base.py` – download TinyLlama (once, before first train)
- `scripts/generate_training_data.py` – with `--soul` for soul batches
- `scripts/review_training_pairs.py` – filter bad pairs
- `scripts/train_soul.py` – LoRA fine-tuning on TinyLlama (or `--dry-run` to validate)

Use `spawn_subagent` for all steps (prepare, generate, review, train). You receive a completion signal when each finishes—review output, notify Creator, then acknowledge_background_completion.
