<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg" />
  <img src="./assets/header-light.svg" alt="Zidos, an agent runtime with provable execution" width="100%" />
</picture>

Zidos runs coding and operations tasks headlessly. A run is a durable object, not
a chat transcript: every decision is appended to an event log, the log is the only
source of truth, and a run that is interrupted resumes from what was recorded
instead of starting over. Effects that touch the world outside the workspace pass
a permission gate, and completion is decided by a verifier command that the
runtime executes itself.

It is written in Go, ships as a few binaries, and talks to models you bring
yourself.

## Why it exists

Most agent tooling is built around an interactive session. The session holds the
state, the model reports its own success, and a crash loses the work. That is a
reasonable design for a five-minute task with a human watching. It stops being
reasonable when a run lasts hours, edits a repository, spends money, or sends
mail.

Zidos makes three things explicit that a chat loop leaves implicit.

**Durability.** The append-only event log is the source of truth. Sequence
numbers are gapless per run and are the only ordering authority; timestamps are
for humans. Tool and model calls follow a `dispatched → committed` ladder, so a
crash between the two is a recognizable window rather than an unknown.

**Authority.** The runtime decides what may happen, not the model and not the
client. A deny is a boundary in every permission mode, including the permissive
ones. External effects such as mail, payments, and posts require a fresh human
decision on every action. Clients render; they do not adjudicate.

**Evidence.** A run does not succeed because the model says it is done. The exit
gate executes the verifier command itself and is blind to the stated goal. A
client may neither supply the verdict nor skip the gate.

## How a run works

```
run.created ──▶ step ──▶ model attempt ──▶ tool invocation ──▶ step closed
                 ▲                                                 │
                 └─────────────── loop until finish ───────────────┘
                                                                   │
                                                            finish.claimed
                                                                   │
                                             exit gate: the runtime executes the verifier
                                                                   │
                                                      run.succeeded / run.failed
```

Every identifier is assigned by the runtime, never by the model and never derived
from a wall clock. Every retry, fallback, and stream continuation opens a new
attempt with a typed cause, so a run's history says why each call happened.

## What Zidos is not

- **Not a hosted service.** You run the binaries. Provider keys are yours; the
  configuration stores the environment variable name, never the key.
- **Not a model or a model wrapper.** The provider is a per-task choice,
  including OpenAI-compatible endpoints and a local Ollama.
- **Not an IDE plugin or a chat front end.** There is a terminal loop and a
  desktop scaffold; the product is the runtime underneath them.
- **Not a control plane for other people's agents.**

## Status

Stated plainly:

| Area | State |
|---|---|
| Runtime and `/v1` API | Headless runs work end to end. Pre-1.0; nothing carries a stability promise yet. |
| Source | Closed until launch. No public release has been tagged. |
| Desktop app | Scaffold. Builds, not released. |
| Windows | Native sandboxing implemented and tested on NTFS; full release acceptance tracked separately. |
| Mobile | Not started. |

## Contact

Zidos is built by [Sergei Ivanov](https://github.com/kavioavio).
For early access or questions:
[LinkedIn](https://www.linkedin.com/in/sergei-ivanov-73856b3a7).
