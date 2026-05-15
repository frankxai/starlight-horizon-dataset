# starlight-horizon-dataset — AGENTS.md

Dataset and training-data workspace for Starlight horizon work.

## Harness

- Manifest: `.agent-harness.json`
- Risk: private
- Deploy policy: none
- Health: `git status`
- Agent files: `AGENTS.md`, `CLAUDE.md`
- Global hooks: disabled.

## Operating Rules

1. Treat raw data, labels, and exports as private unless explicitly marked public.
2. Do not commit credentials, private transcripts, or generated secrets.
3. Preserve dataset provenance and avoid destructive cleanup without an audit.
4. Verify with `git status` before handoff.

