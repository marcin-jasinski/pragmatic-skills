# pragmatic-skills

Agent skills that keep the engineer in the loop.

Most agent tooling optimises for handing you an answer. These optimise for the
opposite: making you produce the answer, and leaving a written record of why.

## Install

**As a Claude Code plugin** — managed, auto-updating:

```
/plugin marketplace add marcin-jasinski/pragmatic-skills
/plugin install pragmatic-skills
```

**With `npx skills`** — editable, and works across Claude Code, Codex, Cursor,
Copilot, Gemini, OpenCode and ~75 other agents:

```
npx skills@latest add marcin-jasinski/pragmatic-skills
```

The installer detects which agents you have and asks which skills to take.
Update later with `npx skills update`.

## The skills

| Skill | What it does |
|---|---|
| [`design-kickoff`](skills/design-kickoff) | Starts a new system from a rough brief without handing you an architecture. Interviews you on the problem, users, constraints and scale; makes you rank quality attributes (and name one you'll be bad at) and turn adjectives into measurable scenarios; has you model the domain and sketch the first architecture *before* it shows any, then critiques your sketch against the drivers. Ends with a design brief and an ordered backlog of open decisions, ready to take one at a time with `socratic-design`. |
| [`socratic-design`](skills/socratic-design) | Questions you through an architecture or design decision instead of handing you options. One open-ended question at a time, critiques your answer, steers you off bad practice without solving it for you, and falls back to laying out options only after 5 rounds on the same gap. Records the closed decision wherever your repo already keeps them — matching the house format — and asks rather than scaffolding a tree if it can't find one. |
| [`premortem`](skills/premortem) | "It's a year from now and this failed — why?" You write the failure stories first; when you stall it changes the angle rather than feeding you risks, then pushes each story into a concrete trigger → chain → consequence. Only then does it add the failures you missed, labelled as agent-raised (via `red-team-architect` when available). You rate, you pick the top three, you propose prevent / detect / contain / accept — every non-prevention gets a real tripwire. The record ends with your **blind spots**: the agent-raised risks you rated as serious. |
| [`defend-architecture`](skills/defend-architecture) | Reads the architecture you actually shipped, then interviews you on why. One question at a time, no recommended answer supplied, one pushback per topic (plus one re-ask if dodged), and it checks your answers against the files. Rejects "it's best practice" and "for scalability"; accepts "I don't know" without snark, and "the agent wrote it" as an honest answer it marks Unowned. Ends with a verdict per decision — Solid, Unproven, Gap, Contradicted, or Unowned — plus what to record as an ADR, what to delete, and what to take ownership of. |

## The agents

| Agent | What it does |
|---|---|
| [`red-team-architect`](agents/red-team-architect.md) | Adversarial reviewer with a fresh context. Reads a design brief, ADR, plan or codebase cold — deliberately without your reasoning — and returns ranked, concrete attacks: failure scenarios, unjustified components, unstated assumptions, and places where the docs and the code disagree, each with file evidence. It never proposes fixes; each attack ends with an open question for you to answer, one at a time. Read-only. |

Agents ship with the Claude Code plugin. `npx skills` installs skills only — to
use the agent elsewhere, copy `agents/red-team-architect.md` into your agent's
subagent directory (for Claude Code without the plugin: `.claude/agents/`). The
skills that use it fall back to doing the work themselves when it's missing.

## Repo layout

```
skills/<name>/SKILL.md      # the skill; support files live alongside it
agents/<name>.md            # subagents (Claude Code plugin only)
.claude-plugin/             # plugin.json + marketplace.json for the Claude Code path
```

`SKILL.md` is the portable format — Claude Code and Codex read it natively, and
`npx skills` translates it for the agents that use a different shape.

## Working on these skills

This repo is the source of truth. Edit here, then reinstall to pick the change
up — editing the installed copy under `~/.claude/skills/` instead just makes the
two drift.

## Adding a skill

Drop a directory under `skills/`, then add its path to the `skills` array in
`.claude-plugin/plugin.json`. Agents go in `agents/` as a single markdown file
and are picked up from there without registration. Frontmatter needs a `name` and a `description`;
the description is the only thing an agent sees when deciding whether to load
the skill, so make it say what it does *and* when to trigger it.

## License

MIT
