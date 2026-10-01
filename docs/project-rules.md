# Skill authoring and documentation conventions

- Essential project-wide rules live in `AGENTS.md` and are imported by `CLAUDE.md`. This file contains the detailed guidance to read for skill authoring and README work.
- In the README, order feature skills by development lifecycle: general build work, specialized build work, review, then review remediation. Add new feature skills at their matching workflow stage; document update management after installation, outside that lifecycle.
- The canonical instruction layout is `docs/agent-instruction-layout.md`. Update it once, then run `python3 scripts/sync-agent-instructions.py --write` to refresh the packaged Knowledge Transfer and Quick Review references. When changing this layout or its packaged references, `python3 scripts/sync-agent-instructions.py --check` must pass before readiness.
