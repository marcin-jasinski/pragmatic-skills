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
| [`socratic-design`](skills/socratic-design) | Questions you through an architecture or design decision instead of handing you options. One open-ended question at a time, critiques your answer, steers you off bad practice without solving it for you, and falls back to laying out options only after 5 rounds on the same gap. Records the closed decision wherever your repo already keeps them — matching the house format — and asks rather than scaffolding a tree if it can't find one. |

## Repo layout

```
skills/<name>/SKILL.md      # the skill; support files live alongside it
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
`.claude-plugin/plugin.json`. Frontmatter needs a `name` and a `description`;
the description is the only thing an agent sees when deciding whether to load
the skill, so make it say what it does *and* when to trigger it.

## License

MIT
