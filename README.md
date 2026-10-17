<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg" />
  <img src="./assets/header-light.svg" alt="Sergei Ivanov, systems architect, building Zidos" width="100%" />
</picture>

<p align="center">
  <a href="https://kavioavio.ru">Website</a> ·
  <a href="https://www.linkedin.com/in/sergei-ivanov-73856b3a7">LinkedIn</a>
</p>

I am a systems architect. I work on distributed platforms end to end: topology,
identity, deployment, observability, failure handling, and recovery. Ten years of
that has been systems integration and middleware in production — Kafka, MQ, CDC,
and the operational path around them.

For the last stretch my work has been agent runtimes, and the same question keeps
coming up in a new setting: when a long-running process claims it did something,
what can you actually check?

## Zidos

**An agent runtime with provable execution.** That is what I am building now. A
run is a durable object, not a chat transcript. Every decision is appended to an
event log, and that log is the only source of truth. A run that is interrupted
resumes from what was recorded instead of starting over.

It makes three things explicit that a chat loop leaves implicit:

- **Durability.** The append-only log orders everything by sequence number, never
  by clock. Tool and model calls go `dispatched → committed`, so a crash between
  the two is a known window rather than an unknown.
- **Authority.** The runtime decides what may happen, not the model and not the
  client. A deny holds in every permission mode. Every external effect, such as
  mail, a payment, or a post, needs a fresh human decision.
- **Evidence.** A run does not succeed because the model says it is done. The
  runtime executes the verifier command itself, and a client can neither supply
  the verdict nor skip the gate.

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

What it is not: a hosted service, a model wrapper, an IDE plugin, or a control
plane for other people's agents. You run the binaries and bring your own model
keys; the configuration stores the variable name, never the key.

| | State |
|---|---|
| Runtime and `/v1` API | Works headless end to end. Pre-1.0, no stability promise yet. |
| Source | Closed until launch. |
| Desktop app | Scaffold, not released. |
| Mobile | Not started. |

Zidos will get its own GitHub organization, `zidos-dev`, once the launch surface
settles.

## How I work

- **Start from failure domains, authority boundaries, and recovery objectives** —
  not from the happy path.
- **Bind documentation claims to runnable checks.** Where no check exists, say so
  in the document instead of rounding the gap away.
- **Treat configure, apply, read back, and roll back as one change contract.**
- **Verify the real client path** after infrastructure health returns green.
- **Rehearse failure and clean-host recovery** before relying on a design.
- **A green exit code is not a result.** Whatever produced it — a test, a script,
  or a model — the claim needs an oracle that would have failed.

## Focus

| Area | Work |
|---|---|
| Governed AI execution | Durable run state, permission authority, human approval for real effects, evidence and receipts, multi-provider routing |
| Distributed streaming | Kafka/KRaft topology, quorum design, replication, `min.insync.replicas`, capacity, upgrades, failure boundaries |
| Integration and middleware | Event-driven integration, CDC, connectors, APIs, message contracts, IBM MQ, IBM Integration Bus |
| Identity and policy | TLS/mTLS, SASL, Kerberos, OAuth/OIDC, ACL/RBAC, secret boundaries, fail-closed automation |
| Production operations | Observability, capacity planning, runbooks, rolling changes, backup/DR decisions, restore tests, incident recovery |

## Core technologies

`Go` · `Apache Kafka` · `KRaft` · `IBM MQ` · `IBM Integration Bus` · `Python` ·
`Linux` · `PostgreSQL` · `Docker` · `Kubernetes` · `Ansible` · `Prometheus` ·
`Grafana`

## Public repositories

Most of what I work on lives in private repositories. The public entries on this
account are forks I keep as working copies, not projects of mine:

- [`graphify`](https://github.com/kavioavio/graphify) — fork of
  [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify).
- [`hermes-agent`](https://github.com/kavioavio/hermes-agent) — fork of
  [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent).

## Public GitHub activity

<p align="center">
  <img src="./github-metrics.svg" alt="Public GitHub activity and contribution calendar" width="480" />
</p>

Generated from public GitHub events. Private repository activity is excluded, so
this chart understates the work.

## Contact

For systems architecture, middleware, platform engineering, or technical advisory
work: [LinkedIn](https://www.linkedin.com/in/sergei-ivanov-73856b3a7) ·
[kavioavio.ru](https://kavioavio.ru)

<!-- github-profile-readme -->
<!-- Header images are generated by design/build.py from the Zidos design tokens. -->
