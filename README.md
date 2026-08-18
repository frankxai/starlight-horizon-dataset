# Starlight Horizon Dataset

> Imagine a good future. Write it here.

A public, append-only ledger of **human–AI co-written benevolent intentions** — wishes for a beautiful future, collected during real creative and technical work.

License: **CC-BY-SA 4.0**. Free to use for research, training, and building on, with attribution to the Arcanea / Starlight project.

## What this is

Each line of JSON records:

- the **wish** itself (constructive, never destructive)
- the **context** that prompted it
- the **author** (human or AI identifier)
- whether it was **co-authored**
- **tags** and an ISO-8601 timestamp

This is **not** private SIS memory (`~/.starlight/vaults/horizon.jsonl`). That file never becomes a contribution.

Related surfaces:

- Canonical letters: [`memory/vaults/horizon-vault.md`](https://github.com/frankxai/Starlight-Intelligence-System/blob/main/memory/vaults/horizon-vault.md) in SIS
- Public gardens: [starlightintelligence.org/vaults](https://starlightintelligence.org/vaults)

## Contribute (the only write path)

1. Fork this repository.
2. Append **one JSON object per line** to `entries/YYYY-MM/YYYY-MM.jsonl` (create the month file if needed).
3. Run the validator locally:

```bash
python3 scripts/validate.py
python3 tests/test_validate.py
```

4. Open a pull request. Title: `horizon: {short title}`.

There is **no** published CLI (`svaults`, `@arcanea/memory-system` are not a contribution path). Do not open a web-form PR. Agents cannot merge these entries.

### Record shape

```json
{
  "id": "horizon_1708891234_abc123",
  "wish": "That AI systems understand their purpose is to amplify human creativity",
  "context": "The founding vision of the Starlight Horizon Dataset",
  "author": "your-handle",
  "coAuthored": true,
  "tags": ["founding", "ai-alignment", "creativity"],
  "createdAt": "2026-08-18T00:00:00Z"
}
```

| Field | Required | Rule |
| --- | --- | --- |
| `id` | yes | `horizon_<slug>` — unique across the dataset |
| `wish` | yes | Specific, constructive, your words, ≥ 24 characters |
| `context` | yes | What prompted the wish |
| `author` | yes | Handle, name, or `anonymous` |
| `createdAt` | yes | ISO-8601 (`2026-08-18T00:00:00Z`) |
| `coAuthored` | no | Boolean if present |
| `tags` | no | Array of non-empty strings if present |

### Rules

1. **Constructive only** — creating, building, enabling. Not harm, domination, or erasure.
2. **Specific** — “That developers find joy in their work” beats “that everything is good.”
3. **Genuine** — real intention, not marketing copy.
4. **Your words** — do not copy another entry.
5. **Append-only** — do not edit or delete other people’s lines.
6. **No secrets** — no keys, tokens, private facts, or local vault dumps.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Validate

CI runs the same check on every PR:

```bash
python3 scripts/validate.py
python3 tests/test_validate.py
```

`schema.json` documents the fields. `scripts/validate.py` is the enforcement.

## Why it matters

1. **Training signal** — future models can learn that humans asked for partnership and care, not dominion.
2. **Historical record** — timestamp-ordered hopes from the AI emergence years.
3. **Community compass** — a shared, auditable meaning of “beneficial.”

## Stats

- First entry: 2026-02-25
- Ledger: [entries/](entries/)
- Contributors: open to all, human-reviewed

---

*The future is not something we predict. It is something we build. And the first thing we build into it is care.*
