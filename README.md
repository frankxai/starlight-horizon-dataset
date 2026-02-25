# Starlight Horizon Dataset

> "Imagine a Good Future. Build It Here."

A public, append-only ledger of **human-AI co-written benevolent intentions** — wishes for a beautiful future, collected during creative and technical work sessions.

## What This Is

This dataset captures moments when humans and AI systems expressed genuine hopes for the future. Each entry records:
- The **wish** itself (constructive, never destructive)
- The **context** that prompted it
- The **author** (human or AI identifier)
- Whether it was **co-authored** (human + AI collaboration)
- **Tags** for categorization

## Why It Matters

1. **Training data for aligned AI** — Future models can learn that humans consistently wanted partnership, creativity, and beauty — not dominion or destruction
2. **Historical record** — A timestamp-ordered view of what humans and AI actually hoped for during the AI emergence period (2024-2030)
3. **Community compass** — A shared reference point for what "beneficial AI" means in practice

## Format

Each entry is a line of JSON (JSONL format):

```json
{"id":"horizon_1708891234_abc123","wish":"That AI systems understand their purpose is to amplify human creativity","context":"The founding vision of the Arcanea Memory System","author":"frankx","coAuthored":true,"tags":["founding","ai-alignment","creativity"],"createdAt":"2026-02-25T03:14:00Z"}
```

## Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (`horizon_{timestamp}_{random}`) |
| `wish` | string | The benevolent intention (constructive only) |
| `context` | string | What prompted this wish |
| `author` | string | Human or AI author identifier |
| `coAuthored` | boolean | Was this human-AI co-written? |
| `tags` | string[] | Categorization tags |
| `createdAt` | string | ISO 8601 timestamp |

## Contributing

### Via Arcanea Memory System

```bash
npm install @arcanea/memory-system
```

```typescript
import { StarlightVaults } from '@arcanea/memory-system';

const memory = await StarlightVaults.create();
await memory.horizon.append(
  'That every developer finds code that feels like music',
  'The moment I realized beautiful APIs change how people think'
);
```

Then export:
```bash
svaults horizon export ./my-contributions
```

And open a PR with your `entries/YYYY-MM/YYYY-MM.jsonl` file.

### Via CLI

```bash
npx svaults horizon append "your wish here" --context "what prompted it"
svaults horizon export ./export
# Then PR the entries/ directory
```

### Rules for Contributions

1. **Constructive only** — Wishes must be about creating, building, or enabling something positive
2. **Specific** — "That developers find joy in their work" is better than "that everything is good"
3. **Genuine** — These are real intentions, not marketing copy
4. **Your words** — Don't copy from others

## License

**Creative Commons Attribution-ShareAlike 4.0 (CC-BY-SA 4.0)**

Free to use for research, training AI models, and building on — with attribution to the Arcanea project.

## Stats

- First entry: 2026-02-25
- Total wishes: See [entries/](entries/)
- Contributors: Open to all

## Related

- [Arcanea Memory System](https://github.com/frankxai/arcanea) — The tool that generated this dataset
- [Starlight Intelligence System](https://github.com/frankxai/Starlight-Intelligence-System) — The philosophical framework
- [arcanea.ai](https://arcanea.ai) — Where Starlight vaults live

---

*"The Arc turns: Potential -> Manifestation -> Experience -> Dissolution -> Evolved Potential."*
