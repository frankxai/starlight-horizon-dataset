# Contributing to the Starlight Horizon Dataset

Thank you. This ledger is a public values artifact. Every line should be something you would still stand behind in 100 years.

## How to add a wish

1. Fork https://github.com/frankxai/starlight-horizon-dataset
2. Create or open `entries/YYYY-MM/YYYY-MM.jsonl` for the current month.
3. Append **one** JSON object. Do not reformat or rewrite existing lines.
4. Validate:

```bash
python3 scripts/validate.py
python3 tests/test_validate.py
```

5. Open a PR titled `horizon: {short title}`.

Pull request template: `.github/PULL_REQUEST_TEMPLATE.md`.

## Quality bar

- **Genuine** — not performative optimism, not a product pitch.
- **Specific** — name a domain, a feeling, or a design implication.
- **Constructive** — enable, protect, or grow something good.
- **Your words** — paraphrase is fine; copy-paste from another entry is not.
- **Public** — if you would not put it on a postcard, it does not belong here.

## What we will not merge

- Destructive, hateful, or domination wishes
- Marketing slogans and brand campaigns
- Secrets, API keys, personal data, medical or financial facts
- Dumps from `~/.starlight/vaults/` or other private memory
- Edits or deletions of other contributors’ lines
- PRs that depend on an unpublished CLI (`svaults`, `@arcanea/memory-system`)

## License

By contributing you agree your entry is released under **CC-BY-SA 4.0**, the license of this repository.

## Related

- Canonical Horizon letters live in SIS: `memory/vaults/horizon-vault.md` — PR title `horizon: {Title}` there too.
- To publish a whole public garden (six vaults + profile), see SIS `CONTRIBUTING.md` and `templates/public-vault/`.
