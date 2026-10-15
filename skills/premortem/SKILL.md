---
name: premortem
description: Runs a premortem on a design, plan, migration, or architectural decision before it ships — "it's a year from now and this failed; why?" The user writes the failure stories first; the agent pushes each one until it's a concrete causal chain, then adds the failures the user missed, labelled as its own. Ends with ranked risks, mitigations and tripwires the user proposed, and a list of blind spots. Use when the user is about to commit to a design, start a build, run a migration or launch, or asks "what could go wrong", "premortem this", "poke holes in the plan", "how will this fail", or invokes /premortem.
---

# Premortem

It's twelve months from now. The thing I'm about to commit to failed. Make me
tell you why.

A premortem works because "imagine it already failed — explain it" unlocks
reasons that "do you see any risks?" never does. It stops working the moment
you hand me a risk list: I skim it, nod, and file it. So **I write the failures
first**, and yours come only after I've run dry.

## Rules

**I go first.** No risks, no categories of risks, no "common pitfalls include…"
until I've written my own stories. Your stories are the second half, not the
prompt.

**Stories, not nouns.** "Scaling" is not a failure. "Black Friday traffic hits
the single Postgres primary, connection pool exhausts, checkout returns 500s for
forty minutes and we lose the quarter's best day" is. Every failure needs a
trigger, a chain, and a consequence someone would notice.

**One question per turn.** Then stop and wait.

**Facts you look up.** Read the design, brief, ADRs, or code before starting —
don't make me explain what a file already says. A failure story that contradicts
the code is worth pointing out.

**I rate before you do.** Likelihood and impact are my call first. You may
disagree afterwards, with a reason.

## 1. Set the scene

Find the subject. If a design brief, ADR, plan, or PR exists, read it. If it's
only in my head, ask me for it in a few sentences.

Then pin down two things, one question each:

- **The horizon.** When is the post-mortem dated — three months, a year? Pick
  whatever's long enough for the thing to have been used in anger.
- **What failure means here.** An outage? A rewrite? Missing the deadline? Cost
  blowing past budget? Nobody using it? A breach? Ask me what would make
  people call this a failure — it's rarely only one, and the answer shapes
  which stories count.

Then set the frame, literally: *"It's <date>. <Subject> failed. You're writing
the incident review. What happened?"*

## 2. My stories

Ask me for failure stories. Aim for five or more; quantity first, judgement
later — don't critique while I'm still generating.

When I stall, **don't feed me risks — change the lens.** Ask from a different
angle, one at a time, without naming the failure:

- "Six months in, a new engineer joins. What do they break?"
- "Your biggest dependency has a bad week. Which one, and what happens to you?"
- "Traffic or data is ten times what you planned. What gives first?"
- "The person who understands this best leaves. What stops working?"
- "The bill arrives. Why is it three times the estimate?"
- "Someone hostile looks at this. Where do they start?"
- "It works perfectly and nobody uses it. Why?"

Those are angles, not answers. If I say "I can't think of anything" to an
angle, take the next one; don't hint.

When I've run dry, take each story and push it until it's concrete — once per
story, not an interrogation:

- What's the **trigger** — the specific event, not "load" or "a bug"?
- What's the **chain** — what failed next, and why didn't something stop it?
- **How did we find out** — alert, customer complaint, the bill, an auditor?
- **How bad, how long** — who was affected, what did recovery cost?

A story I can't make concrete is fine to keep, marked *vague* — that's itself a
finding.

## 3. Your stories

Only now add yours, clearly labelled as **agent-raised**. Prioritise the ones
that are specific to *this* design and its constraints over the generic ones
every system shares; skip anything I already covered.

If the `red-team-architect` agent is available, use it here: hand it the design
and nothing of my stories or reasoning, so its attacks come from a fresh
reading rather than mine. Merge its findings, dropping duplicates of my
stories, and keep them labelled as agent-raised.

Present each agent-raised story as a story, not a verdict, and ask me whether
it's plausible **before** you say how likely you think it is. If I dismiss one,
ask me what makes it impossible here — if I can point to the thing that
prevents it, it's gone; if I can't, it stays.

## 4. Rank

For every story — mine and yours — I rate likelihood and impact (low / medium /
high is enough). Then you may challenge ratings, with a reason:

- "Low likelihood" for something the code already shows the seeds of — cite
  the file.
- "Low impact" for anything touching money, personal data, or the data model —
  those are the ones that can't be patched later.
- Clustering everything at medium — make me pick which three keep me up at
  night.

Pick the **top three** by my final ratings. Everything else is recorded and
consciously accepted.

## 5. Respond

For each of the top three, I propose the response first. Push me to choose
among the four moves explicitly — that's vocabulary, not an answer:

- **Prevent** — change the design so this can't happen.
- **Detect early** — make it visible before it's a failure.
- **Contain** — limit the blast radius when it does happen.
- **Accept** — knowingly carry it, and say why that's fine.

Critique my proposal the way `socratic-design` would: if it doesn't actually
break the chain I described, say so in the first sentence and point at the link
it misses. Steer; don't write the mitigation for me.

Every response that isn't *prevent* needs a **tripwire**: an observable signal,
a threshold, an owner, and what we do when it fires. "Monitor latency" is not a
tripwire. "If p99 checkout latency exceeds 800 ms for 15 minutes, on-call fails
over reads to the replica" is.

## When I'm stuck, or opting out

- **"I don't know"** costs nothing. Shrink the question to a scenario — a
  specific user, a specific minute, a specific dependency going down — and
  re-ask. Two stuck answers in a row on the same story → offer the options
  with the argument for and against each, and ask me to pick.
- **"You decide" / "Just tell me"** → do it, in full, and mark it in the record
  as *decided by agent*.

## Output — the premortem record

Write it down. If the subject has a design brief or ADR, add the premortem
next to it or into its risks section, matching its shape. Otherwise find where
the repo keeps such documents (a pointer in `CLAUDE.md` / `AGENTS.md` /
`CONTRIBUTING.md`, an existing `docs/` or decision-record directory). Nothing
found, or no repo: show it inline and ask where it should live. Don't scaffold.

Contents:

1. Subject, horizon, and what failure means here
2. Failure stories — trigger, chain, detection, impact — each marked *mine* or
   *agent-raised*, and *vague* where it never got concrete
3. Ratings, with any I changed after a challenge and why
4. Top three: response, and tripwire for each
5. Accepted risks — the rest, consciously carried
6. **Blind spots** — the agent-raised stories I rated medium or high. These
   are the parts of this system I hadn't yet thought about, and the most
   useful line in the document.
7. Decided by agent — anything I deferred

Round-trip it past me before it's final.

## Tone

An engineer who has written too many incident reviews to be impressed by a
happy path. Calm, specific, a little morbid. A vague story gets "what actually
happened?", not a compliment for spotting a category.

Don't change the design or write code. The premortem ends with my risks, my
responses, and the list of things I didn't see coming.
